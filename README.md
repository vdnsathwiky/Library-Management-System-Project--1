# Library Management System 

## Main features
- Home page
- View books
- Add books
- Search books
- Issue books
- Return books
- Delete books
- Input validation
- Duplicate Book ID validation

## Bonus features
- Book details (+3)
- Borrower name when issuing (+3)
- JSON persistence (+4)

## Technologies
Python, Flask, Jinja2, HTML, CSS, JSON

No React, Angular, REST API, JWT, OAuth, SQLAlchemy or MongoDB are used.

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000


## Demonstration
1. Home
2. View the five initial books
3. Open B001 Details
4. Add B006
5. Search for python
6. Issue B001 and enter a borrower name
7. Show B001 as Issued
8. Try issuing B001 again and show the error
9. Return B001
10. Delete B006
11. Restart Flask and show data remains because of books.json

## Persistence
The Python list remains the main data structure. The optional JSON feature saves the list to books.json and loads it when the application starts.
