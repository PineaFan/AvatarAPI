from aiohttp import web
import os

routes = web.RouteTableDef()

def make_main(callback):
    async def predicate(request):
        args = request.query_string.split('&')
        argDict = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                argDict[key] = value
            else:
                argDict[arg] = True
        return web.Response(body=callback(**argDict))
    return predicate

# Register all files in /routes

for file in os.listdir("endpoints"):
    if file.endswith(".py"):
        file = file[:-3]
        if file != "__init__" and "__pycache__" not in file:
            # Get the "main" function and the "path" variable from the file
            module = __import__(f"endpoints.{file}", fromlist=["main", "path"])
            routes.get(f'/{module.path}')(make_main(module.main))

app = web.Application()
app.add_routes(routes)
web.run_app(app)
