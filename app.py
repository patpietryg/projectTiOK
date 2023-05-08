from fastapi import FastAPI, Request
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
favicon_path = 'favicon.ico'

templates = Jinja2Templates(directory="templates")

@app.get('/favicon.ico', include_in_schema=False)
def get_favicon():
    return FileResponse(favicon_path)


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
async def read_root(request: Request, page: int = 1, search: str = ""):
    url = f"https://jsonplaceholder.typicode.com/posts?_page={page}&_limit=10"
    if search:
        url += f"&q={search}"
    response = requests.get(url)
    posts = response.json()
    total_count = int(response.headers["x-total-count"])
    total_pages = (total_count + 9) // 10
    for post in posts:
        post["comments_count"] = get_comments_count(post["id"])
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts, "total_pages": total_pages, "current_page": page, "xyz": search})


@app.get("/post/{id}")
def get_post(request: Request, id: str):
    post_url = f"https://jsonplaceholder.typicode.com/posts/{id}"
    comments_url = f"https://jsonplaceholder.typicode.com/comments?postId={id}"

    post_response = requests.get(post_url)
    if post_response.status_code == 404:
        return JSONResponse(status_code=404, content='Invalid post id')
    post = post_response.json()

    try:
        user_id = post.get('userId')
        user_url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
        user_response = requests.get(user_url)
        user = user_response.json()
    except (requests.exceptions.RequestException, ValueError, KeyError) as e:
        print(f"Error fetching user for post {id}: {e}")
        user = {}

    comments_response = requests.get(comments_url)
    comments = comments_response.json()

    return templates.TemplateResponse("post.html",
                                      {'request': request, 'post': post, 'comments': comments, 'user': user})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)

