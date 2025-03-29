
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import employee_routes
from .auth import auth_middleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="./employee_repo/static"), name="static")

templates = Jinja2Templates(directory="./employee_repo/templates")

app.middleware("http")(auth_middleware)

app.include_router(employee_routes.router)