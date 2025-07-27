from fastapi import FastAPI,Body
from typing import Optional
app = FastAPI()

books = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "category": "Fiction"
    },
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "category": "Science"
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "category": "Dystopia"
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Philosophical Fiction"
    },
    {
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Programming"
    }
]

                                       ##### POST REQUESTS #####

@app.post("/books/create_book")
async def create_body(new_book : dict = Body()):
    books.append(new_book)
    return {"message" : "Book Successfully Created" , "Book": new_book}


@app.post("/books/upload_many")
async def upload_books(new_books: list[dict] = Body(...)):
    
    for book in new_books:
        if not all(k in book for k in ("title", "author", "category")):
            return {"error": "Each book must have 'title', 'author', and 'category'"}
        books.append(book)

    return {"message": f"{len(new_books)} books added successfully", "books": new_books}



                                     ##### GET REQUESTS #####
                                     
@app.get('')                                     
@app.get("/books/{author}")
async def get_books_by_author(author:str):
    book = []
    for i in books:
        if i.get('author').casefold() == author.casefold():
            book.append(i)
    
    return book if book else {'message' : f'books from {author} are unavailable'}

@app.get("/books/")
async def read_books_by_query(author: Optional[str] = None,\
    category: Optional[str] = None, title: Optional[str] = None):
    queried_books = []
    for book in books:
        if author and book.get('author', '').casefold() != author.casefold():
            continue
        if category and book.get('category', '').casefold() != category.casefold():
            continue
        if title and book.get('title', '').casefold() != title.casefold():
            continue
        queried_books.append(book)

    return queried_books if queried_books else {"error": "No books \
        found matching your query"} 


@app.get("/books")
async def get_books():
        return books


@app.get("/books/fav_book")
async def get_facourite_book():
    return {"favourite_book": "Best Book Ever"}


@app.get("/books/{dyn_param}")
async def read_book_by_parameter(dyn_param):
    return {"dynamic_parameter": dyn_param}





                              ##### PUT REQUESTS #####


#used to work in the older versions of fastAPI, but it returns error code 422 which shows Validation Error
@app.put("/books/update_book")
async def update_book(update_book : dict = Body(...)):
    for i in range(len(books)):
        if books[i].get('title').casefold() == update_book.get('title').casefold():
            books[i] = update_book
            return {"message": "Book updated successfully", "book": books[i]}

 
                                   ###Delete Requests###
                            
@app.delete("/books/delete_books/{title}")
async def delete_book_by_title(title : str):
    for i in range(len(books)):
        if books[i].get('title').casefold() == title.casefold():
            del books[i]
            return {"message":f"book {title} deleted successfully"}
