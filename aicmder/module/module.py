from typing import Callable
import inspect
from aicmder.utils.utils import load_py_module, Version, load_py_dir
import os
_module_serving_func = {}
_module_runnable_func = {}


class InvalidModule(Exception):
    def __init__(self, directory: str):
        self.directory = directory

    def __str__(self):
        return '{} is not a valid Module'.format(self.directory)


def runnable(func: Callable) -> Callable:
    '''Mark a Module method as runnable, when the command `hub run` is used, the method will be called.'''
    mod = func.__module__ + '.' + inspect.stack()[1][3]
    _module_runnable_func[mod] = func.__name__

    def _wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return _wrapper


def serving(func: Callable) -> Callable:
    '''Mark a Module method as serving method, when the command `hub serving` is used, the method will be called.'''
    mod = func.__module__ + '.' + inspect.stack()[1][3]
    _module_serving_func[mod] = func.__name__

    def _wrapper(*args, **kwargs):
        func_signature = inspect.signature(func)
        if len(func_signature.parameters) <= 1:
            print(args, kwargs)
            return func(*args)
        return func(*args, **kwargs)

    return _wrapper


class Module(object):
    '''
    In PaddleHub, Module represents an executable module, which usually a pre-trained model that can be used for end-to-end
    prediction, such as a face detection model or a lexical analysis model, or a pre-trained model that requires finetuning,
    such as BERT/ERNIE. When loading a Module with a specified name, if the Module does not exist locally, PaddleHub will
    automatically request the server or the specified Git source to download the resource.

    Args:
        name(str): Module name.
        directory(str|optional): Directory of the module to be loaded, only takes effect when the `name` is not specified.
        version(str|optional): The version limit of the module, only takes effect when the `name` is specified. When the local
                               Module does not meet the specified version conditions, PaddleHub will re-request the server to
                               download the appropriate Module. Default to None, This means that the local Module will be used.
                               If the Module does not exist, PaddleHub will download the latest version available from the
                               server according to the usage environment.
        source(str|optional): Url of a git repository. If this parameter is specified, PaddleHub will no longer download the
                              specified Module from the default server, but will look for it in the specified repository.
                              Default to None.
        update(bool|optional): Whether to update the locally cached git repository, only takes effect when the `source`
                               is specified. Default to False.
        branch(str|optional): The branch of the specified git repository. Default to None.
    '''

    def __init__(self, **kwargs) -> None:
        pass

    def __new__(cls,
                *,
                name: str = None,
                directory: str = None,
                version: str = None,
                source: str = None,
                update: bool = False,
                branch: str = None,
                **kwargs):
        if cls.__name__ == 'Module':
            # from paddlehub.server.server import CacheUpdater
            # This branch come from hub.Module(name='xxx') or hub.Module(directory='xxx')
            if name:
                module = cls.init_with_name(
                    name=name, version=version, source=source, update=update, branch=branch, **kwargs)
                # CacheUpdater("update_cache", module=name, version=version).start()
            elif directory:
                module = cls.init_with_directory(directory=directory, **kwargs)
                # CacheUpdater("update_cache", module=directory, version="0.0.0").start()
        else:
            module = object.__new__(cls)

        return module

    def _get_func_name(self, current_cls, module_func_dict: dict):
        mod = current_cls.__module__ + '.' + current_cls.__name__
        if mod in module_func_dict:
            _func_name = module_func_dict[mod]
            return _func_name
        elif current_cls.__bases__:
            for base_class in current_cls.__bases__:
                base_run_func = self._get_func_name(base_class, module_func_dict)
                if base_run_func:
                    return base_run_func
        else:
            return None

    @property
    def serving_func_name(self):
        return self._get_func_name(self.__class__, _module_serving_func)

    @classmethod
    def load(cls, directory: str):
        '''Load the Module object defined in the specified directory.'''
        if directory.endswith(os.sep):
            directory = directory[:-1]

        # try:
        #     # check class exists or not
        #     py_module = eval(directory)()
        # except:
        basename = os.path.basename(directory)
        dirname = os.path.dirname(directory)
        load_py_dir(os.path.join(os.getcwd(), dirname))
        py_module = load_py_module(dirname, basename)

        for _item, _cls in inspect.getmembers(py_module, inspect.isclass):
            _item = py_module.__dict__[_item]
            if hasattr(_item, '_hook_by_cmder') and issubclass(_item, Module) and _item.__module__ in directory:
                user_module_cls = _item
                break
        else:
            raise InvalidModule(directory)

        user_module_cls.directory = directory

        # source_info_file = os.path.join(directory, '_source_info.yaml')
        # if os.path.exists(source_info_file):
        #     info = parser.yaml_parser.parse(source_info_file)
        #     user_module_cls.source = info.get('source', '')
        #     user_module_cls.branch = info.get('branch', '')
        # else:
        #     user_module_cls.source = ''
        #     user_module_cls.branch = ''

        # # In the case of multiple cards, the following code can set each process to use the correct place.
        # if issubclass(user_module_cls, paddle.nn.Layer):
        #     place = paddle.get_device().split(':')[0]
        #     paddle.set_device(place)

        return user_module_cls

    @classmethod
    def init_with_name(cls,
                       name: str,
                       version: str = None,
                       source: str = None,
                       update: bool = False,
                       branch: str = None,
                       **kwargs):
        '''Initialize Module according to the specified name.'''
        # from paddlehub.module.manager import LocalModuleManager
        # manager = LocalModuleManager()
        # user_module_cls = manager.search(name, source=source, branch=branch)
        # if not user_module_cls or not user_module_cls.version.match(version):
        #     user_module_cls = manager.install(
        #         name=name, version=version, source=source, update=update, branch=branch)

        # directory = manager._get_normalized_path(user_module_cls.name)

        # # The HubModule in the old version will use the _initialize method to initialize,
        # # this function will be obsolete in a future version
        # if hasattr(user_module_cls, '_initialize'):
        #     log.logger.warning(
        #         'The _initialize method in HubModule will soon be deprecated, you can use the __init__() to handle the initialization of the object'
        #     )
        #     user_module = user_module_cls(directory=directory)
        #     user_module._initialize(**kwargs)
        #     return user_module

        # if issubclass(user_module_cls, ModuleV1):
        #     return user_module_cls(directory=directory, **kwargs)

        # user_module_cls.directory = directory
        user_module_cls = cls.load(name)
        return user_module_cls(**kwargs)


def moduleinfo(name: str = '',
               version: str = '1.0',
               author: str = None,
               author_email: str = None,
               summary: str = None,
               type: str = None,
               meta=None) -> Callable:
    '''
    Mark Module information for a python class, and the class will automatically be extended to inherit HubModule. In other words, python classes
    marked with moduleinfo can be loaded through hub.Module.
    '''

    def _wrapper(cls):
        wrap_cls = cls
        _meta = Module if not meta else meta
        if not issubclass(cls, _meta):
            _bases = []
            for _b in cls.__bases__:
                if issubclass(_meta, _b):
                    continue
                _bases.append(_b)
            _bases.append(_meta)
            _bases = tuple(_bases)
            wrap_cls = builtins.type(cls.__name__, _bases, dict(cls.__dict__))

        wrap_cls.name = name
        wrap_cls.version = Version(version)
        wrap_cls.author = author
        wrap_cls.author_email = author_email
        wrap_cls.summary = summary
        wrap_cls.type = type
        wrap_cls._hook_by_cmder = True
        return wrap_cls

    return _wrapper
