def _sort_private(
    prot: ABY3,
    x: ABY3PrivateTensor,
    axis: int,
    acc: bool = True,
) -> ABY3PrivateTensor:

    with tf.name_scope("sort"):

        def bitonic_index(n, stage, sub_stage):
            assert sub_stage <= stage, "The i-th stage can have at most i+1 sub stages."
            # In bitonic sorting network, the 0-th sub stage in each stage has a different pattern from
            # other sub stages.
            if sub_stage == 0:
                a = np.arange(n)
                b = np.split(a, n / (2**stage))
                left = np.concatenate(b[0::2])
                right = np.concatenate([np.flip(x) for x in b[1::2]])
                return (left, right)
            else:
                a = np.arange(n)
                b = np.split(a, n / (2 ** (stage - sub_stage)))
                left = np.concatenate(b[0::2])
                right = np.concatenate(b[1::2])
                return (left, right)

        # def bitonic_sort(x):
        # n = int(x.shape[0])
        # n_stages = ceil(log2(n))
        # for stage in range(n_stages):
        # print("building stage: ", stage)
        # for sub_stage in range(stage + 1):
        # left_idx, right_idx = bitonic_index(n, stage, sub_stage)
        # left = prot.gather(x, left_idx)
        # right = prot.gather(x, right_idx)
        # left, right = prot.cmp_swap(left, right)
        # z0 = prot.scatter_nd(
        # np.expand_dims(left_idx, axis=1),
        # left,
        # x.shape)
        # z1 = prot.scatter_nd(
        # np.expand_dims(right_idx, axis=1),
        # right,
        # x.shape)
        # x = z0 + z1
        # return x

        # return bitonic_sort(x)

        def build_bitonic_index(n):
            indices = []
            n_stages = ceil(log2(n))
            for stage in range(n_stages):
                for sub_stage in range(stage + 1):
                    left_idx, right_idx = bitonic_index(n, stage, sub_stage)
                    indices.append(np.stack([left_idx, right_idx]))
            return np.stack(indices)

        axis = axis % len(x.shape)
        if axis < 0:
            axis += len(x.shape)
        if axis != 0:
            x = prot.transpose(
                x,
                perm=[axis]
                + list(range(0, axis))
                + list(range(axis + 1, len(x.shape))),
            )

        unpadded_n = int(x.shape[0])
        n = next_power_of_two(unpadded_n)
        if n > unpadded_n:
            # We can only handle numbers of bit length k-2 for comparison
            max_bound = (1 << (x.backing_dtype.nbits - 2)) - 1
            pad = prot.define_constant(
                np.ones([n - unpadded_n] + x.shape[1:]) * max_bound, apply_scaling=False
            )
            pad = pad.to_private(x.share_type)
            pad.is_scaled = x.is_scaled
            x = prot.concat([x, pad], axis=0)

        n_stages = ceil(log2(n))
        n_sub_stages = int((1 + n_stages) * n_stages / 2)

        indices = build_bitonic_index(n)
        indices = prot.define_constant(indices, apply_scaling=False)

        def cond(i, x):
            return i < n_sub_stages

        def body(i, x):
            left_idx = indices[i][0]
            right_idx = indices[i][1]

            left = prot.gather(x, left_idx, axis=0)
            right = prot.gather(x, right_idx, axis=0)
            min_, max_ = prot.cmp_swap(left, right)

            if acc:
                min_idx, max_idx = (left_idx, right_idx)
            else:
                min_idx, max_idx = (right_idx, left_idx)

            z0 = prot.scatter_nd(prot.expand_dims(min_idx, axis=1), min_, x.shape)
            z1 = prot.scatter_nd(prot.expand_dims(max_idx, axis=1), max_, x.shape)
            x = z0 + z1

            return (i + 1, x)

        _, x = prot.while_loop(cond, body, [tf.constant(0), x])
        if n > unpadded_n:
            if acc:
                x = x[:unpadded_n]
            else:
                x = x[(n - unpadded_n) :]
        if axis != 0:
            x = prot.transpose(
                x,
                perm=list(range(1, axis + 1))
                + [0]
                + list(range(axis + 1, len(x.shape))),
            )
        return x