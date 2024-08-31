import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)
@app.errorhandler(404)
def pageNotFound(e):
    return render_template('404.html'), 404
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])


def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username and not password:
            message = 'Username and Password is required.'
        elif not username:
            # If the username field is empty
            message = 'Username is required.'
        elif not password:
            # If the password field is empty
            message = 'Password is required.'
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
            user = cursor.fetchone()

            if not user:
                # If the username is not found in the database
                message = 'Incorrect username!'
            else:
                if user['password'] == password:
                    # If both username and password are correct
                    session['loggedin'] = True
                    session['userid'] = user['id']
                    session['username'] = user['username']
                    message = 'Logged in successfully!'
                    return redirect(url_for('dashboard'))
                else:
                    # If the username is correct but the password is incorrect
                    message = 'Incorrect password!'

    # If the form is not submitted or there's any other issue
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for('login'))

    
@app.route("/dashboard", methods =['GET', 'POST'])
def dashboard():
    if 'loggedin' in session:        
        return render_template("dashboard.html")
    return redirect(url_for('login'))  


@app.route('/category')
def category():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM category")
        data = cur.fetchall()
        cur.close()
        return render_template('category.html', category=data)
    else:
        return redirect(url_for('login'))


@app.route('/insertCategory', methods = ['POST', 'GET'])
def insertCategory():
    if request.method == "POST":
        title = request.form["title"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO category (cat_name) VALUES (%s)", (title,))
        mysql.connection.commit()
        flash("Category successfully added!", "success")
        return redirect(url_for('category'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('category'))
    
    
    
@app.route('/updateCategory', methods = ['POST', 'GET'])
def updateCategory():
    if request.method == "POST":
        cat_id = request.form["cat_id"]
        title = request.form["title1"]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE category  SET cat_name =  %s WHERE cat_id =  %s", (title,cat_id))
        mysql.connection.commit()
        flash("Category successfully updated!", "success")
        return redirect(url_for('category'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('category'))


@app.route('/deleteCategory/<string:id_data>', methods=['POST'])
def delete(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM category WHERE cat_id=%s", (id_data,))
        mysql.connection.commit()
        response = {'code': 200, 'message': 'Category successfully deleted'}
    except Exception as e:
        print(e)
        response = {'code': 500, 'message':e }
    
    return jsonify(response)


@app.route('/rack')
def rack():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rack")
        data = cur.fetchall()
        cur.close()
        return render_template('rack.html', rack=data)
    else:
        return redirect(url_for('login'))



@app.route('/insertRack', methods = ['POST', 'GET'])
def insertRack():
    if request.method == "POST":
        title = request.form["title"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO rack (rack_name) VALUES (%s)", (title,))
        mysql.connection.commit()
        flash("Rack successfully added!", "success")
        return redirect(url_for('rack'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('rack'))


@app.route('/updateRack', methods = ['POST', 'GET'])
def updateRack():
    if request.method == "POST":
        rack_id = request.form["rack_id"]
        title = request.form["title1"]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE rack  SET rack_name =  %s WHERE rack_id =  %s", (title,rack_id))
        mysql.connection.commit()
        flash("Rack successfully updated!", "success")
        return redirect(url_for('rack'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('rack'))


@app.route('/deleteRack/<string:id_data>', methods=['POST'])
def deleteRack(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM rack WHERE rack_id=%s", (id_data,))
        mysql.connection.commit()
        response = {'code': 200, 'message': 'Rack successfully deleted'}
    except Exception as e:
        print(e)
        response = {'code': 500, 'message':e }
    
    return jsonify(response)


@app.route('/books')
def books():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT books.*, category.cat_name, rack.rack_name, SUM(CASE WHEN issued_books.status = 1 THEN 1 ELSE 0 END) AS borrowed FROM books JOIN category ON books.cat_id = category.cat_id JOIN rack ON books.rack_id = rack.rack_id LEFT JOIN issued_books ON books.book_id = issued_books.book_id GROUP BY books.book_id, category.cat_name, rack.rack_name;")
        books = cur.fetchall()

        cur.execute("SELECT * FROM category")
        category = cur.fetchall()

        cur.execute("SELECT * FROM rack")
        rack = cur.fetchall()

        cur.close()
        return render_template('books.html', books=books, category=category, rack=rack)
    else:
        return redirect(url_for('login'))


@app.route('/insertBook', methods = ['POST', 'GET'])
def insertBook():
    
    if request.method == "POST":
        
        title = request.form["title"]
        isbn = request.form["isbn"]
        author = request.form["author"]
        publisher = request.form["publisher"]
        category = request.form["category"]
        rack = request.form["rack"]
        quantity = request.form["quantity"]
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM books where isbn= (%s)", (isbn,))
        row = cur.fetchone()
        if row:
            flash("ISBN already used. Enter again.", "error")
            return redirect(url_for('books'))
        else:
            cur.execute("INSERT INTO books (name, isbn, author, publisher, cat_id, rack_id, quantity) VALUES (%s,%s,%s,%s,%s,%s,%s)", (title, isbn, author, publisher, category, rack, quantity))
            mysql.connection.commit()
            flash("Book successfully added!", "success")
            return redirect(url_for('books'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('books'))
    
    
@app.route('/deleteBook/<string:id_data>', methods=['POST'])
def deleteBook(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM books WHERE book_id=%s", (id_data,))
        mysql.connection.commit()
        response = {'code': 200, 'message': 'Book successfully deleted'}
    except Exception as e:
        print(e)
        response = {'code': 500, 'message':e }
    
    return jsonify(response)


@app.route('/updateBook', methods = ['POST', 'GET'])
def updateBook():
    if request.method == "POST":
        book_id = request.form["book_id"]
        title = request.form["title1"]
        isbn = request.form["isbn1"]
        author = request.form["author1"]
        publisher = request.form["publisher1"]
        category = request.form["category1"]
        rack = request.form["rack1"]
        quantity = request.form["quantity1"]
        cur = mysql.connection.cursor()
        cur.execute("UPDATE books SET name =  %s, isbn = %s, author = %s, publisher = %s, cat_id = %s, rack_id = %s, quantity = %s WHERE book_id =  %s", (title, isbn, author, publisher, category, rack, quantity, book_id))
        mysql.connection.commit()
        flash("Book successfully updated!", "success")
        return redirect(url_for('books'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('books'))


@app.route('/archiveBook/<string:id_data>', methods = ['GET'])
def archiveBook(id_data):
    flash("Book Archived!")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE books set status = %s  WHERE book_id=%s", (2, id_data,))
    mysql.connection.commit()
    return redirect(url_for('books'))

@app.route('/availableBook/<string:id_data>', methods = ['GET'])
def availableBook(id_data):
    flash("Book Available!")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE books set status = %s  WHERE book_id=%s", (1, id_data,))
    mysql.connection.commit()
    return redirect(url_for('books'))


@app.route('/issueBooktoStudent', methods = ['POST', 'GET'])
def issueBooktoStudent():
    if request.method == "POST":
        book_id = request.form["bookID"]
        number_id = request.form["number_id"]
        fullname = request.form["fullname"]
        return_date = request.form["return_date"]
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO issued_books (book_id, number_id, fullname, expected_date) VALUES (%s, %s, %s, %s)", (book_id,number_id, fullname, return_date))
        mysql.connection.commit()
        flash("Book issued successfully!", "success")
        return redirect(url_for('books'))
    else:
       
        flash("Invalid request method", "error")
        return redirect(url_for('books'))
    
    
@app.route('/issued')
def issued():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT issued_books.*, books.name, books.isbn FROM issued_books JOIN books ON issued_books.book_id = books.book_id")
        books = cur.fetchall()
        cur.close()
        current_date = datetime.now().date()
        return render_template('issued.html', books=books, current_date=current_date)
    else:
        return redirect(url_for('login'))


@app.route('/deleteIssued/<string:id_data>', methods=['POST'])
def deleteIssued(id_data):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM issued_books WHERE id=%s", (id_data,))
        mysql.connection.commit()
        response = {'code': 200, 'message': 'Record successfully deleted'}
    except Exception as e:
        print(e)
        response = {'code': 500, 'message':e }
    
    return jsonify(response)

@app.route('/returnBook/<string:id_data>', methods = ['GET'])
def returnBook(id_data):
    flash("Book Returned!")
    cur = mysql.connection.cursor()
    cur.execute("UPDATE issued_books set status = %s  WHERE id=%s", (2, id_data,))
    mysql.connection.commit()
    return redirect(url_for('issued'))


if __name__ == "__main__":
    app.run(debug=True)