from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def get_comments_count(post_id):
    url = f"https://jsonplaceholder.typicode.com/comments?postId={post_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        comments = response.json()
        return len(comments)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching comments for post {post_id}: {e}")
        return 0
    except ValueError as e:
        print(f"Error parsing comments response for post {post_id}: {e}")
        return 0

@app.get("/")
async def read_root(request: Request, page: int = 1, body_length_min: int = None, body_length_max: int = None, search: str = None):
    url = f"https://jsonplaceholder.typicode.com/posts?_page={page}&_limit=10"
    if search:
        url += f"&q={search}"
    response = requests.get(url)
    posts = response.json()
    total_count = int(response.headers["x-total-count"])
    total_pages = (total_count + 9) // 10
    for post in posts:
        post["comments_count"] = get_comments_count(post["id"])
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts, "total_pages": total_pages, "current_page": page})

@app.get("/posts")
def get_posts(request: Request):
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    return templates.TemplateResponse("posts.html", {'request':request, 'context':response.json()})


@app.get("/post/{id}")
def get_posts(request: Request, id: str):
    url = "https://jsonplaceholder.typicode.com/posts/"+id
    response = requests.get(url)
    #return response.json()
    return templates.TemplateResponse("post.html", {'request':request, 'context':response.json()})


@app.get("/comments")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/comments"
    response = requests.get(url)
    print(response.json())
    slownik=list(response.json())[:10]
    print(slownik[0])
    return response.json()


@app.get("/users")
def get_posts():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)