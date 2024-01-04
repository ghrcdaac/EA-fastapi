def callWithNonNoneArgs(f, *args, **kwargs):
    kwargsNotNone = {k: v for k, v in kwargs.items() if v is not None}
    return f(*args, **kwargsNotNone)