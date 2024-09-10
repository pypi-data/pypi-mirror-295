#装饰器
import time
import traceback


class decorator:
    #显示异常装饰器，很多时候有些过程无法显示异常内容，比方说pyqt5 ，所以说加个这个装饰器，就可以了
    @classmethod
    def ExceptionD(cls,f):
        def func_inner(*args, **kwargs):
            try:
                ret = f(*args, **kwargs)  # *代表打散
                return ret
            except Exception as E:
                print(E)

        return func_inner

    @classmethod
    def ExceptionD_desc(cls,f):
        def func_inner(*args, **kwargs):
            try:
                ret = f(*args, **kwargs)  # *代表打散
                return ret
            except Exception as E:
                traceback.print_exc()

        return func_inner

    @classmethod
    def ExceptionD_desc_sleep(cls,times = 1,*args,**kwargs):
        def func_out(f):
            def func_inner(*args, **kwargs):
                try:
                    ret = f(*args, **kwargs)  # *代表打散
                    return ret
                except Exception as E:
                    traceback.print_exc()
                    time.sleep(times)
            return func_inner
        return func_out