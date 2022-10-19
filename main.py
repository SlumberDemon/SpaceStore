import deta
import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = fastapi.FastAPI()
apps = deta.Base("apps")

pages = Jinja2Templates(directory="pages")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=fastapi.responses.HTMLResponse)
async def home(request: fastapi.Request):
    res = apps.fetch()
    items = res.items
    while res.last:
        res = apps.fetch(last=res.last)
        items += res.items
    return pages.TemplateResponse("index.html", {"request": request, "items": items})


@app.post("/add")
async def add_app(name: str, version: str, icon: str, url: str):
    data = apps.put({"name": name, "version": version, "icon": icon, "url": url})
    return {"key": data["key"]}


@app.patch("/update")
async def update_app(key: str, name: str, version: str, icon: str, url: str):
    apps.update({"name": name, "version": version, "icon": icon, "url": url}, key)
    return {"key": key}
