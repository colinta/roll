class Result:
    class Ok:
        def __init__(self, val):
            self.val = val

    class Err:
        def __init__(self, err):
            self.err = err
