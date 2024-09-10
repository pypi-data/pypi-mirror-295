
from .app import App
import inspect
from pydantic import create_model
from typing import Any, Dict
from fastapi import FastAPI
import uvicorn
from typing import Callable, get_type_hints
from .app import App

class Server:
    def __init__(self, app: App):
        self.app = app
        self.fastapi_app = FastAPI()
        self._setup()
        self._setup_routes()

    def _setup(self):
        if self.app.setup_fn:
            self.app.setup_fn()

    def _setup_routes(self):
        for name, method in self.app.api_endpoints.items():
            self._create_route(method)

    def _create_route(self, method: Callable):
        method_name = method.__name__
        signature = inspect.signature(method)
        parameters = signature.parameters

        # Create a Pydantic model for the request body
        fields = {}
        for name, param in parameters.items():
            if name == 'self':
                continue
            annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
            default = ... if param.default == inspect.Parameter.empty else param.default
            fields[name] = (annotation, default)

        BodyModel = create_model(f'{method_name.capitalize()}Body', **fields)
        response_type = get_type_hints(method)
        @self.fastapi_app.post(f"/{method_name}")
        async def endpoint(body: BodyModel):
            kwargs = body.dict()
            result = self.app.api_endpoints[method_name](**kwargs)
            return result
            # return {"result": result}

    def run(self, host: str = "0.0.0.0", port: int = 6006):
        @self.fastapi_app.get("/health")
        def health():
            return {"success":True}
        uvicorn.run(self.fastapi_app, host=host, port=port)
        

# Example usage:
# app = App("MyApp")
# server = Server(app)

# @server.api_endpoint("/hello")
# async def hello():
#     return {"message": "Hello, World!"}

# if __name__ == "__main__":
#     server.run()