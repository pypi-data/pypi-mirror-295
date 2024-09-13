NAME

::

    OBJW - objects workdir


SYNOPSIS

::

    >>> from objx import Object
    >>> from objw import Workdir, sync
    >>> Workdir.wdr = ".test"
    >>> o = Object()
    >>> sync(o)


INSTALL

::

    $ pip install objw


DESCRIPTION

::

    OBJX contains all the python3 code to program objects in a functional
    way. It provides a base Object class that has only dunder methods, all
    methods are factored out into functions with the objects as the first
    argument. It is called Object Programming (OP), OOP without the
    oriented.

    OBJX  allows for easy json save//load to/from disk of objects. It
    provides an "clean namespace" Object class that only has dunder
    methods, so the namespace is not cluttered with method names. This
    makes storing and reading to/from json possible.

    OBJW provides a persist store with the use of a directory on disk.


COPYRIGHT

::

    OBJW is Public Domain.
