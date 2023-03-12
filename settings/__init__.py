import os

ENVIRONMENT = os.getenv("ENVIRONMENT", None)

match ENVIRONMENT:
    case "local":
        from .local import *
    case _:
        from .default import *
