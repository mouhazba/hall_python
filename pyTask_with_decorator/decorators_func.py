import time


def check_role_user(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if role != "admin":
                    raise PermissionError("Access denied")
            else:
                func(*args, **kwargs)
                        
        return wrapper
    return decorator

def timing_x(func):
    def wrapper(*args, **kwargs):
        stat_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print(f"time execution of : {func.__name__} : {end_time - stat_time}")
                      
    return wrapper