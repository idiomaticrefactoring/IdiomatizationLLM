def conv3d_strategy_cuda(attrs, inputs, out_type, target):
    """conv3d cuda strategy"""
    strategy = _op.OpStrategy()
    data, kernel = inputs
    layout = attrs.data_layout
    _, stride_h, stride_w = attrs.get_int_tuple("strides")
    _, dilation_h, dilation_w = attrs.get_int_tuple("dilation")
    assert layout in ["NCDHW", "NDHWC"], "Not support this layout {} yet".format(layout)
    if layout == "NCDHW":
        strategy.add_implementation(
            wrap_compute_conv3d(topi.cuda.conv3d_ncdhw),
            wrap_topi_schedule(topi.cuda.schedule_conv3d_ncdhw),
            name="conv3d_ncdhw.cuda",
            plevel=10,
        )
        _, _, _, kh, kw = get_const_tuple(kernel.shape)
        if (
            2 < kh < 8
            and 2 < kw < 8
            and kh == kw
            and stride_h == 1
            and stride_w == 1
            and dilation_h == 1
            and dilation_w == 1
            and attrs["groups"] == 1
        ):
            strategy.add_implementation(
                wrap_compute_conv3d(topi.cuda.conv3d_ncdhw_winograd),
                wrap_topi_schedule(topi.cuda.schedule_conv3d_ncdhw_winograd),
                name="conv3d_ncdhw_winograd.cuda",
                plevel=5,
            )
    else:  # layout == "NDHWC":
        strategy.add_implementation(
            wrap_compute_conv3d(topi.cuda.conv3d_ndhwc),
            wrap_topi_schedule(topi.cuda.schedule_conv3d_ndhwc),
            name="conv3d_ndhwc.cuda",
            plevel=10,
        )
        N, _, _, _, _ = get_const_tuple(data.shape)
        _, _, _, CI, CO = get_const_tuple(kernel.shape)
        if target.kind.name == "cuda":
            if nvcc.have_tensorcore(target=target):
                if (
                    (N % 16 == 0 and CI % 16 == 0 and CO % 16 == 0)
                    or (N % 8 == 0 and CI % 16 == 0 and CO % 32 == 0)
                    or (N % 32 == 0 and CI % 16 == 0 and CO % 8 == 0)
                ) and out_type == "float16":
                    strategy.add_implementation(
                        wrap_compute_conv3d(topi.cuda.conv3d_ndhwc_tensorcore),
                        wrap_topi_schedule(topi.cuda.schedule_conv3d_ndhwc_tensorcore),
                        name="conv3d_ndhwc_tensorcore.cuda",
                        plevel=20,
                    )

    if target.kind.name == "cuda" and "cudnn" in target.libs:
        strategy.add_implementation(
            wrap_compute_conv3d(topi.cuda.conv3d_cudnn, True),
            wrap_topi_schedule(topi.cuda.schedule_conv3d_cudnn),
            name="conv3d_cudnn.cuda",
            plevel=25,
        )
    return strategy


