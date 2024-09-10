from typing import Callable
from functools import wraps

class App:
    def __init__(self, name: str) -> None:
        self.name = name
        self.setup_fn = None
        self.api_endpoints = {}
        self.instance = None

    def __call__(self, cls: type):
        print(f"App {self.name}")
        self.instance = cls()
        return cls
    
    def setup(self, func:Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.instance, *args, **kwargs)
        self.setup_fn = wrapper
        print(f"Setting {func.__name__} as a setup function")
        return func
    
    def api_endpoint(self, func:Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(self.instance, *args, **kwargs)
        self.api_endpoints[func.__name__] = wrapper
        return func
        
        