import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from core.token import Token


profile_route = fastapi.APIRouter(prefix="/profile")
templates = Jinja2Templates("./templates")

@profile_route.get("/@me", response_class=HTMLResponse)
async def profile_me(request: fastapi.Request):
    cookies = request.cookies
    if cookies.get("token"):
        tclass = Token(cookies["token"])
        await tclass.fit()
        if tclass.authentication:
            data = await Token.get_username(tclass.username)
            if data:
                return templates.TemplateResponse(
                    "profile-me.html",
                    context={"request": request, "x":data}
                )
    return RedirectResponse("/")
    
@profile_route.get("/{username}", response_class=HTMLResponse)
async def profile_username(request: fastapi.Request, username:str):
    
    cookies = request.cookies
    if cookies.get("token"):
        tclass = Token(cookies["token"])
        await tclass.fit()
        if tclass.authentication:
            data = await Token.get_username(username)
            if data:
                return templates.TemplateResponse(
                    "profile.html",
                    context=
                    {
                        "request": request,
                        "x": data
                    }
                )
    return RedirectResponse("/")