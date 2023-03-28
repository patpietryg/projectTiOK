# projectTiOK

Project - Code Testing And Optimalization

## Requirements
Python 3.10  
FastApi  
Uvicorn  
Requests

## Installation
1. Clone repo
```console
$ git clone git clone https://github.com/patpietryg/projectTiOK.git
$ cd projectTiOK

---> 100%
 ```

2. Create virtual environment
```console
$ python3 -m venv env
$ source env/bin/activate

---> 100%
 ```

3. Install required libreries

4. Start the server
```console
$ uvicorn app:app --reload

---> 100%
 ```
 
 ## Usage
  Open browser and activate your local server (ex. localhost:8000)
  
 Retrieve all blog posts
 ```console
http://localhost:8000/
 ```
 
 Retrieve a blog post by ID
  ```console
http://localhost:8000/post/{id}
 ```
 
## Testing

1. Run tests with 'unittest'
  ```console
$ python -m unittest discover
 ```
 
 #### Created by Patyczek
