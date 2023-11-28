from website import create_app
from website.models import User, TransactionBorrow, ActiveLoans, ExpiredLoans
from flask_apscheduler import APScheduler
from datetime import date, timedelta


app = create_app()
# sched = APScheduler()

if __name__=='__main__':
    app.run(debug=True)