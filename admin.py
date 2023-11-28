from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from website.models import Book, TransactionBorrow, ActiveLoans, ExpiredLoans, TransactionReturn, User
import click

DB_NAME = 'database.db'
engine = create_engine(f'sqlite:///instance/{DB_NAME}')
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--title', prompt='Title', help='Title of the book')
@click.option('--author', prompt='Author', help='Author of the book')
@click.option('--category', prompt='Category', help='Category of the book')
@click.option('--tags', prompt='Tags(seperated by space)', help='Tags for the book')
def add_book(title, author, category, tags):
    """Add a new book to the database."""
    new_book = Book(title=title, author=author, category=category, tags=tags.split(), status='Available')
    session.add(new_book)
    session.commit()
    click.echo(f'Book "{title}" by {author} added successfully.')

@cli.command()
@click.option('--email', prompt='Email', help='Email of the user')
@click.option('--password', prompt='Password', hide_input=True, help='Password of the user')
@click.option('--first-name', prompt='First Name', help='First name of the user')
def add_user(email, password, first_name):
    """Add a new user to the database."""
    new_user = User(email=email, password=password, firstName=first_name)
    session.add(new_user)
    session.commit()
    click.echo(f'User "{first_name}" added successfully.')

@cli.command()
@click.option('--book-id', prompt='Book ID', help='ID of the book to edit')
@click.option('--title', prompt='Title', help='New title of the book')
@click.option('--author', prompt='Author', help='New author of the book')
@click.option('--category', prompt='Category', help='New category of the book')
@click.option('--tags', prompt='Tags(seperated by space)', help='Tags for the book')
def edit_book(book_id, title, author, category, tags):
    """Edit an existing book in the database."""
    book = session.query(Book).get(book_id)
    if book:
        book.title = title if title else book.title
        book.author = author if author else book.author
        book.category = category if category else book.category
        book.tags = tags.split() if tags else book.tags
        session.commit()
        click.echo(f'Book with ID {book_id} edited successfully.')
    else:
        click.echo(f'Book with ID {book_id} not found.')

@cli.command()
@click.option('--book-id', prompt='Book ID', help='ID of the book to delete')
def delete_book(book_id):
    """Delete a book from the database."""
    book = session.query(Book).get(book_id)
    if book:
        session.delete(book)
        session.commit()
        click.echo(f'Book with ID {book_id} deleted successfully.')
    else:
        click.echo(f'Book with ID {book_id} not found.')

@cli.command()
@click.option('--user-id', prompt='User ID', help='ID of the user to delete')
def delete_user(user_id):
    """Delete a user from the database."""
    user_to_delete = session.query(User).get(user_id)
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        click.echo(f'User with ID {user_id} deleted successfully.')
    else:
        click.echo(f'User with ID {user_id} not found.')


if __name__ == '__main__':
    cli()