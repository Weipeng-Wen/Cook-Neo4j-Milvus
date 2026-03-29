# E:\Anaconda\envs\cook-rag\Scripts\uvicorn.exe cook-rag-graphRAG.test:app --reload

from fastapi import FastAPI, Form
from typing import Union
from pydantic import BaseModel, Field

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

class Item(BaseModel):
    name: str = Field(..., title="Item Name", max_length=100)
    description: Union[str, None] = Field(None, title="Item Description", max_length=300)
    price : float = Field(..., title="Item Price", gt=0)

@app.post("/items/")
def create_item(
    name: str = Form(...),
    description: Union[str, None] = Form(None),
    price: float = Form(...)
):
    item = Item(name=name, description=description, price=price)
    print(f"Server received data: {item}")
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)