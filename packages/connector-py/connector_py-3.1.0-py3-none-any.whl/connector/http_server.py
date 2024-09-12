from connector.helpers import collect_methods
from connector.integration import Integration
from connector.oai.integration import Integration as OpenApiIntegration


def collect_routes(obj: object):
    """
    Collect all methods from an object and create a route for each.
    """
    from fastapi import APIRouter

    router = APIRouter()
    commands = collect_methods(obj)
    for method in commands:
        router.add_api_route(f"/{method.__name__.replace('_', '-')}", method, methods=["POST"])
    return router


def collect_integration_routes(
    integration: Integration | OpenApiIntegration,
    prefix_app_id: bool = False,
):
    """Create API endpoint for each method in integration."""
    from fastapi import APIRouter

    router = APIRouter()
    for capability_name, capability in integration.capabilities.items():
        prefix = f"/{integration.app_id}" if prefix_app_id else ""
        # replace `-` in prefix (e.g. app_id) and capability name
        route = f"{prefix}/{capability_name.value}".replace("-", "_")
        router.add_api_route(route, capability, methods=["POST"])

    return router


def runserver(router, port: int):
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)

    uvicorn.run(app, port=port)