def optimize_parameters(self, step):
    # G
    for p in self.netD.parameters():
        p.requires_grad = False

    self.optimizer_G.zero_grad()

    self.input = self.real_H
    self.output = self.netG(x=self.input)

    loss = 0
    zshape = self.output[:, 3:, :, :].shape

    LR = self.Quantization(self.output[:, :3, :, :])

    gaussian_scale = self.train_opt['gaussian_scale'] if self.train_opt['gaussian_scale'] != None else 1
    y_ = torch.cat((LR, gaussian_scale * self.gaussian_batch(zshape)), dim=1)

    self.fake_H = self.netG(x=y_, rev=True)

    if step % self.D_update_ratio == 0 and step > self.D_init_iters:
        l_forw_fit = self.loss_forward(self.output, self.ref_L)
        l_back_rec, l_back_fea, l_back_gan = self.loss_backward(self.real_H, self.fake_H)

        loss += l_forw_fit + l_back_rec + l_back_fea + l_back_gan

        loss.backward()

        # gradient clipping
        if self.train_opt['gradient_clipping']:
            nn.utils.clip_grad_norm_(self.netG.parameters(), self.train_opt['gradient_clipping'])

        self.optimizer_G.step()

    # D
    for p in self.netD.parameters():
        p.requires_grad = True

    self.optimizer_D.zero_grad()
    l_d_total = 0
    pred_d_real = self.netD(self.real_H)
    pred_d_fake = self.netD(self.fake_H.detach())
    if self.opt['train']['gan_type'] == 'gan':
        l_d_real = self.cri_gan(pred_d_real, True)
        l_d_fake = self.cri_gan(pred_d_fake, False)
        l_d_total = l_d_real + l_d_fake
    elif self.opt['train']['gan_type'] == 'ragan':
        l_d_real = self.cri_gan(pred_d_real - torch.mean(pred_d_fake), True)
        l_d_fake = self.cri_gan(pred_d_fake - torch.mean(pred_d_real), False)
        l_d_total = (l_d_real + l_d_fake) / 2

    l_d_total.backward()
    self.optimizer_D.step()

    # set log
    if step % self.D_update_ratio == 0 and step > self.D_init_iters:
        self.log_dict['l_forw_fit'] = l_forw_fit.item()
        self.log_dict['l_back_rec'] = l_back_rec.item()
        self.log_dict['l_back_fea'] = l_back_fea.item()
        self.log_dict['l_back_gan'] = l_back_gan.item()
    self.log_dict['l_d'] = l_d_total.item()

    def __init__(
            self,
            outcome_learners: Optional[Sequence[AutoML]] = None,
            effect_learners: Optional[Sequence[AutoML]] = None,
            propensity_learner: Optional[AutoML] = None,
            base_task: Optional[Task] = None,
            timeout: Optional[int] = None,
            cpu_limit: int = 4,
            gpu_ids: Optional[str] = "all",
    ):
        if (outcome_learners is None or len(outcome_learners) == 0) and base_task is None:
            raise RuntimeError('Must specify any of learners or "base_task"')

        if outcome_learners is not None and len(outcome_learners) > 0:
            base_task = self._get_task(outcome_learners[0])
            super().__init__(self._get_task(outcome_learners[0]))

        super().__init__(base_task, timeout, cpu_limit, gpu_ids)

        self.learners: Dict[str, Union[Dict[str, AutoML], AutoML]] = {
            "outcome": {},
            "effect": {},
        }
        if propensity_learner is None:
            self.learners["propensity"] = self._get_default_learner(Task("binary"))
        else:
            self.learners["propensity"] = propensity_learner

        if outcome_learners is None or len(outcome_learners) == 0:
            self.learners["outcome"]["control"] = self._get_default_learner(self.base_task)
            self.learners["outcome"]["treatment"] = self._get_default_learner(self.base_task)
        elif len(outcome_learners) == 1:
            self.learners["outcome"]["control"] = outcome_learners[0]
            self.learners["outcome"]["treatment"] = copy.deepcopy(outcome_learners[0])
        elif len(outcome_learners) == 2:
            self.learners["outcome"]["control"] = outcome_learners[0]
            self.learners["outcome"]["treatment"] = outcome_learners[1]
        else:
            raise RuntimeError('The number of "outcome_learners" must be 0/1/2')

        if effect_learners is None or len(effect_learners) == 0:
            self.learners["effect"]["control"] = self._get_default_learner(Task("reg"))
            self.learners["effect"]["treatment"] = self._get_default_learner(Task("reg"))
        elif len(effect_learners) == 1:
            self.learners["effect"]["control"] = effect_learners[0]
            self.learners["effect"]["treatment"] = copy.deepcopy(effect_learners[0])
        elif len(effect_learners) == 2:
            self.learners["effect"]["control"] = effect_learners[0]
            self.learners["effect"]["treatment"] = effect_learners[1]
        else:
            raise RuntimeError('The number of "effect_learners" must be 0/1/2')

