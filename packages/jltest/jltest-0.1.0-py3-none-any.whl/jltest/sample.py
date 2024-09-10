import random

def some_func(func):
    print("#"+"I am ur new math teacher".center(50, "*")+"#")
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + random.randint(1, 10)
    return wrapper

@some_func
def add(a, b):
    return a + b

if __name__ == "__main__":
    
    print(add(10, 20))