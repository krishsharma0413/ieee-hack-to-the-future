import fastapi
from fastapi.responses import JSONResponse, RedirectResponse
from core.crud import validate_login
from hashlib import sha256
from core.token import Token

api_route = fastapi.APIRouter(prefix="/api")

@api_route.get("/login", response_class=RedirectResponse)
async def api_login(request:fastapi.Request, email:str, password:str):
    data = await validate_login(email=email.strip().lower(), password=password)
    if isinstance(data, bool):
        return RedirectResponse("/", status_code=302)
    elif isinstance(data, str):
        redirect = RedirectResponse("/", status_code=302)
        redirect.set_cookie("token", data, max_age=10000)
        return redirect
    
@api_route.get("/signup", response_class=RedirectResponse)
async def api_signup(request:fastapi.Request, fullname:str, email:str, password:str):
    data = await Token.add_user(email=email.strip().lower(), password=password, fullname=fullname)
    if isinstance(data, bool):
        return RedirectResponse("/")
    else:
        redirect = RedirectResponse("/")
        redirect.set_cookie("token", data, max_age=10000)
        return redirect

@api_route.get("/logout", response_class=RedirectResponse)
async def api_logout(request:fastapi.Request):
    redirect = RedirectResponse("/")
    redirect.delete_cookie("token")
    return redirect