def train_progressive_gan(
    G_smoothing             = 0.999,        # Exponential running average of generator weights.
    D_repeats               = 1,            # How many times the discriminator is trained per G iteration.
    minibatch_repeats       = 4,            # Number of minibatches to run before adjusting training parameters.
    reset_opt_for_new_lod   = True,         # Reset optimizer internal state (e.g. Adam moments) when new layers are introduced?
    total_kimg              = 15000,        # Total length of the training, measured in thousands of real images.
    mirror_augment          = False,        # Enable mirror augment?
    drange_net              = [-1,1],       # Dynamic range used when feeding image data to the networks.
    image_snapshot_ticks    = 1,            # How often to export image snapshots?
    network_snapshot_ticks  = 10,           # How often to export network snapshots?
    save_tf_graph           = False,        # Include full TensorFlow computation graph in the tfevents file?
    save_weight_histograms  = False,        # Include weight histograms in the tfevents file?
    resume_run_id           = None,         # Run ID or network pkl to resume training from, None = start from scratch.
    resume_snapshot         = None,         # Snapshot index to resume training from, None = autodetect.
    resume_kimg             = 0.0,          # Assumed training progress at the beginning. Affects reporting and training schedule.
    resume_time             = 0.0):         # Assumed wallclock time at the beginning. Affects reporting.

    maintenance_start_time = time.time()
    training_set = dataset.load_dataset(data_dir=config.data_dir, verbose=True, **config.dataset)

    # Construct networks.
    with tf.device('/gpu:0'):
        if resume_run_id is not None:
            network_pkl = misc.locate_network_pkl(resume_run_id, resume_snapshot)
            print('Loading networks from "%s"...' % network_pkl)
            G, D, Gs = misc.load_pkl(network_pkl)
        else:
            print('Constructing networks...')
            G = tfutil.Network('G', num_channels=training_set.shape[0], resolution=training_set.shape[1], label_size=training_set.label_size, **config.G)
            D = tfutil.Network('D', num_channels=training_set.shape[0], resolution=training_set.shape[1], label_size=training_set.label_size, **config.D)
            Gs = G.clone('Gs')
        Gs_update_op = Gs.setup_as_moving_average_of(G, beta=G_smoothing)
    G.print_layers(); D.print_layers()

    print('Building TensorFlow graph...')
    with tf.name_scope('Inputs'):
        lod_in          = tf.placeholder(tf.float32, name='lod_in', shape=[])
        lrate_in        = tf.placeholder(tf.float32, name='lrate_in', shape=[])
        minibatch_in    = tf.placeholder(tf.int32, name='minibatch_in', shape=[])
        minibatch_split = minibatch_in // config.num_gpus
        reals, labels   = training_set.get_minibatch_tf()
        reals_split     = tf.split(reals, config.num_gpus)
        labels_split    = tf.split(labels, config.num_gpus)
    G_opt = tfutil.Optimizer(name='TrainG', learning_rate=lrate_in, **config.G_opt)
    D_opt = tfutil.Optimizer(name='TrainD', learning_rate=lrate_in, **config.D_opt)
    for gpu in range(config.num_gpus):
        with tf.name_scope('GPU%d' % gpu), tf.device('/gpu:%d' % gpu):
            G_gpu = G if gpu == 0 else G.clone(G.name + '_shadow')
            D_gpu = D if gpu == 0 else D.clone(D.name + '_shadow')
            lod_assign_ops = [tf.assign(G_gpu.find_var('lod'), lod_in), tf.assign(D_gpu.find_var('lod'), lod_in)]
            reals_gpu = process_reals(reals_split[gpu], lod_in, mirror_augment, training_set.dynamic_range, drange_net)
            labels_gpu = labels_split[gpu]
            with tf.name_scope('G_loss'), tf.control_dependencies(lod_assign_ops):
                G_loss = tfutil.call_func_by_name(G=G_gpu, D=D_gpu, opt=G_opt, training_set=training_set, minibatch_size=minibatch_split, **config.G_loss)
            with tf.name_scope('D_loss'), tf.control_dependencies(lod_assign_ops):
                D_loss = tfutil.call_func_by_name(G=G_gpu, D=D_gpu, opt=D_opt, training_set=training_set, minibatch_size=minibatch_split, reals=reals_gpu, labels=labels_gpu, **config.D_loss)
            G_opt.register_gradients(tf.reduce_mean(G_loss), G_gpu.trainables)
            D_opt.register_gradients(tf.reduce_mean(D_loss), D_gpu.trainables)
    G_train_op = G_opt.apply_updates()
    D_train_op = D_opt.apply_updates()

    print('Setting up snapshot image grid...')
    grid_size, grid_reals, grid_labels, grid_latents = setup_snapshot_image_grid(G, training_set, **config.grid)
    sched = TrainingSchedule(total_kimg * 1000, training_set, **config.sched)
    grid_fakes = Gs.run(grid_latents, grid_labels, minibatch_size=sched.minibatch//config.num_gpus)

    print('Setting up result dir...')
    result_subdir = misc.create_result_subdir(config.result_dir, config.desc)
    misc.save_image_grid(grid_reals, os.path.join(result_subdir, 'reals.png'), drange=training_set.dynamic_range, grid_size=grid_size)
    misc.save_image_grid(grid_fakes, os.path.join(result_subdir, 'fakes%06d.png' % 0), drange=drange_net, grid_size=grid_size)
    summary_log = tf.summary.FileWriter(result_subdir)
    if save_tf_graph:
        summary_log.add_graph(tf.get_default_graph())
    if save_weight_histograms:
        G.setup_weight_histograms(); D.setup_weight_histograms()

    print('Training...')
    cur_nimg = int(resume_kimg * 1000)
    cur_tick = 0
    tick_start_nimg = cur_nimg
    tick_start_time = time.time()
    train_start_time = tick_start_time - resume_time
    prev_lod = -1.0
    while cur_nimg < total_kimg * 1000:

        # Choose training parameters and configure training ops.
        sched = TrainingSchedule(cur_nimg, training_set, **config.sched)
        training_set.configure(sched.minibatch, sched.lod)
        if reset_opt_for_new_lod:
            if np.floor(sched.lod) != np.floor(prev_lod) or np.ceil(sched.lod) != np.ceil(prev_lod):
                G_opt.reset_optimizer_state(); D_opt.reset_optimizer_state()
        prev_lod = sched.lod

        # Run training ops.
        for repeat in range(minibatch_repeats):
            for _ in range(D_repeats):
                tfutil.run([D_train_op, Gs_update_op], {lod_in: sched.lod, lrate_in: sched.D_lrate, minibatch_in: sched.minibatch})
                cur_nimg += sched.minibatch
            tfutil.run([G_train_op], {lod_in: sched.lod, lrate_in: sched.G_lrate, minibatch_in: sched.minibatch})

        # Perform maintenance tasks once per tick.
        done = (cur_nimg >= total_kimg * 1000)
        if cur_nimg >= tick_start_nimg + sched.tick_kimg * 1000 or done:
            cur_tick += 1
            cur_time = time.time()
            tick_kimg = (cur_nimg - tick_start_nimg) / 1000.0
            tick_start_nimg = cur_nimg
            tick_time = cur_time - tick_start_time
            total_time = cur_time - train_start_time
            maintenance_time = tick_start_time - maintenance_start_time
            maintenance_start_time = cur_time

            # Report progress.
            print('tick %-5d kimg %-8.1f lod %-5.2f minibatch %-4d time %-12s sec/tick %-7.1f sec/kimg %-7.2f maintenance %.1f' % (
                tfutil.autosummary('Progress/tick', cur_tick),
                tfutil.autosummary('Progress/kimg', cur_nimg / 1000.0),
                tfutil.autosummary('Progress/lod', sched.lod),
                tfutil.autosummary('Progress/minibatch', sched.minibatch),
                misc.format_time(tfutil.autosummary('Timing/total_sec', total_time)),
                tfutil.autosummary('Timing/sec_per_tick', tick_time),
                tfutil.autosummary('Timing/sec_per_kimg', tick_time / tick_kimg),
                tfutil.autosummary('Timing/maintenance_sec', maintenance_time)))
            tfutil.autosummary('Timing/total_hours', total_time / (60.0 * 60.0))
            tfutil.autosummary('Timing/total_days', total_time / (24.0 * 60.0 * 60.0))
            tfutil.save_summaries(summary_log, cur_nimg)

            # Save snapshots.
            if cur_tick % image_snapshot_ticks == 0 or done:
                grid_fakes = Gs.run(grid_latents, grid_labels, minibatch_size=sched.minibatch//config.num_gpus)
                misc.save_image_grid(grid_fakes, os.path.join(result_subdir, 'fakes%06d.png' % (cur_nimg // 1000)), drange=drange_net, grid_size=grid_size)
            if cur_tick % network_snapshot_ticks == 0 or done:
                misc.save_pkl((G, D, Gs), os.path.join(result_subdir, 'network-snapshot-%06d.pkl' % (cur_nimg // 1000)))

            # Record start time of the next tick.
            tick_start_time = time.time()

    # Write final results.
    misc.save_pkl((G, D, Gs), os.path.join(result_subdir, 'network-final.pkl'))
    summary_log.close()
    open(os.path.join(result_subdir, '_training-done.txt'), 'wt').close()

    def iterate(self):
        """Perform one step in the algorithm.

        Implements Algorithm 4.1(k=1) or 4.2(k=2) in [APS1995]
        """
        self.iterations += 1
        eps = np.finfo(float).eps
        d, fd, e, fe = self.d, self.fd, self.e, self.fe
        ab_width = self.ab[1] - self.ab[0]  # Need the start width below
        c = None

        for nsteps in range(2, self.k + 2):
            # If the f-values are sufficiently separated, perform an inverse
            # polynomial interpolation step. Otherwise, nsteps repeats of
            # an approximate Newton-Raphson step.
            if _notclose(self.fab + [fd, fe], rtol=0, atol=32 * eps):
                c0 = _inverse_poly_zero(self.ab[0], self.ab[1], d, e,
                                        self.fab[0], self.fab[1], fd, fe)
                if self.ab[0] < c0 < self.ab[1]:
                    c = c0
            if c is None:
                c = _newton_quadratic(self.ab, self.fab, d, fd, nsteps)

            fc = self._callf(c)
            if fc == 0:
                return _ECONVERGED, c

            # re-bracket
            e, fe = d, fd
            d, fd = self._update_bracket(c, fc)

        # u is the endpoint with the smallest f-value
        uix = (0 if np.abs(self.fab[0]) < np.abs(self.fab[1]) else 1)
        u, fu = self.ab[uix], self.fab[uix]

        _, A = _compute_divided_differences(self.ab, self.fab,
                                            forward=(uix == 0), full=False)
        c = u - 2 * fu / A
        if np.abs(c - u) > 0.5 * (self.ab[1] - self.ab[0]):
            c = sum(self.ab) / 2.0
        else:
            if np.isclose(c, u, rtol=eps, atol=0):
                # c didn't change (much).
                # Either because the f-values at the endpoints have vastly
                # differing magnitudes, or because the root is very close to
                # that endpoint
                frs = np.frexp(self.fab)[1]
                if frs[uix] < frs[1 - uix] - 50:  # Differ by more than 2**50
                    c = (31 * self.ab[uix] + self.ab[1 - uix]) / 32
                else:
                    # Make a bigger adjustment, about the
                    # size of the requested tolerance.
                    mm = (1 if uix == 0 else -1)
                    adj = mm * np.abs(c) * self.rtol + mm * self.xtol
                    c = u + adj
                if not self.ab[0] < c < self.ab[1]:
                    c = sum(self.ab) / 2.0

        fc = self._callf(c)
        if fc == 0:
            return _ECONVERGED, c

        def __init__(self, class_dim: int = 1000, load_checkpoint: str = None):
            super(ResNeXt101_vd, self).__init__()

            self.layers = 101
            self.cardinality = 64
            depth = [3, 4, 23, 3]
            num_channels = [64, 256, 512, 1024]
            num_filters = [256, 512, 1024, 2048]

            self.conv1_1 = ConvBNLayer(num_channels=3, num_filters=32, filter_size=3, stride=2, act='relu',
                                       name="conv1_1")
            self.conv1_2 = ConvBNLayer(num_channels=32, num_filters=32, filter_size=3, stride=1, act='relu',
                                       name="conv1_2")
            self.conv1_3 = ConvBNLayer(num_channels=32, num_filters=64, filter_size=3, stride=1, act='relu',
                                       name="conv1_3")

            self.pool2d_max = MaxPool2d(kernel_size=3, stride=2, padding=1)

            self.block_list = []
            for block in range(len(depth)):
                shortcut = False
                for i in range(depth[block]):
                    if block == 2:
                        if i == 0:
                            conv_name = "res" + str(block + 2) + "a"
                        else:
                            conv_name = "res" + str(block + 2) + "b" + str(i)
                    else:
                        conv_name = "res" + str(block + 2) + chr(97 + i)
                    bottleneck_block = self.add_sublayer(
                        'bb_%d_%d' % (block, i),
                        BottleneckBlock(
                            num_channels=num_channels[block]
                            if i == 0 else num_filters[block] * int(64 // self.cardinality),
                            num_filters=num_filters[block],
                            stride=2 if i == 0 and block != 0 else 1,
                            cardinality=self.cardinality,
                            shortcut=shortcut,
                            if_first=block == i == 0,
                            name=conv_name))
                    self.block_list.append(bottleneck_block)
                    shortcut = True

            self.pool2d_avg = AdaptiveAvgPool2d(1)

            self.pool2d_avg_channels = num_channels[-1] * 2

            stdv = 1.0 / math.sqrt(self.pool2d_avg_channels * 1.0)

            self.out = Linear(
                self.pool2d_avg_channels,
                class_dim,
                weight_attr=ParamAttr(initializer=Uniform(-stdv, stdv), name="fc_weights"),
                bias_attr=ParamAttr(name="fc_offset"))

            if load_checkpoint is not None:
                model_dict = paddle.load(load_checkpoint)[0]
                self.set_dict(model_dict)
                print("load custom checkpoint success")

            else:
                checkpoint = os.path.join(self.directory, 'resnext101_vd_64x4d_imagenet.pdparams')
                if not os.path.exists(checkpoint):
                    os.system(
                        'wget https://paddlehub.bj.bcebos.com/dygraph/image_classification/resnext101_vd_64x4d_imagenet.pdparams -O '
                        + checkpoint)
                model_dict = paddle.load(checkpoint)[0]
                self.set_dict(model_dict)
                print("load pretrained checkpoint success")

        e, fe = d, fd
        d, fd = self._update_bracket(c, fc)

        # If the width of the new interval did not decrease enough, bisect
        if self.ab[1] - self.ab[0] > self._MU * ab_width:
            e, fe = d, fd
            z = sum(self.ab) / 2.0
            fz = self._callf(z)
            if fz == 0:
                return _ECONVERGED, z
            d, fd = self._update_bracket(z, fz)

        # Record d and e for next iteration
        self.d, self.fd = d, fd
        self.e, self.fe = e, fe

        status, xn = self.get_status()
        return status, xn


def main_worker(gpu, ngpus_per_node, args):
    global best_acc1
    args.gpu = gpu
    use_crossval = args.cvn > 0
    use_mask = args.dir_train_mask is not None
    cv_fold = args.cv
    cv_n_folds = args.cvn
    class_weights = None

    if use_crossval and use_mask:
        raise ValueError('Either args.cvn > 0 or dir-train-mask not None, but not both.')

    if args.gpu is not None:
        print("Use GPU: {} for training".format(args.gpu))

    if args.distributed:
        if args.dist_url == "env://" and args.rank == -1:
            args.rank = int(os.environ["RANK"])
        if args.multiprocessing_distributed:
            # For multiprocessing distributed training, rank needs to be the
            # global rank among all the processes
            args.rank = args.rank * ngpus_per_node + gpu
        dist.init_process_group(backend=args.dist_backend, init_method=args.dist_url,
                                world_size=args.world_size, rank=args.rank)
    # create model
    if args.pretrained:
        print("=> using pre-trained model '{}'".format(args.arch))
        model = models.__dict__[args.arch](
            pretrained=True, num_classes=num_classes)
    else:
        print("=> creating model '{}'".format(args.arch))
        model = models.__dict__[args.arch](num_classes=num_classes)

    if args.distributed:
        # For multiprocessing distributed, DistributedDataParallel constructor
        # should always set the single device scope, otherwise,
        # DistributedDataParallel will use all available devices.
        if args.gpu is not None:
            torch.cuda.set_device(args.gpu)
            model.cuda(args.gpu)
            # When using a single GPU per process and per
            # DistributedDataParallel, we need to divide the batch size
            # ourselves based on the total number of GPUs we have
            args.batch_size = int(args.batch_size / ngpus_per_node)
            args.workers = int(args.workers / ngpus_per_node)
            model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[args.gpu])
        else:
            model.cuda()
            # DistributedDataParallel will divide and allocate batch_size to all
            # available GPUs if device_ids are not set
            model = torch.nn.parallel.DistributedDataParallel(model)
    elif args.gpu is not None:
        torch.cuda.set_device(args.gpu)
        model = model.cuda(args.gpu)
    else:
        # DataParallel will divide and allocate batch_size to all available GPUs
        if args.arch.startswith('alexnet') or args.arch.startswith('vgg'):
            model.features = torch.nn.DataParallel(model.features)
            model.cuda()
        else:
            model = torch.nn.DataParallel(model).cuda()

            # define optimizer
    optimizer = torch.optim.SGD(model.parameters(), args.lr,
                                momentum=args.momentum,
                                weight_decay=args.weight_decay)

    # optionally resume from a checkpoint
    if args.resume:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            if args.gpu is None:
                checkpoint = torch.load(args.resume)
            else:
                # Map model to be loaded to specified single gpu.
                loc = 'cuda:{}'.format(args.gpu)
                checkpoint = torch.load(args.resume, map_location=loc)
            args.start_epoch = checkpoint['epoch']
            best_acc1 = checkpoint['best_acc1']
            if args.gpu is not None:
                # In case you load checkpoint from different GPU
                best_acc1 = best_acc1.to(args.gpu)
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            print("=> loaded checkpoint '{}' (epoch {})"
                  .format(args.resume, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))

    cudnn.benchmark = True

    # Data loading code
    traindir = os.path.join(args.data, 'train')
    valdir = os.path.join(args.data, 'test')

    train_dataset = datasets.ImageFolder(
        traindir,
        transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(
                [0.507, 0.487, 0.4417],
                [0.267, 0.256, 0.276],
            ),
        ]),
    )

    # if training labels are provided use those instead of dataset labels
    if args.train_labels is not None:
        with open(args.train_labels, 'r') as rf:
            train_labels_dict = json.load(rf)
        train_dataset.imgs = [(fn, train_labels_dict[fn]) for fn, _ in train_dataset.imgs]
        train_dataset.samples = train_dataset.imgs

    # If training only on a cross-validated portion & make val_set = train_holdout.
    if use_crossval:
        checkpoint_fn = "model_{}__fold_{}__checkpoint.pth.tar".format(args.arch, cv_fold)
        print('Computing fold indices. This takes 15 seconds.')
        # Prepare labels
        labels = [label for img, label in datasets.ImageFolder(traindir).imgs]
        # Split train into train and holdout for particular cv_fold.
        kf = StratifiedKFold(n_splits=cv_n_folds, shuffle=True, random_state=args.cv_seed)
        cv_train_idx, cv_holdout_idx = list(kf.split(range(len(labels)), labels))[cv_fold]
        # Seperate datasets
        np.random.seed(args.cv_seed)
        holdout_dataset = copy.deepcopy(train_dataset)
        holdout_dataset.imgs = [train_dataset.imgs[i] for i in cv_holdout_idx]
        holdout_dataset.samples = holdout_dataset.imgs
        train_dataset.imgs = [train_dataset.imgs[i] for i in cv_train_idx]
        train_dataset.samples = train_dataset.imgs
        print('Train size:', len(cv_train_idx), len(train_dataset.imgs))
        print('Holdout size:', len(cv_holdout_idx), len(holdout_dataset.imgs))
    else:
        checkpoint_fn = "model_{}__checkpoint.pth.tar".format(args.arch)
        if use_mask:
            checkpoint_fn = "model_{}__masked__checkpoint.pth.tar".format(args.arch)
            orig_class_counts = np.bincount(
                [lab for img, lab in datasets.ImageFolder(traindir).imgs])
            train_bool_mask = np.load(args.dir_train_mask)
            # Mask labels
            train_dataset.imgs = [img for i, img in enumerate(train_dataset.imgs) if train_bool_mask[i]]
            train_dataset.samples = train_dataset.imgs
            clean_class_counts = np.bincount(
                [lab for img, lab in train_dataset.imgs])
            print('Train size:', len(train_dataset.imgs))
            # Compute class weights to re-weight loss during training
            # Should use the confident joint to estimate the noise matrix then
            # class_weights = 1 / p(s=k, y=k) for each class k.
            # Here we approximate this with a simpler approach
            # class_weights = count(y=k) / count(s=k, y=k)
            class_weights = torch.Tensor(orig_class_counts / clean_class_counts)

    val_dataset = datasets.ImageFolder(
        valdir,
        transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(
                [0.507, 0.487, 0.441],
                [0.267, 0.256, 0.276],
            ),
        ]),
    )

    if args.distributed:
        train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)
    else:
        train_sampler = None

    train_loader = torch.utils.data.DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=(train_sampler is None),
        num_workers=args.workers, pin_memory=True, sampler=train_sampler,
    )

    val_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=args.batch_size, shuffle=False,
        num_workers=args.workers, pin_memory=True,
    )

    # define loss function (criterion)
    criterion = nn.CrossEntropyLoss(weight=class_weights).cuda(args.gpu)

    if args.evaluate:
        validate(val_loader, model, criterion, args)
        return

    for epoch in range(args.start_epoch, args.epochs):
        if args.distributed:
            train_sampler.set_epoch(epoch)
        adjust_learning_rate(optimizer, epoch, args)

        # train for one epoch
        train(train_loader, model, criterion, optimizer, epoch, args)

        # evaluate on validation set
        acc1 = validate(val_loader, model, criterion, args)

        # remember best acc@1, model, and save checkpoint
        is_best = acc1 > best_acc1
        best_acc1 = max(best_acc1, acc1)

        if not args.multiprocessing_distributed or (args.multiprocessing_distributed
                                                    and args.rank % ngpus_per_node == 0):
            save_checkpoint(
                {
                    'epoch': epoch + 1,
                    'arch': args.arch,
                    'state_dict': model.state_dict(),
                    'best_acc1': best_acc1,
                    'optimizer': optimizer.state_dict(),
                },
                is_best=is_best,
                filename=checkpoint_fn,
                cv_fold=cv_fold,
                use_mask=use_mask,
            )
    if use_crossval:
        holdout_loader = torch.utils.data.DataLoader(
            holdout_dataset,
            batch_size=args.batch_size, shuffle=False,
            num_workers=args.workers, pin_memory=True,
        )
        print("=> loading best model_{}__fold_{}_best.pth.tar".format(args.arch, cv_fold))
        checkpoint = torch.load("model_{}__fold_{}_best.pth.tar".format(args.arch, cv_fold))
        model.load_state_dict(checkpoint['state_dict'])
        print("Running forward pass on holdout set of size:", len(holdout_dataset.imgs))
        probs = get_probs(holdout_loader, model, args)
        np.save('model_{}__fold_{}__probs.npy'.format(args.arch, cv_fold), probs)

    def erase_in_display(self, how=0, *args, **kwargs):
        # dump the screen to history
        # check also https://github.com/selectel/pyte/pull/108

        if not self.alternate_buffer_mode and \
                (how == 2 or (how == 0 and self.cursor.x == 0 and self.cursor.y == 0)):
            self.push_lines_into_history()

        if how == 0:
            interval = range(self.cursor.y + 1, self.lines)
        elif how == 1:
            interval = range(self.cursor.y)
        elif how == 2 or how == 3:
            interval = range(self.lines)

        self.dirty.update(interval)
        for y in interval:
            line = self.buffer[y]
            for i, x in list(enumerate(line)):
                if i < self.columns:
                    line[x] = self.cursor.attrs
                else:
                    line.pop(x, None)

        if how == 0 or how == 1:
            self.erase_in_line(how)

        if how == 3:
            self.history.clear()
            self._clear_callback()