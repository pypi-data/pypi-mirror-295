import inspect
import os



class exclusive:
    @staticmethod
    def file(func):
        def wrapper(*args,**kwargs):

            actual_func=func
            while hasattr(actual_func,"__func__"):
                actual_func=actual_func.__func__

            caller_filename=inspect.stack()[1].filename
            function_filename=inspect.getfile(actual_func)

            if not os.path.samefile(caller_filename,function_filename):
                raise RuntimeError("This function can only be used within the file it was defined in.")

            return func(*args,**kwargs)

        return wrapper


    @staticmethod
    def dir(func):
        def wrapper(*args,**kwargs):

            actual_func=func
            while hasattr(actual_func,"__func__"):
                actual_func=actual_func.__func__

            caller_filename=inspect.stack()[1].filename
            function_filename=inspect.getfile(actual_func)

            caller_directory=os.path.dirname(caller_filename)
            function_directory=os.path.dirname(function_filename)

            if not os.path.samefile(caller_directory,function_directory) and not os.path.samefile(caller_filename,function_filename):
                raise RuntimeError("This function can only be used within the directory it was defined in.")

            return func(*args,**kwargs)

        return wrapper


