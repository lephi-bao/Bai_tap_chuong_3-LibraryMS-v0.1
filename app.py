from flask import Flask, render_template, request, jsonify, abort

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Lập trình Python cơ bản", "author": "Nguyễn Văn A", "year": 2021, "category": "Lập trình", "available": True},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "year": 2008, "category": "Lập trình", "available": False},
    {"id": 3, "title": "Dune", "author": "Frank Herbert", "year": 1965, "category": "Khoa học viễn tưởng", "available": True},
    {"id": 4, "title": "Lược sử loài người", "author": "Yuval Noah Harari", "year": 2011, "category": "Lịch sử", "available": True},
    {"id": 5, "title": "Cấu trúc dữ liệu và giải thuật", "author": "Lê Văn B", "year": 2019, "category": "Lập trình", "available": True}
]

@app.route("/")
def index():

    total_books = len(BOOKS)

    available_books = sum(
        1 for book in BOOKS
        if book["available"]
    )

    return render_template(
        "index.html",
        total_books=total_books,
        available_books=available_books
    )

@app.route("/books")
def books():

    category = request.args.get("category")

    if category:
        filtered_books = [
            book for book in BOOKS
            if book["category"] == category
        ]
    else:
        filtered_books = BOOKS

    categories = sorted(
        set(book["category"] for book in BOOKS)  # noqa: C401
    )

    return render_template(
        "books.html",
        books=filtered_books,
        categories=categories,
        current_category=category
    )

def find_book(book_id):
    """Tìm sách theo ID."""

    for book in BOOKS:
        if book["id"] == book_id:
            return book

    return None
@app.route("/books/<int:book_id>")
def book_detail(book_id):

    book = find_book(book_id)

    if book is None:
        abort(404, description=f"Không có sách với ID = {book_id}")

    return render_template(
        "book_detail.html",
        book=book
    )


@app.route("/api/books")
def api_books():

    return jsonify(BOOKS)

@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):

    book = find_book(book_id)

    if book is None:
        return jsonify({
            "error": f"Không có sách với ID = {book_id}"
        }), 404

    return jsonify(book)

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html",
        message=error.description or "Trang bạn tìm không tồn tại."
    ), 404


if __name__ == '__main__':
    app.run(debug=True)
