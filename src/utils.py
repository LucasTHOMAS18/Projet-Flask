import os


def mkpath(p):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), p))
