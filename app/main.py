from fastapi import FastAPI
from app.routers import permission
from app.routers import auth
from app.routers.category import router as category_router
from app.routers.products import router as products_router
from app.routers.review import router as review_router
from app.routers.example import router as example_router
# from loguru import logger
# from uuid import uuid4
from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
from .log import log_middleware


# logger.add("info.log", format="Log: [{extra[log_id]}:{time} - {level} - {message}]", level="INFO", enqueue = True)

app = FastAPI()

app_v1 = FastAPI()
app_v2 = FastAPI()

app.middleware("http")(log_middleware)

#
# @app.middleware("http")
# async def log_middleware(request: Request, call_next):
#     log_id = str(uuid4())
#     with logger.contextualize(log_id=log_id):
#         try:
#             response = await call_next(request)
#             if response.status_code in [401, 402, 403, 404]:
#                 logger.warning(f"Request to {request.url.path} failed")
#             else:
#                 logger.info('Successfully accessed ' + request.url.path)
#         except Exception as ex:
#             logger.error(f"Request to {request.url.path} failed: {ex}")
#             response = JSONResponse(content={"success": False}, status_code=500)
#         return response


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app_v1.include_router(category_router)
app_v1.include_router(products_router)
app_v1.include_router(auth.router)
app_v1.include_router(permission.router)
app_v1.include_router(review_router)

app_v2.include_router(example_router)


app.mount('/api/v1', app_v1)
app.mount('/api/v2', app_v2)