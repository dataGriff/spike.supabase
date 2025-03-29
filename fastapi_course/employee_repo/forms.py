from fastapi import Form

def as_form(cls):
    def _as_form(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        salary: float = Form(...),
        phone: str = Form(None),
        address: str = Form(None),
        image_url: str = Form(None),
        is_active: bool = Form(True),
    ):
        return cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            salary=salary,
            phone=phone,
            address=address,
            image_url=image_url,
            is_active=is_active,
        )
    cls.as_form = _as_form
    return cls
