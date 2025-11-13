from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#creating FASTAPI app
app = FastAPI(title ="E2E Mini App")

# adding CORS middleware to let frontend call backend 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allowing all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Login model
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(req: LoginRequest):
    if req.username == "admin" and req.password == "fakepass":
        return{"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid Credentials")

#Health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

#item model
class Item(BaseModel):
    name: str
    price: float

#in-memory "database"
items_db = []
item_id_counter = 1

@app.post("/items")
def create_item(item: Item):
    global item_id_counter
    new_item = {"id":item_id_counter, "name": item.name, "price":item.price}
    items_db.append(new_item)
    item_id_counter += 1
    return new_item

@app.get("/items")
def list_items():
    return items_db

@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code = 404, detail = "Item not found")
