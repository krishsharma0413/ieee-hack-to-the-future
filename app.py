import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes.api import api_route
from routes.profile import profile_route
from routes.marketplace import marketplace_route
from routes.blog import blog_route
from routes.forum import forum_route
from core.token import Token
from core.coins import Coins

from core.marketplace import Marketplace
app = fastapi.FastAPI()

app.include_router(api_route)
app.include_router(marketplace_route)
app.include_router(profile_route)
app.include_router(blog_route)
app.include_router(forum_route)


app.mount("/static", StaticFiles(directory="./static"))
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: fastapi.Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: fastapi.Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup(request: fastapi.Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/newsletter", response_class=HTMLResponse)
async def newsletter(request: fastapi.Request):
    return templates.TemplateResponse(
        "alert-template.html",
        {
            "request": request,
            "emoji": "✅",
            "msg": "You have successfully subscribed to our newsletter.",
            "title": "THANK YOU!",
            "link": "/",
            "button_msg": "Return to Homepage",
            "bgcolor": "accent",
    })

@app.get("/about-us", response_class=HTMLResponse)
async def about_us(request: fastapi.Request):
    return templates.TemplateResponse("about-us.html", {"request": request})

@app.get("/thank-you", response_class=HTMLResponse)
async def thank_you(request: fastapi.Request):
    return templates.TemplateResponse(
        "done.html", {"request": request,}
    )
    
@app.get("/cart", response_class=HTMLResponse)
async def cart(request: fastapi.Request):
    if request.cookies.get("token"):
        tclass = Token(request.cookies.get("token"))
        await tclass.fit()
        if tclass.authentication:
            cart = await Marketplace.get_cart(tclass.token)
            return templates.TemplateResponse("cart.html", {"request": request, "cart": cart})
    return RedirectResponse("/")

@app.get("/new-password", response_class=HTMLResponse)
async def new_password(request: fastapi.Request):
    if request.cookies.get("token"):
        tclass = Token(request.cookies.get("token"))
        await tclass.fit()
        if tclass.authentication:
            return templates.TemplateResponse("newpassword.html", {"request": request})
    return RedirectResponse("/")

@app.get("/new-avatar", response_class=HTMLResponse)
async def new_avatar(request: fastapi.Request):
    if request.cookies.get("token"):
        tclass = Token(request.cookies.get("token"))
        await tclass.fit()
        if tclass.authentication:
            return templates.TemplateResponse("newavatar.html", {"request": request})
    return RedirectResponse("/")

@app.get("/no-coins", response_class=HTMLResponse)
async def no_coins(request: fastapi.Request):
    return templates.TemplateResponse(
        "alert-template.html",
        {
            "request": request,
            "emoji": "❌",
            "msg": "You either don't have the required amount of monthly tracking or your month average was more than the average of last 6 months.",
            "title": "OOPS!",
            "link": "/",
            "button_msg": "Return to Homepage",
            "bgcolor": "red-400",
    })
    
@app.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard(request: fastapi.Request):
    if request.cookies.get("token"):
        tclass = Token(request.cookies.get("token"))
        await tclass.fit()
        if tclass.authentication:
            
            leaderboard = await Coins(tclass.email).get_leaderboard()
            # add position
            for x in leaderboard:
                x['position'] = leaderboard.index(x)+1
            return templates.TemplateResponse(
                "leaderboard.html",
                {
                    "request": request,
                    "leaderboard": leaderboard
                }
            )
    return RedirectResponse("/")