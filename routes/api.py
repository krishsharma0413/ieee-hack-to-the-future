import fastapi
from fastapi.responses import RedirectResponse
from core.crud import validate_login
from core.token import Token
from core.crud import newsletter_collection, consumption_collection
from core.forum import Forum
from core.marketplace import Marketplace
from datetime import datetime
from core.coins import Coins
import pytz

ist = pytz.timezone("Asia/Kolkata")
api_route = fastapi.APIRouter(prefix="/api")

@api_route.get("/login", response_class=RedirectResponse)
async def api_login(request:fastapi.Request, email:str, password:str):
    data = await validate_login(email=email.strip().lower(), password=password)
    if isinstance(data, bool):
        return RedirectResponse("/login", status_code=302)
    elif isinstance(data, str):
        redirect = RedirectResponse("/", status_code=302)
        redirect.set_cookie("token", data, max_age=10000)
        return redirect
    
@api_route.get("/signup", response_class=RedirectResponse)
async def api_signup(request:fastapi.Request, fullname:str, email:str, password:str):
    data = await Token.add_user(email=email.strip().lower(), password=password, fullname=fullname)
    if isinstance(data, bool):
        return RedirectResponse("/signup", status_code=302)
    else:
        redirect = RedirectResponse("/")
        redirect.set_cookie("token", data, max_age=10000)
        return redirect

@api_route.get("/logout", response_class=RedirectResponse)
async def api_logout(request:fastapi.Request):
    redirect = RedirectResponse("/")
    redirect.delete_cookie("token")
    return redirect

@api_route.get("/newsletter", response_class=RedirectResponse)
async def api_newsletter(request:fastapi.Request, email:str):
    token = request.cookies.get("token")
    print(token)
    if token:
        data = await newsletter_collection.find_one({"_id":email.strip().lower()})
        if data:
            return RedirectResponse("/", status_code=302)
        else:
            await newsletter_collection.insert_one({"_id":email.strip().lower()})
            return RedirectResponse("/newsletter", status_code=302)
    else:
        return RedirectResponse("/", status_code=302)

@api_route.get("/create-post", response_class=RedirectResponse)
async def api_create_post(request:fastapi.Request, forumtitle:str, forumdesc:str):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            await Forum.create_forum(tclass.email, tclass.fullname, forumtitle, forumdesc)
            return RedirectResponse("/forum", status_code=302)
        else:
            return RedirectResponse("/", status_code=302)
    else:
        return RedirectResponse("/", status_code=302)
    
@api_route.get("/create-reply", response_class=RedirectResponse)
async def api_create_reply(request:fastapi.Request, forum_id:str, reply:str):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            await Forum.create_reply(forum_id, tclass.email, reply)
            return RedirectResponse(f"/forum/{forum_id}", status_code=302)
        else:
            return RedirectResponse("/", status_code=302)
    else:
        return RedirectResponse("/", status_code=302)
    
@api_route.get("/cart", response_class=RedirectResponse)
async def api_cart(request:fastapi.Request, product_id:str):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            await Marketplace.add_to_cart(product_id, tclass.token)
            return RedirectResponse("/cart", status_code=302)
        else:
            return RedirectResponse("/", status_code=302)
    else:
        return RedirectResponse("/", status_code=302)
    
@api_route.get("/buynow", response_class=RedirectResponse)
async def api_buynow(request:fastapi.Request):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            await Marketplace.buynow(tclass.token)
            return RedirectResponse("/thank-you", status_code=302)

    return RedirectResponse("/", status_code=302)

@api_route.get("/change-password", response_class=RedirectResponse)
async def api_change_password(request:fastapi.Request, password:str):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            data = await tclass.change_password(password)
            if data:
                return RedirectResponse("/profile/@me", status_code=302)
    return RedirectResponse("/", status_code=302)
    
@api_route.get("/change-avatar", response_class=RedirectResponse)
async def api_change_password(request:fastapi.Request, avatar:str):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            data = await tclass.change_avatar(avatar)
            if data:
                return RedirectResponse("/profile/@me", status_code=302)
    return RedirectResponse("/", status_code=302)


@api_route.get("/claim-coin", response_class=RedirectResponse)
async def api_claim_coin(request:fastapi.Request):
    token = request.cookies.get("token")
    if token:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            coinclass = Coins(tclass.email)
            avg = await coinclass.get_average()
            lastmonth = datetime.now(ist).month
            month = (await coinclass.get_months())[-1]
            lastclaim = await coinclass.get_last_claim()
            if month < avg and lastmonth != lastclaim:
                await coinclass.add_coins(15)
                await consumption_collection.update_one(
                    {
                        "_id":tclass.email
                    },
                    {
                        "$set":{
                            "last_claim":lastmonth
                        }
                    }
                )
                return RedirectResponse("/profile/@me", status_code=302)
    return RedirectResponse("/no-coins", status_code=302)