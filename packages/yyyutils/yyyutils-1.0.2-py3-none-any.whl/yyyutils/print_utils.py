import inspect
import builtins
from colorama import Fore, Style


# 保存原始的print函数


class PrintUtils:
    """
    自定义print函数，可以添加文件名、类名、函数名、行号、时间，以及是否使用红色绿色字体打印
    """
    original_print = print

    def __init__(self, add_line=True, add_file=False, add_class=False, add_func=False, add_time=False, red=False, green=False):
        # 是否添加文件名、类名、函数名、行号、时间，以及是否使用红色字体打印
        self.add_line = add_line
        self.add_file = add_file
        self.add_func = add_func
        self.add_time = add_time
        self.add_class = add_class
        self.red = red
        self.green = green
        self.__enable = True
        self.__replace_print(self.__all_print)

    @staticmethod
    def get_original_print():
        return PrintUtils.original_print

    def __all_print(self, *args, **kwargs):
        string = ""
        frame = inspect.currentframe().f_back

        if self.add_file:
            file_name = frame.f_code.co_filename
            string += f"F--{file_name}, "
        if self.add_class:
            class_name = frame.f_locals.get('self', None).__class__.__name__
            string += f"C--{class_name}, "
        if self.add_func:
            func_name = frame.f_code.co_name
            string += f"Fu--{func_name}, "
        if self.add_line:
            line_number = frame.f_lineno
            string += f"L--{line_number}, "
        if self.add_time:
            import time
            # 获取当前时间,时分秒
            now_time = time.strftime("%H:%M:%S", time.localtime())
            string += f"T--{now_time}, "
        # 把最后一个逗号改成冒号
        string = string[:-2] + "："
        if self.red:
            PrintUtils.original_print(Fore.RED, end="")
        elif self.green:
            PrintUtils.original_print(Fore.GREEN, end="")
        else:
            PrintUtils.original_print(Style.RESET_ALL, end='')
        if not self.add_time and not self.add_line and not self.add_file and not self.add_class and not self.add_func:
            string = ""
        PrintUtils.original_print(string, sep='', *args, **kwargs)

    def disable(self):
        self.__enable = False
        PrintUtils.original_print(Style.RESET_ALL, end='')
        self.__replace_print(PrintUtils.original_print)

    def enable(self):
        self.__enable = True
        self.__replace_print(self.__all_print)

    def __replace_print(self, func):
        # 替换print函数
        builtins.print = func


if __name__ == '__main__':
    pr = PrintUtils(add_line=False)
    op = PrintUtils.original_print
    pr.green = True
    print("hello")
    pr.green = False
    print("world")
