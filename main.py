from fastapi import FastAPI, Request, Form, HTTPException, Depends, status
from fastapi.templating import Jinja2Templates
import aiprompting
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
# Create database tables
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

class TopicBase(BaseModel):
    topic_id: int
    topic_name: str
    genre: str

class UserBase(BaseModel):
    username: str
    #user_id: int

# Dependency to create and close sessions for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/topics/)", status_code=status.HTTP_201_CREATED)
async def create_topic(topic: TopicBase, db: db_dependency):
    db_topic = models.Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    return db_topic.topic_name

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user.username

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
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
