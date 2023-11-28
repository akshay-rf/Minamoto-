from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db,or_
from sqlalchemy import union, text, func
from .models import User, Book, TransactionBorrow, ActiveLoans, TransactionReturn
from datetime import date, time
import csv

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'], defaults={'loanCon':None})
@views.route('/<loanCon>', methods=['GET', 'POST'])
@login_required
def home(loanCon):
    search=False
    searchTag=""
    numDays=0
    recommend=False
    combined_query = Book.query
    recomBook = Book.query
    count = len(combined_query.all())
    most_common_category = (
    db.session.query(
        Book.category,
        func.count(Book.category).label('category_count')
    ).join(TransactionReturn, Book.bid == TransactionReturn.bookId).filter(TransactionReturn.userId == current_user.id).group_by(Book.category).order_by(func.count(Book.category).desc()).first())

    if most_common_category:
        recommend=True
        comName=most_common_category[0]
        recomBook = Book.query.filter(Book.category==comName)

    else:
        comName=""

    if request.method == 'POST':
        if loanCon:
            try:
                # Adding requested loan. 
                numDays=request.form['days']
                newTrans = TransactionBorrow(userId=current_user.id, bookId=int(loanCon.strip()), due=numDays)
                db.session.add(newTrans)
                Book.query.filter(Book.bid==int(loanCon.strip())).update({'status':'issued', 'issuedId':current_user.id})
                db.session.commit()
                newLoan = ActiveLoans(user=current_user.id, transID=newTrans.tid)
                db.session.add(newLoan)
                db.session.commit()
                flash(f'{numDays} days loan has been approved and added to your account.')
            except:
                pass
        else:
            loanCon=False

        searchTag = request.form.get('Search')
        filters = request.form.get('filter')

        if searchTag:
            if searchTag.strip()!="":
                search=True
                if filters=="all":
                    if len(searchTag.split())>1:
                        combined_query = Book.query.filter(False)
                        for tag in searchTag.split():
                            tag = tag.strip()
                            query1 = Book.query.filter(Book.title.ilike(f"%{tag}%"))
                            query3 = Book.query.filter(Book.author.ilike(f"%{tag}%"))

                            # Fetch all records
                            all_books = query1.union_all(query3)

                            filtered_books = []
                            # Filter records where 'tag' is in the 'tags' list
                            for i in Book.query.all():
                                book = i
                                if tag in i.tags:
                                    filtered_books.append(book)

                            filtered_book_ids = [book.bid for book in filtered_books]

                            # Creating a new query based on the filtered_book_ids
                            filtered_query = Book.query.filter(Book.bid.in_(filtered_book_ids))

                            temp_comb = all_books.union(filtered_query)
                            combined_query = combined_query.union_all(temp_comb).all()
                    else:
                        searchTag = searchTag.strip()
                        query1 = Book.query.filter(Book.title.ilike(f"%{searchTag}%"))
                        query3 = Book.query.filter(Book.author.ilike(f"%{searchTag}%"))

                        # Fetch all records
                        all_books = query1.union_all(query3)

                        filtered_books = []
                        # Filter records where 'tag' is in the 'tags' list
                        for i in Book.query.all():
                            book = i
                            if searchTag in i.tags:
                                filtered_books.append(book)

                        filtered_book_ids = [book.bid for book in filtered_books]

                        # Creating a new query based on the filtered_book_ids
                        filtered_query = Book.query.filter(Book.bid.in_(filtered_book_ids))

                        combined_query = all_books.union(filtered_query).all()
                if filters=="title":
                    searchTag = searchTag.strip()
                    query1 = Book.query.filter(Book.title.ilike(f"%{searchTag}%"))

                    combined_query = query1.all()
                if filters=="author":
                    print("yes")
                    searchTag = searchTag.strip()
                    query3 = Book.query.filter(Book.author.ilike(f"%{searchTag}%"))

                    combined_query = query3.all()
                if filters=="category":
                    searchTag = searchTag.strip()
                    query3 = Book.query.filter(Book.category.ilike(f"%{searchTag}%"))

                    combined_query = query3.all()
                count = len(combined_query)
            else:
                searchTag=""
        else:
            searchTag=""
    
    return render_template("home.html", user=current_user, books=combined_query, recomBook=recomBook, recommend=recommend, count=count, request=request, searched=search, comName=comName, loanCon=loanCon, str=str, or_=or_)

@views.route('/borrow/<bid>', methods=['GET', 'POST'])
@login_required
def borrow(bid):
    return render_template("borrow.html", user=current_user, books=Book, bbid=bid, date=date, str=str)



