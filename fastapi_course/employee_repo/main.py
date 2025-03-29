
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routes import employee_routes

app = FastAPI()

app.mount("/static", StaticFiles(directory="./employee_repo/static"), name="static")

templates = Jinja2Templates(directory="./employee_repo/templates")

app.include_router(employee_routes.router)