import types
import packaging.version
import sys
import os
import importlib


class Version(packaging.version.Version):
    '''Extended implementation of packaging.version.Version'''

    def match(self, condition: str) -> bool:
        '''
        Determine whether the given condition are met
        Args:
            condition(str) : conditions for judgment
        Returns:
            bool: True if the given version condition are met, else False
        Examples:
            .. code-block:: python
                Version('1.2.0').match('>=1.2.0a')
        '''
        if not condition:
            return True
        if condition.startswith('>='):
            version = condition[2:]
            _comp = self.__ge__
        elif condition.startswith('>'):
            version = condition[1:]
            _comp = self.__gt__
        elif condition.startswith('<='):
            version = condition[2:]
            _comp = self.__le__
        elif condition.startswith('<'):
            version = condition[1:]
            _comp = self.__lt__
        elif condition.startswith('=='):
            version = condition[2:]
            _comp = self.__eq__
        elif condition.startswith('='):
            version = condition[1:]
            _comp = self.__eq__
        else:
            version = condition
            _comp = self.__eq__

        return _comp(Version(version))

    def __lt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__lt__(other)

    def __le__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__le__(other)

    def __gt__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__gt__(other)

    def __ge__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__ge__(other)

    def __eq__(self, other):
        if isinstance(other, str):
            other = Version(other)
        return super().__eq__(other)


def load_py_dir(python_dir: str):
    model_basename = os.path.basename(python_dir)
    spec = importlib.util.spec_from_file_location(
        model_basename, os.path.join(python_dir, '__init__.py'))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_py_module(python_path: str, py_module_name: str) -> types.ModuleType:
    '''
    Load the specified python module.

    Args:
        python_path(str) : The directory where the python module is located
        py_module_name(str) : Module name to be loaded
    '''
    sys.path.insert(0, python_path)

    # Delete the cache module to avoid hazards. For example, when the user reinstalls a HubModule,
    # if the cache is not cleared, then what the user gets at this time is actually the HubModule
    # before uninstallation, this can cause some strange problems, e.g, fail to load model parameters.
    if py_module_name in sys.modules:
        sys.modules.pop(py_module_name)

    py_module = importlib.import_module(py_module_name)
    sys.path.pop(0)

    return py_module
