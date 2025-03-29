from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class EmployeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    salary: float
    phone: Optional[str] = None
    address: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = True

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...),
        image_url: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(True),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            salary=salary,
            image_url=image_url,
            is_active=is_active,
        )

class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    salary: Optional[float] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...),
        image_url: Optional[str] = Form(None),
        is_active: Optional[bool] = Form(True),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            salary=salary,
            image_url=image_url,
            is_active=is_active,
        )
