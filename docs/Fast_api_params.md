FastAPI has a few **main ways** to get input from a client:

1. **Path parameters** (like your `"/items/{item_id}"`)
2. **Query parameters** (`?skip=0&limit=10`)
3. **Request body** (JSON, form data, files, etc.)
4. **Headers**
5. **Cookies**
6. **Form fields**
7. **File uploads**
8. **Combination of all of the above**

I’ll walk you through each one with examples, starting from what you already have.

---

## 1. Path parameters

**What they are:**  
Values embedded in the URL path, part of the route definition.

Your example:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    db = load_database()
    items = db.get("items", {})
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

- `"/items/{item_id}"` means:  
  - Any URL like `/items/abc123` or `/items/42` will call this function.
  - The part in `{}` is extracted and passed to the parameter with the same name: `item_id`.
- The type annotation `item_id: str` tells FastAPI to **parse it as a string**.
  - You could also use `int`, `float`, etc.

**More examples:**

```python
@app.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

@app.get("/orders/{year}/{month}")
async def read_orders(year: int, month: int):
    return {"year": year, "month": month}
```

**With validation and metadata:**

```python
from fastapi import Path

@app.get("/products/{product_id}")
async def read_product(
    product_id: int = Path(..., ge=1, description="The ID must be >= 1")
):
    return {"product_id": product_id}
```

---

## 2. Query parameters

**What they are:**  
Values that appear **after `?` in the URL**, like:

- `GET /items?skip=0&limit=10&search=phone`

FastAPI automatically treats **any function parameter that is not a path, body, etc.** as a query parameter (by default).

```python
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10, search: str | None = None):
    return {"skip": skip, "limit": limit, "search": search}
```

- URL: `/items?skip=5&limit=20&search=laptop`
  - `skip = 5`
  - `limit = 20`
  - `search = "laptop"`

**With validation:**

```python
from fastapi import Query

@app.get("/items")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None, min_length=3, max_length=50)
):
    return {"skip": skip, "limit": limit, "search": search}
```

---

## 3. Request body (JSON / Pydantic models)

**What it is:**  
Data sent in the body of the request, usually as JSON, e.g.:

- `POST /items` with JSON body:
  ```json
  {
    "name": "Phone",
    "price": 500.0,
    "is_offer": false
  }
  ```

FastAPI uses **Pydantic models** to define and validate body data.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

@app.post("/items")
async def create_item(item: Item):
    # item is already validated and parsed
    return {"message": "Item created", "item": item}
```

- Here, `item` is a **body parameter**.
- FastAPI reads JSON body → validates it against `Item` → passes you a Python object.

**Multiple body parameters:**

```python
class User(BaseModel):
    username: str
    email: str

@app.post("/orders")
async def create_order(item: Item, user: User):
    return {"item": item, "user": user}
```

**Mixing body with query/path:**

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,                # path
    item: Item,                  # body (JSON)
    q: str | None = None         # query
):
    return {"item_id": item_id, "item": item, "q": q}
```

---

## 4. Headers

**What they are:**  
HTTP headers like `User-Agent`, `Authorization`, etc.

```python
from fastapi import Header

@app.get("/me")
async def read_me(user_agent: str | None = Header(None)):
    return {"user_agent": user_agent}
```

- Client sends header: `User-Agent: Mozilla/5.0`
- FastAPI passes it as the `user_agent` parameter.

**Example with custom header:**

```python
@app.get("/secure-data")
async def secure_data(x_api_key: str = Header(...)):
    # Requires header: X-API-Key: your-key
    return {"api_key_used": x_api_key}
```

Note: HTTP headers use `-` but Python variables use `_`. FastAPI maps them automatically.

---

## 5. Cookies

**What they are:**  
Values stored in browser cookies, sent with each request.

```python
from fastapi import Cookie

@app.get("/preferences")
async def read_prefs(session_id: str | None = Cookie(None)):
    return {"session_id": session_id}
```

- If the client has `session_id=abc123` in cookies, it will be passed.

---

## 6. Form data

**What it is:**  
Data sent as HTML form (`application/x-www-form-urlencoded` or `multipart/form-data`), often from normal `<form>` submissions.

```python
from fastapi import Form

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```

- Client sends form fields `username`, `password`.
- Useful for login pages or when not using JSON.

---

## 7. File uploads

**What they are:**  
Files sent via `multipart/form-data` (e.g., an image upload).

```python
from fastapi import File, UploadFile

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

- `UploadFile` gives you:
  - `filename`
  - `content_type`
  - async `read()`, `write()`, etc.

**Multiple files:**

```python
from typing import List

@app.post("/uploadfiles")
async def upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [f.filename for f in files]}
```

---

## 8. Dependency injection (inputs from other functions)

This is more advanced, but extremely powerful.  
You can define *dependencies* that themselves get data from path, query, headers, etc., and inject them into your path function.

```python
from fastapi import Depends

def common_params(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items")
async def read_items(commons: dict = Depends(common_params)):
    return commons

@app.get("/users")
async def read_users(commons: dict = Depends(common_params)):
    return commons
```

- Both `/items` and `/users` now share the same query params and logic.
- Dependencies themselves can use:
  - path params
  - query params
  - headers
  - etc.

---

## 9. How FastAPI decides where each input comes from

FastAPI uses **type annotation + parameter position + special helpers** to decide:

1. **Path parameters**  
   - If a parameter name appears in the path (`"/items/{item_id}"`) and in the function signature (`item_id: int`), it’s a path parameter.

2. **Body parameters**  
   - Any parameter that is **a Pydantic model** or declared explicitly using `Body(...)` is taken from the request body.

3. **Query parameters**  
   - Simple types (`int`, `str`, `bool`, etc.) that are **not path params** and **not declared as Form/File/Header/Cookie** become query parameters.

4. **Special helpers** override the default:
   - `Query(...)` → query param (with extra validation)
   - `Path(...)` → path param (with extra validation)
   - `Header(...)` → header
   - `Cookie(...)` → cookie
   - `Form(...)` → form field
   - `File(...)` → file upload
   - `Depends(...)` → dependency injection

---

## 10. Connecting back to your example

Your route:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    ...
```

- `item_id` is a **path parameter**.
- You could **add query params**:

  ```python
  @app.get("/items/{item_id}")
  async def read_item(
      item_id: str, 
      include_details: bool = False
  ):
      # Now /items/123?include_details=true
      ...
  ```

- Or add a **body** (for POST/PUT):

  ```python
  @app.put("/items/{item_id}")
  async def update_item(item_id: str, item: Item):
      # item is the JSON body
      ...
  ```

- Or add **headers**:

  ```python
  from fastapi import Header

  @app.get("/items/{item_id}")
  async def read_item(item_id: str, x_token: str = Header(...)):
      # Requires header X-Token
      ...
  ```

---

## Summary

FastAPI has **many ways to receive input**, but the core ideas are:

- **Path parameters**: inside `"/path/{param}"`, part of the URL.
- **Query parameters**: after `?` in the URL.
- **Body**: JSON (or other) content in the request body, usually using Pydantic models.
- **Headers, Cookies, Form, File**: explicitly declared with their helper functions.
- **Dependencies**: reusable pieces that can combine any of the above.

If you tell me what kind of data you want to accept in your app (e.g., “create items with JSON body plus an auth header and pagination”), I can write you a few complete FastAPI route examples tailored to that.