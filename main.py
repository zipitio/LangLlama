from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/story")
async def story(request: Request, language: str = Form(...), language_level: str = Form(...), article_topic: str = Form(...)):

    return templates.TemplateResponse("story.html",{
        "request": request,
        "language": language,
        "language_level": language_level,
        "article_topic": article_topic
    })
