"""
This is effectively an interface to pint. These are scattered throughout
different codebases, and it might make sense to consolidate them here.

Currently we are using pint for units, we might consider other libraries that
hande units like:

    * pint
    * quantities
    * astropy
    * unyt

See [UnitTableComparison]_ for a table comparing some unit / quantity packages.

References:
    .. [UnTy17] https://github.com/yt-project/unyt/issues/17
    .. [UnTyCompare] https://unyt.readthedocs.io/en/latest/usage.html#working-with-code-that-uses-astropy-units
    .. [UnitTableComparison] https://socialcompare.com/en/comparison/python-units-quantities-packages
"""

try:
    from functools import cache
except ImportError:
    from ubelt import memoize as cache


__all__ = ['unit_registry', 'ureg']  # NOQA


@cache
def unit_registry():
    """
    A memoized unit registry

    Returns:
        pint.UnitRegistry
    """
    import pint
    ureg = pint.UnitRegistry()
    return ureg


class __module_property_definitions__:
    """
    experimental feature for handling module level properties.

    References:
        https://github.com/scientific-python/lazy-loader/issues/127
    """
    def __init__(self):
        self.names = {'ureg'}

    @property
    def ureg(self):
        return unit_registry()

__modprops__ = __module_property_definitions__()


def __getattr__(name):
    """
    Create a lazy properties for this module that gives quick access to the
    unit registery.
    """
    if name in __modprops__.names:
        return getattr(__modprops__, name)
    else:
        raise AttributeError(f'Module {__name__!r} has no attribute {name!r}')
