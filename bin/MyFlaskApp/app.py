from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask.ext.mysql import MySQL
import mysql.connector
import Smart_Shopper_Lib_Tester as SSL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)
#Config mysql
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root123'
app.config['MYSQL_DATABASE_DB'] = 'smartshopper'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)

cust_id = 2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

class RegisterForm(Form):
    rfid = StringField('Rfid', [validators.Length(min=12, max=12)])
    userid = StringField('Userid', [validators.Length(min=1, max=5)])
    username = StringField('Username', [validators.Length(min = 3, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords do not match')
    ])
    wal_amt = StringField('Wallet Amount', [validators.Length(min = 1, max=6)])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    con, cursor = SSL.establish_conn()
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        rfid = form.rfid.data
        userid = form.userid.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        wal_amt = form.wal_amt.data
        #create cursor
#        cur = mysql.connection.cursor()
        cursor.execute("INSERT INTO customer(C_ID, C_Name, Password, Wallet_Amount) VALUES(%s, %s, %s, %s)",(userid, username, password, wal_amt))
        con.commit()
        cursor.execute("INSERT INTO rfid_link VALUES(%s,%s)",(rfid, userid))

        #Commit to db
#        mysql.connection.commit()
        con.commit()
        #Close Connection
        con.close()
        cursor.close()


        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields

        username = request.form['username']
        password_candidate = request.form['password']
        app.logger.info(username)

        # Create cursor
        try:
            con, cur = SSL.establish_conn()

        # Get user by username
            q_add = ("SELECT * FROM register WHERE Username = %s")

            result = cur.execute(q_add, (username,))
            res_1 = cur.fetchone()
            app.logger.info(res_1)
            app.logger.info(result)
            if res_1 :
            # Get stored hash
                app.logger.info('hi')


                password = res_1[2]
                app.logger.info(password)
                try :
            # Compare Passwords
                    if sha256_crypt.verify(password_candidate, password):
                # Passed
                        app.logger.info('Matched')
                        session['logged_in'] = True
                        session['username'] = username

                        flash('You are now logged in', 'success')
                        return redirect(url_for('dashboard'))

                    else:
                        app.logger.info('Not Matched')
                    # Close connection
                        error = 'Invalid login'
                        return render_template('login.html', error=error)
                        cur.close()
                except :
                    app.logger.info("minor failure")
            else:
                app.logger.info('no user')
                error = 'Username not found'
                return render_template('login.html', error=error)
        except :
            app.logger.info('Failure')
        return render_template('login.html')
    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/dashboard')
@is_logged_in
def dashboard():
    con, cursor = SSL.establish_conn()
    cust_detail = SSL.cust_detail(cust_id, cursor)
    items = SSL.items_bought(cust_id,cursor)
    wallet_amt = SSL.get_amount_in_wallet(cust_id,cursor)
    total_cost = SSL.calculate_total(cust_id, cursor)
    balance = wallet_amt-total_cost
    if balance < 0 :
        flash('You do not have sufficient Balance to purchase this item', 'error')

    return render_template('dashboard.html', cust_id = cust_id, cust_detail = cust_detail, items = items, wallet_amt = wallet_amt, total_cost = total_cost)

    # Get articles




    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

#Check if user logged if __name__ == '__main__':


#User Log out
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
    wal_amt = 0
    if SSL.deduct_amount(cust_id,cursor):
        con.commit()
        wal_amt = SSL.get_amount_in_wallet(cust_id, cursor)
        msg = "The items have been bought and the total cost is removed from the wallet. Balance Amount : "
    else :
        msg = "Error in updating wallet"
    return render_template('logout.html', msg = msg, wal_amt = wal_amt)

@app.route('/cust_details')
def cust_details():
    cust_detail = SSL.cust_detail(cust_id, cursor)
    items = SSL.items_bought(cust_id,cursor)
    wallet_amt = SSL.get_amount_in_wallet(cust_id,cursor)
    total_cost = SSL.calculate_total(cust_id, cursor)
    balance = wallet_amt-total_cost
    if balance < 0 :
        flash('You do not have sufficient Balance to purchase this item', 'error')

    return render_template('cust_details.html', cust_id = cust_id, cust_detail = cust_detail, items = items, wallet_amt = wallet_amt, total_cost = total_cost)


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug =True)
