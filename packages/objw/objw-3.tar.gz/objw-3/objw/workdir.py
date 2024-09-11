# This file is placed in the Public Domain.
# pylint: disable=C,I,R


"workdir"


import os
import pathlib


from objx import fqn


class Workdir:

    "Workdir"

    fqns = []
    wdr = ""


def long(name):
    "match from single name to long name."
    split = name.split(".")[-1].lower()
    res = name
    for names in types():
        if split == names.split(".")[-1].lower():
            res = names
            break
    return res


def skel():
    "create directory,"
    stor = os.path.join(Workdir.wdr, "store", "")
    path = pathlib.Path(stor)
    path.mkdir(parents=True, exist_ok=True)
    return path


def store(pth=""):
    "return objects directory."
    stor = os.path.join(Workdir.wdr, "store", "")
    if not os.path.exists(stor):
        skel()
    return os.path.join(Workdir.wdr, "store", pth)


def types():
    "return types stored."
    return os.listdir(store())


def whitelist(clz):
    "whitelist classes."
    Workdir.fqns.append(fqn(clz))


def __dir__():
    return (
        'Workdir',
        'long',
        'skel',
        'store',
        'types',
        'whitelist'
    )
