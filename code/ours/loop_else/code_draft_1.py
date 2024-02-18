for op in ops:
    all_outputs_reached = True
    for out in output_feature_names:
        if out not in outputs_encountered:
            all_outputs_reached = False
            break
    if all_outputs_reached:
        break
    if op.type not in _ops_to_layers._OP_REGISTRY and \
            op.type not in unsupported_op_types and \
            op.name not in skip_ops:
        unsupported_op_types.append(op.type)
    for out in op.outputs:
        outputs_encountered[out.name] = True
if len(unsupported_op_types) > 0:
    raise NotImplementedError("Unsupported Ops of type: %s" % (
        ','.join(unsupported_op_types)))