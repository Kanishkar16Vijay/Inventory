from flask import Flask,render_template,request
import mysql.connector

app=Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Kanishkar@6374243181',
        database='inventory'
    )
    return connection

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/addproduct',methods=['GET','POST'])
def add_products() :
    if request.method=='POST' :
        p_id=request.form.get('pid')
        p_name=request.form.get('pname')
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("INSERT INTO Product(product_id,name) VALUES(%s,%s)",(p_id,p_name))
        connection.commit()
        cur.close()
        connection.close()
        return render_template('add_product.html')
    return render_template('add_product.html')

@app.route('/viewproduct',methods=['GET','POST'])
def view_product() :
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute("SELECT *FROM Product")
    product=cur.fetchall()
    cur.close()
    connection.close()
    return render_template('view_products.html',products=product)

@app.route('/addlocation',methods=['POST','GET'])
def add_location() :
    if request.method=='POST' :
        l_id=request.form.get('lid')
        l_name=request.form.get('lname')
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("INSERT INTO Location(location_id,name) VALUES(%s,%s)",(l_id,l_name))
        connection.commit()
        cur.close()
        connection.close()
        return render_template('add_location.html')
    return render_template('add_location.html')

@app.route('/viewlocation',methods=['POST','GET'])
def view_location() :
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute("SELECT *FROM Location")
    location=cur.fetchall()
    cur.close()
    connection.close()
    return render_template('view_locations.html',locations=location)

if __name__=='__main__' :
    app.run(debug=True)