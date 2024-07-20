import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes.api import api_route
from routes.profile import profile_route
from routes.marketplace import marketplace_route
from routes.blog import blog_route

import pytz

ist = pytz.timezone("Asia/Kolkata")

app = fastapi.FastAPI()

app.include_router(api_route)
app.include_router(marketplace_route)
app.include_router(profile_route)
app.include_router(blog_route)


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