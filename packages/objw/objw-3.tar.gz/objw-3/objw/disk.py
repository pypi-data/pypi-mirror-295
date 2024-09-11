# This file is placed in the Public Domain.
# pylint: disable=C,I,R,W0105


"disk"


import datetime
import os
import pathlib
import _thread


from objx import dump, fqn, load, update


from .workdir import store


lock = _thread.allocate_lock()
disklock = _thread.allocate_lock()


"utilities"


def cdir(pth):
    "create directory."
    path = pathlib.Path(pth)
    path.parent.mkdir(parents=True, exist_ok=True)


def ident(obj):
    "return an id for an object."
    return os.path.join(fqn(obj), *str(datetime.datetime.now()).split())


"methods"


def fetch(obj, pth):
    "read object from disk."
    with disklock:
        pth2 = store(pth)
        read(obj, pth2)
        return os.sep.join(pth.split(os.sep)[-3:])


def read(obj, pth):
    "read an object from file path."
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def sync(obj, pth=None):
    "sync object to disk."
    with disklock:
        if pth is None:
            pth = ident(obj)
        pth2 = store(pth)
        write(obj, pth2)
        return pth


def write(obj, pth):
    "write an object to disk."
    with lock:
        cdir(pth)
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile, indent=4)


def __dir__():
    return (
        'fetch',
        'read',
        'sync',
        'write'
    )
