class Command:
    def __init__(self, func, description=None):
        self.func = func
        self.description = description

    def __call__(self, *args, **kwargs):
        self.func(*args, **kwargs)