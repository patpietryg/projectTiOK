from fastapi import FastAPI
import requests
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/posts")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return response.json()


@app.get("/posts/{id}")
def get_posts(id):
    url = "https://jsonplaceholder.typicode.com/posts/"+id
    response = requests.get(url)
    #return response.json()
    return templates.TemplateResponse("post.html", {"request": request, "id": id})


@app.get("/comments")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/comments"
    response = requests.get(url)
    slownik=list(response.json())[:10]
    print(slownik[0]["body"])
    return response.json()


@app.get("/users")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)