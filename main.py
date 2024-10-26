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

#pydantic used here for data validation
class TopicBase(BaseModel):
    topic_name: str
    genre: str

class UserBase(BaseModel):
    username: str

# Dependency to create and close sessions for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/topics/", status_code=status.HTTP_201_CREATED)
async def create_topic(topic: TopicBase, db: db_dependency):
    db_topic = models.Topic(**topic.dict())
    db.add(db_topic)
    db.commit()
    return db_topic.topic_name

@app.get("/topics/{topic_id}", status_code=status.HTTP_200_OK)
async def read_topic(topic_id: int, db: db_dependency):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@app.delete("/topics/{topic_id}", status_code=status.HTTP_200_OK)
async def delete_topic(topic_id: int, db: db_dependency):
    db_topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if db_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(db_topic)
    db.commit()

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

@app.delete("/users/", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(db_user)
    db.commit()

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
