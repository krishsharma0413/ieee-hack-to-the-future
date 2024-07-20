import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from core.crud import validate_login
from core.token import Token
from fastapi.templating import Jinja2Templates

marketplace_route = fastapi.APIRouter(prefix="/marketplace")

templates = Jinja2Templates(directory="templates")

@marketplace_route.get("/", response_class=RedirectResponse)
async def marketplace_home(request:fastapi.Request, ):
    token = request.cookies.get("token")
    
    if token is None:
        return RedirectResponse(url="/login")
    else:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            
            
            
            return templates.TemplateResponse("marketplace.html", {"request": request})