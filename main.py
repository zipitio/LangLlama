from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import aiprompting

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/story")
async def story(request: Request, language: str = Form(...), language_level: str = Form(...), article_topic: str = Form(...)):
    ai_story = aiprompting.prompt_ai(language, language_level, article_topic)
    print(ai_story)
    story_list = ai_story.split("*")
    print(story_list)
    story_title = story_list.pop(0)
    return templates.TemplateResponse("story.html",{
        "request": request,
        "language": language,
        "language_level": language_level,
        "article_topic": article_topic,
        "story_title": story_title,
        "story_list": story_list
    })
