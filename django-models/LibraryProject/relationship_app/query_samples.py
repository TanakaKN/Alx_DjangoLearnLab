# relationship_app/query_samples.py
# Standalone script that can be executed under the manage.py environment:
# Run with:
#   python manage.py shell -c "exec(open('relationship_app/query_samples.py').read())"
#
# The script will:
# - create sample data (if none exists)
# - run the three required queries and print results

import django
from django.db import transaction

# When run via the manage.py shell this is already set up; guard for safety.
try:
    # Import models
    from relationship_app.models import Author, Book, Library, Librarian
except Exception:
    # If running outside manage.py shell, we cannot set DJANGO_SETTINGS_MODULE reliably here.
    raise RuntimeError(
        "This script should be run via manage.py shell, for example:\n"
        "python manage.py shell -c \"exec(open('relationship_app/query_samples.py').read())\""
    )

def create_sample_data():
    """
    Create sample data only if none exists to keep the script idempotent.
    """
    if Author.objects.exists() or Book.objects.exists() or Library.objects.exists():
        print("Sample data already exists — skipping creation.")
        return

    with transaction.atomic():
        # Create authors
        a1 = Author.objects.create(name="Jane Austen")
        a2 = Author.objects.create(name="Mark Twain")

        # Create books
        b1 = Book.objects.create(title="Pride and Prejudice", author=a1)
        b2 = Book.objects.create(title="Emma", author=a1)
        b3 = Book.objects.create(title="Adventures of Huckleberry Finn", author=a2)

        # Create libraries
        lib1 = Library.objects.create(name="Central Library")
        lib2 = Library.objects.create(name="Community Library")

        # Add books to libraries (ManyToMany)
        lib1.books.add(b1, b3)
        lib2.books.add(b2)

        # Create librarians (OneToOne with Library)
        Librarian.objects.create(name="Alice", library=lib1)
        Librarian.objects.create(name="Bob", library=lib2)

        print("Sample data created.")


def query_books_by_author(author_name):
    print(f"\nQuery: All books by author '{author_name}':")
    qs = Book.objects.filter(author__name=author_name)
    if not qs.exists():
        print("  (no books found)")
    for b in qs:
        print(f"  - {b.title} (id={b.id})")


def list_all_books_in_library(library_name):
    print(f"\nQuery: List all books in library '{library_name}':")
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print("  (library not found)")
        return
    books = lib.books.all()
    if not books.exists():
        print("  (no books in this library)")
    for b in books:
        print(f"  - {b.title} by {b.author.name}")


def retrieve_librarian_for_library(library_name):
    print(f"\nQuery: Retrieve the librarian for library '{library_name}':")
    try:
        lib = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print("  (library not found)")
        return
    # Access OneToOne via related attribute
    librarian = getattr(lib, "librarian", None)
    if librarian is None:
        print("  (no librarian assigned)")
    else:
        print(f"  Librarian: {librarian.name} (id={librarian.id})")


if __name__ == "__main__":
    # Create sample data if missing
    create_sample_data()

    # Run the three required queries:
    query_books_by_author("Jane Austen")
    list_all_books_in_library("Central Library")
    retrieve_librarian_for_library("Central Library")
