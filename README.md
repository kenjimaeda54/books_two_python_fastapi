# Motivação
Reforçar conceitos de fastapi para lidar com exceções e validações.


## Feature
- Aprendi a utilizar os principais recursos para lidar com validações como o Path, Query, Field
- Aprendi o uso do Pydantic para criar validações como abaixo.
- Aprendi também a demonstrar de forma padronizada os campos do swagger assim a pessoa ganha tempo com um modelo real que esperamos.

```python

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
    

```

##
- Toda vez que utilizo o modelo do Pydantic preciso fazer tipo um spread para transformar para o modelo do python como exemplo abaixo.
- Repara que recebo o BookRequest que é o gerenciado pelo Pydantic e depois converto para nosso modelo com o uso do asterisco.
- Sempre que recebo um BookRequest preciso fazer isso, se não ira falhar nas comparações. Por exemplo, no Put tentar comparar diretamente um modelo do python com o pydantic pelo id sempre irá resultar falha.

```python
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

@app.post("/books",status_code=status.HTTP_201_CREATED)
async  def create_book(book: BookRequest):
    new_book  = Book(**book.model_dump())
    BOOKS.append(
       find_book(new_book)
    )

```

##

- Aprendi a lançar exceções usando o raise e o HTTPException, como também aprendi a definir os padrões de retorno de sucesso. Existe um padrão no mercado exemplo 201 para create

```python

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


@app.get("/books",status_code= status.HTTP_200_OK)
async  def read_all_books():
    return BOOKS


```

##
- Para lidar com validações do PATH parâmetros usamos o PATH , tem que tomar cuidado em confundir ambos PATH com Query
- Abaixo estou validando que o book_id que é um path seja maior que 0, porque nosso id iniciam com 1

```python

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

```

##
- Para lidar com Query Parametros quais são os parâmetros após o ? Nós usamos a palavra Query

```python

@app.get("/books/return_by_rating",status_code=status.HTTP_200_OK)
async def read_by_rating(rating: int = Query(gt=0,lt=6)):
    return_book = []
    for book in BOOKS:
        if book.rating == rating:
           return_book.append(book)
    return return_book


```

## 
- Dicas de código para recuperar o último elemento de uma lista em python podem utilizar o -1
- Abaixo tem um exemplo do uso do ternário

```python

def find_book(book: Book):
    book.id = 0 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

```





