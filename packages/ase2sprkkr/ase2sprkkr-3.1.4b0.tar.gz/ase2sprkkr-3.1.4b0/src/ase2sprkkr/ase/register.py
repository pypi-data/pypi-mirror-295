import platformdirs
import os

registered = False


def user_preferences_file():
    """ Return filename with user preferences """
    return os.path.join(platformdirs.user_config_dir('ase2sprkkr', 'ase2sprkkr'), '__init__.py')


def load_user_preferences():
    """ Load user defined preferences from
        ``$HOME/.config/ase2sprkkr/__init__.py``
    """
    file = user_preferences_file()

    try:
       if os.path.isfile(file):
           import types
           import importlib.machinery
           loader = importlib.machinery.SourceFileLoader('ase2sprkkr.personal', file)
           mod = types.ModuleType(loader.name)
           loader.exec_module(mod)
    except Exception as e:
        import warnings
        warnings.warn(f'Can not import {file} file with the user preferences: \n{e}')


def register():
    global registered

    if registered:
        return

    # fallback to the old way
    else:
        from ase.calculators.calculator import register_calculator_class
        from ..sprkkr.calculator import SPRKKR  # NOQA: E402
        registered=True
        #register_calculator_class('sprkkr', SPRKKR)


try:

    def ase_register(plugin):
        global registered
        if registered:
            return
        registered = True
        plugin.register_calculator('ase2sprkkr.SPRKKR')
        plugin.register_io_format('ase2sprkkr.ase.io', 'SPRKKR potential file',
                            '1F', name='sprkkr', ext='pot')


except ImportError:

    pass
