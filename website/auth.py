from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User,Book, ActiveLoans, TransactionBorrow, TransactionReturn, ExpiredLoans
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date, timedelta



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, pwd):
                flash("Logged in successfully.", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password or email, try again.", category='error')
        else:
            flash("Incorrect password or email, try again.", category='error')                
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash("Email already exists.", category='error')
        elif "@" not in email:
            flash("Enter a valid email address.", category='error')
        elif password1!=password2:
            flash("Passwords don't match.", category='error')
        elif len(password1)<8:
            flash("Password too short(must be greater than 8 characters).", category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')

            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user) 

@auth.route('/loans', methods=['GET', 'POST'])
def loans():

    print("checking expired loans")
    print(ActiveLoans.query.all())
    for loans in ActiveLoans.query.all():
        print("bruh")
        transaction = TransactionBorrow.query.filter(TransactionBorrow.tid==loans.transID).first()
        user = User.query.filter(transaction.userId == User.id).first()
        dueDate = transaction.time + timedelta(int(transaction.due))
        print(dueDate)
        if dueDate.date() < date.today():
            daysPast = date.today() - dueDate.date()
            daysPast = daysPast.days
            newFine = ExpiredLoans(user=user.id, transID=transaction.tid, daysPastDue=daysPast)
            db.session.add(newFine)
            db.session.delete(loans)
            db.session.commit()
    print("updated...")

    if request.method == "POST":
        exp=False
        for i in range(ActiveLoans.query.filter(current_user.id==ActiveLoans.user).count()):
            if request.form.get('idek'+str(i), None):
                bid = int(request.form.get('idek'+str(i)))

        for i in range(ExpiredLoans.query.filter(current_user.id==ExpiredLoans.user).count()):
            if request.form.get('udek'+str(i), None):
                exp=True
                bid = int(request.form.get('udek'+str(i)))
        if exp:
            for loan in ExpiredLoans.query.filter(current_user.id==ExpiredLoans.user):
                trans = TransactionBorrow.query.filter(TransactionBorrow.tid == loan.transID).first()
                if trans.bookId==bid:
                    print(bid)
                    newTrans = TransactionReturn(userId=loan.user, bookId=trans.bookId, overDue=0)
                    db.session.add(newTrans)
                    Book.query.filter(Book.bid==bid).update({'status':'available', 'issuedId':None})
                    print(trans.bookId)
                    db.session.delete(loan)
                    db.session.commit()

        for loan in ActiveLoans.query.filter(current_user.id==ActiveLoans.user):
            trans = TransactionBorrow.query.filter(TransactionBorrow.tid == loan.transID).first()
            if trans.bookId==bid:
                print(bid)
                newTrans = TransactionReturn(userId=loan.user, bookId=trans.bookId, overDue=0)
                db.session.add(newTrans)
                Book.query.filter(Book.bid==bid).update({'status':'available', 'issuedId':None})
                print(trans.bookId)
                db.session.delete(loan)
                db.session.commit()

    return render_template("loans.html", user=current_user, books=Book, loans=ActiveLoans, exploans=ExpiredLoans, transact=TransactionReturn, transactions=TransactionBorrow, str=str, date=date, timedelta=timedelta, int=int)