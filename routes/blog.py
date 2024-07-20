import fastapi
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from core.blogs import Blog

blog_route = fastapi.APIRouter(prefix="/blog")
templates = Jinja2Templates(directory="templates")

@blog_route.get("/", response_class=HTMLResponse)
async def blog(request: fastapi.Request):
    
    blogs = await Blog.get_all_blogs()
    
    blogs = sorted(blogs, key=lambda x:x["date"], reverse=True)
    
    return templates.TemplateResponse(
        "blog-homepage.html",
        {
            "request": request,
            "blogs": blogs
        })

@blog_route.get("/{blog_id}", response_class=HTMLResponse)
async def blog(request: fastapi.Request, blog_id:str):
    
    blog = await Blog.get_blog_by_id(blog_id)
    with open(f"{blog['path']}") as f:
        blog = f.read()
    if blog:
        return templates.TemplateResponse(
            "blog-page.html",
            {
                "request": request,
                "blog": blog
            })
    else:
        return fastapi.responses.RedirectResponse("/blog", status_code=303)
    
    