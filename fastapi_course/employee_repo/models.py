from pydantic import BaseModel
from typing import Optional

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    salary: float
    phone: Optional[str] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    salary: Optional[float] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None
