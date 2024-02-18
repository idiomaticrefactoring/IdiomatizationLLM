def patchify2d_cx(cx, w_in, w_out, k, *, bias=True):
    """Accumulates complexity of patchify2d into cx = (h, w, flops, params, acts)."""
    err_str = "Only kernel sizes divisible by the input size are supported."
    assert cx["h"] % k == 0 and cx["w"] % k == 0, err_str
    h, w, flops, params, acts = cx["h"], cx["w"], cx["flops"], cx["params"], cx["acts"]
    h, w = h // k, w // k
    flops += k * k * w_in * w_out * h * w + (w_out * h * w if bias else 0)
    params += k * k * w_in * w_out + (w_out if bias else 0)
    acts += w_out * h * w
    return {"h": h, "w": w, "flops": flops, "params": params, "acts": acts}