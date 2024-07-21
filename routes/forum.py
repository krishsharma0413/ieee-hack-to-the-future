import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.forum import Forum
from core.token import Token

forum_route = fastapi.APIRouter(prefix="/forum")
templates = Jinja2Templates(directory="templates")

@forum_route.get("/", response_class=HTMLResponse)
async def forum_root(request: fastapi.Request):
    
    if request.cookies.get("token"):
        tclass = Token(request.cookies.get("token"))
        await tclass.fit()
        if not tclass.authentication:
            return fastapi.responses.RedirectResponse("/login", status_code=303)
    else:
        return fastapi.responses.RedirectResponse("/login", status_code=303)
    
    forums = await Forum.get_all_forums()
    return templates.TemplateResponse(
        "forum-homepage.html",
        {
            "request": request,
            "forums": forums
        })

@forum_route.get("/{forum_id}", response_class=HTMLResponse)
async def forum_page(request: fastapi.Request, forum_id:str):
    
    forum = await Forum.get_forum_by_id(forum_id)


    
    if forum:
        profile = await Token.get_email(forum["author"])
        profile = profile["username"]
        
        replies = await Forum.get_replies_by_forum_id(forum_id)
        for reply in replies:
            profile = await Token.get_email(reply["author"])
            reply["name"] = profile["fullname"]
            reply["avatar"] = profile["avatar"]
        
        return templates.TemplateResponse(
            "forum-page.html",
            {
                "request": request,
                "title": forum["title"],
                "description": forum["description"].replace("\n", "<br>"),
                "author": forum["name"],
                "profile": profile,
                "forum_id": forum_id,
                "replies": replies
            })
    else:
        return fastapi.responses.RedirectResponse("/forum", status_code=303)
    
    