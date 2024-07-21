import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from core.token import Token
from core.coins import Coins

from datetime import datetime
import pytz

profile_route = fastapi.APIRouter(prefix="/profile")
templates = Jinja2Templates("./templates")
ist = pytz.timezone("Asia/Kolkata")

mon = {
    1:"January",
    2:"February",
    3:"March",
    4:"April",
    5:"May",
    6:"June",
    7:"July",
    8:"August",
    9:"September",
    10:"October",
    11:"November",
    12:"December"
}

@profile_route.get("/@me", response_class=HTMLResponse)
async def profile_me(request: fastapi.Request):
    cookies = request.cookies
    if cookies.get("token"):
        tclass = Token(cookies["token"])
        await tclass.fit()
        if tclass.authentication:
            data = await Token.get_username(tclass.username)
            
            coinclass = Coins(tclass.email)
            consumption = await coinclass.get_months()
            consumption = consumption[-6:]
            currentmonth = datetime.now(ist).month
            
            months = [mon[currentmonth-1] for y,x in enumerate(consumption[::-1])]
            
            coinclass = Coins(tclass.email)
            totalcoins = await coinclass.get_coins()
            
            if data:
                return templates.TemplateResponse(
                    "profile-me.html",
                    context={
                        "request": request,
                        "x":data,
                        "consumption": str(consumption),
                        "months": str(months),
                        "coins": totalcoins
                    }
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