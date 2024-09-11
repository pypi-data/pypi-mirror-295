from pkgutil import iter_modules
import importlib

__all__ = []

# 自动导入当前包中的所有模块
for module in iter_modules(__path__):
    module_name = module.name
    # 动态导入
    imported_module = importlib.import_module(f'.{module_name}', package=__name__)
    globals()[module_name] = imported_module
    __all__.append(module_name)
