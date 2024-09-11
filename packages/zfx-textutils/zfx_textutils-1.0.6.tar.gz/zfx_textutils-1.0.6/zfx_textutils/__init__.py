from pkgutil import iter_modules
import importlib
import os

__all__ = []

# 确保在当前包路径下
current_dir = os.path.dirname(__file__)

# 打印当前包路径以确认
print("Package path:", current_dir)

# 自动导入当前包中的所有模块
for module_info in iter_modules([current_dir]):
    module_name = module_info.name
    if module_name != '__init__':
        # 打印发现的模块名以进行调试
        print("Found module:", module_name)
        # 动态导入
        try:
            imported_module = importlib.import_module(f'.{module_name}', package=__name__)
            globals()[module_name] = imported_module
            __all__.append(module_name)
        except Exception as e:
            print(f"Error importing {module_name}: {e}")

# 打印 __all__ 列表以确认
print("__all__ list:", __all__)
