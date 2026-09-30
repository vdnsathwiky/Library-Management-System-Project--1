from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "books.json"
initial_books = [
    {"book_id": "B001", "title": "Python Crash Course", "author": "Eric Matthes", "available": True, "borrower": ""},
    {"book_id": "B002", "title": "Clean Code", "author": "Robert C. Martin", "available": True, "borrower": ""},
    {"book_id": "B003", "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "available": True, "borrower": ""},
    {"book_id": "B004", "title": "Fluent Python", "author": "Luciano Ramalho", "available": True, "borrower": ""},
    {"book_id": "B005", "title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "available": True, "borrower": ""}
]
def save_books(book_list):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(book_list, file, indent=4)

def load_books():
    if not os.path.exists(DATA_FILE):
        save_books(initial_books)
        return initial_books.copy()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    save_books(initial_books)
    return initial_books.copy()

books = load_books()
def find_book(book_id):
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/books")
def view_books():
    message = request.args.get("message")
    message_type = request.args.get("message_type", "success")
    return render_template(
        "books.html",
        books=books,
        message=message,
        message_type=message_type
    )

@app.route("/book/<book_id>")
def book_details(book_id):
    book = find_book(book_id)

    if book is None:
        return redirect(url_for(
            "view_books",
            message="Book ID does not exist.",
            message_type="error"
        ))
    return render_template("book_details.html", book=book)

@app.route("/add-book", methods=["GET", "POST"])
def add_book():
    message = None
    message_type = None
    if request.method == "POST":
        book_id = request.form.get("book_id", "").strip()
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        if book_id == "" or title == "" or author == "":
            message = "Book ID, title, and author are required."
            message_type = "error"
        elif find_book(book_id) is not None:
            message = "Book ID already exists."
            message_type = "error"
        else:
            new_book = {
                "book_id": book_id,
                "title": title,
                "author": author,
                "available": True,
                "borrower": ""
            }
            books.append(new_book)
            save_books(books)
            message = "Book added successfully."
            message_type = "success"
    return render_template(
        "add_book.html",
        message=message,
        message_type=message_type
    )

@app.route("/search", methods=["GET", "POST"])
def search_books():
    search_text = ""
    results = []
    searched = False
    if request.method == "POST":
        search_text = request.form.get("search", "").strip()
        searched = True
        for book in books:
            if (search_text.lower() in book["title"].lower()
                    or search_text.lower() in book["author"].lower()):
                results.append(book)
    return render_template(
        "search.html",
        results=results,
        search_text=search_text,
        searched=searched
    )

@app.route("/issue/<book_id>", methods=["GET", "POST"])
def issue_book(book_id):
    book = find_book(book_id)
    if book is None:
        return redirect(url_for(
            "view_books",
            message="Book ID does not exist.",
            message_type="error"
        ))
    if book["available"] is False:
        return redirect(url_for(
            "view_books",
            message="Book is already issued.",
            message_type="error"
        ))
    if request.method == "POST":
        borrower = request.form.get("borrower", "").strip()
        if borrower == "":
            return render_template(
                "issue_book.html",
                book=book,
                message="Borrower name is required.",
                message_type="error"
            )
        book["available"] = False
        book["borrower"] = borrower
        save_books(books)
        return redirect(url_for(
            "view_books",
            message="Book issued successfully.",
            message_type="success"
        ))
    return render_template(
        "issue_book.html",
        book=book,
        message=None,
        message_type=None
    )

@app.route("/return/<book_id>")
def return_book(book_id):
    book = find_book(book_id)
    if book is None:
        return redirect(url_for(
            "view_books",
            message="Book ID does not exist.",
            message_type="error"
        ))
    if book["available"] is True:
        return redirect(url_for(
            "view_books",
            message="Book is already available.",
            message_type="error"
        ))
    book["available"] = True
    book["borrower"] = ""
    save_books(books)
    return redirect(url_for(
        "view_books",
        message="Book returned successfully.",
        message_type="success"
    ))

@app.route("/delete/<book_id>")
def delete_book(book_id):
    book = find_book(book_id)
    if book is None:
        return redirect(url_for(
            "view_books",
            message="Book ID does not exist.",
            message_type="error"
        ))
    books.remove(book)
    save_books(books)
    return redirect(url_for(
        "view_books",
        message="Book deleted successfully.",
        message_type="success"
    ))

if __name__ == "__main__":
    app.run(debug=True)