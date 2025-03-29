from fastapi import APIRouter, Request, Depends, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from ..database import supabase, SUPABASE_BUCKET, SUPABASE_URL
from ..models import EmployeeCreate, EmployeeUpdate
from ..forms import as_form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../employee_repo/templates")

@router.get("/", response_class=HTMLResponse)
async def read_employees(request: Request):
    """Get all employees."""
    response = supabase.table("employees").select("*").eq('is_active', True).execute()
    employees = response.data
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

@route.get("/add", response_class=HTMLResponse)
async def add_employee(request: Request):
    """Render the employee creation form."""
    return templates.TemplateResponse("add_employee.html", {"request": request})
@router.post("/add")
async def create_employee(request: Request
                          , employee: EmployeeCreate = Depends(as_form)
                          , image: UploadFile = File(None)):
    image_url = None
    # Handle the uploaded image
    if image and image.filename != "":
        image_file_name = f"{employee.first_name}_{employee.last_name}_{image.filename}"
        file_content = await image.read()
        response = supabase.storage.from_(SUPABASE_BUCKET).upload(image_file_name, file_content)
        if response.status_code == 200:
            # Get the public URL of the uploaded image
            image_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{image_file_name}"

        supabase.table("employees").insert({
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "email": employee.email,
            "phone": employee.phone,
            "address": employee.address,
            "image_url": image_url
        }).execute()

        return RedirectResponse(url="/", status_code=303)

