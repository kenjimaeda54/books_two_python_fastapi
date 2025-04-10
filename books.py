from typing import Optional

import uvicorn
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel,Field
from starlette import status


app = FastAPI()

class Book:
    id: int
    description: str
    title: str
    rating: int
    author: str
    published_date: int


    def __init__(self,id,description,title,rating,author,published_date):
        self.id  = id
        self.description = description
        self.title = title
        self.rating = rating
        self.author = author
        self.published_date = published_date


class BookRequest(BaseModel):
    #description aparece no schema do boody do post
    id: Optional[int] = Field(description="Id don't need on create",default=None)
    description: str = Field(min_length=3,max_length=100)
    title: str = Field(min_length=1)
    rating: int = Field(gt=0,lt=6) #1 ate 5 . gt ==> maior, lt  ==> menor
    author: str = Field(min_length=1)
    published_date: int = Field(gt=1999,lt=2500)

    #dessa maneira vai aparecer como padrão no swager no body do post
    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Great description",
                "title": "Great title",
                "rating": 5,
                "author": "Great author",
                "published_date": 2012
            }
        }
    }


BOOKS = [
    Book(id= 1,description="Great Book",title="Answer book", rating=5,author="Great Author",published_date=2012),
    Book(id= 2,description="Book on life",title="Life", rating=3,author="Cameron",published_date=2015),
    Book(id= 3,description="Book is good",title="Good", rating=4,author="Lysa",published_date=2020),
    Book(id= 4,description="Example of good",title="Example", rating=4,author="Great good",published_date=2015),
]

@app.get("/books",status_code= status.HTTP_200_OK)
async  def read_all_books():
    return BOOKS

#com o path consigo validar o path parameters
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    #vou precisar usar uma variavel para saber se alterou
    is_success_change =  False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
           BOOKS.remove(BOOKS[i])
           is_success_change = True
           break
    if not is_success_change:
       raise HTTPException(status_code=404,detail="Item not found")

@app.get("/books/return_by_rating",status_code=status.HTTP_200_OK)
async def read_by_rating(rating: int = Query(gt=0,lt=6)):
    return_book = []
    for book in BOOKS:
        if book.rating == rating:
           return_book.append(book)
    return return_book

@app.get("/books/return_by_date",status_code=status.HTTP_200_OK)
async def read_by_published_date(published_date: int = Query(gt=1999,lt=2500)):
    return_published_date = []
    for book in BOOKS:
        if book.published_date == published_date:
            return_published_date.append(book)
    return  return_published_date

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_by_book_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id  == book_id:
            return book
    raise HTTPException(status_code=404,detail="Item not found")

@app.post("/books",status_code=status.HTTP_201_CREATED)
async  def create_book(book: BookRequest):
    new_book  = Book(**book.model_dump())
    BOOKS.append(
       find_book(new_book)
    )

@app.put("/books",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    is_success_change = False
    for i in  range(len(BOOKS)):
        if BOOKS[i].id == book.id:
           BOOKS[i] = Book(**book.model_dump())
           is_success_change = True
           break
    if not is_success_change:
        #raise é mesmo que o throw seria lançar uma excessão
        raise HTTPException(status_code=404,detail="Item not found")


# BOOKS[-1].id coom o [-1] estou pegando o ultimo Book da lista
# e como usar o leng - 1
def find_book(book: Book):
    book.id = 0 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)









