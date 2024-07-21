import fastapi
from fastapi.responses import HTMLResponse, RedirectResponse
from core.token import Token
from fastapi.templating import Jinja2Templates
from core.marketplace import Marketplace

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
            products = await Marketplace.get_all_products()
            
            print(products)
            return templates.TemplateResponse(
                "marketplace.html",
                {
                    "request": request,
                    "products": products
                }
            )            

@marketplace_route.get("/{product_id}", response_class=HTMLResponse)
async def product_page(request:fastapi.Request, product_id:str):
    token = request.cookies.get("token")
    
    if token is None:
        return RedirectResponse(url="/login")
    else:
        tclass = Token(token)
        await tclass.fit()
        if tclass.authentication:
            product = await Marketplace(product_id).get_product()
            print(product)
            return templates.TemplateResponse(
                "product-page.html",
                {
                    "request": request,
                    "product": product
                }
            )