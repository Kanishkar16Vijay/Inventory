from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
from datetime import datetime
from zoneinfo import ZoneInfo

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

@app.route('/viewproduct')
def view_product() :
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute("SELECT *FROM Product")
    product=cur.fetchall()
    cur.close()
    connection.close()
    return render_template('view_products.html',products=product)

@app.route('/editproduct/<string:id>',methods=['GET','POST'])
def edit_product(id) :
    if request.method=='POST' :
        p_id=request.form.get('pid')
        p_name=request.form.get('pname')
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("SET SQL_SAFE_UPDATES = 0")
        cur.execute("UPDATE Product SET name=%s WHERE product_id=%s",(p_name,p_id))
        cur.execute("SET SQL_SAFE_UPDATES = 1")
        connection.commit()
        cur.close()
        connection.close()
        return redirect(url_for('view_product'))
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute("SELECT *FROM Product WHERE product_id=%s",[id])
    res=cur.fetchone()
    return render_template('edit_product.html',result=res)

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

@app.route('/viewlocation')
def view_location() :
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute("SELECT *FROM Location")
    location=cur.fetchall()
    cur.close()
    connection.close()
    return render_template('view_locations.html',locations=location)

@app.route('/addmovement',methods=['POST','GET'])
def add_movement() :
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute("SELECT *FROM Product")
    product=cur.fetchall()
    cur.execute("SELECT *FROM Location")
    location=cur.fetchall()
    cur.close()
    connection.close()
    if request.method=='POST' :
        m_id=request.form.get('mid')
        p_id=request.form.get('pid')
        from_l=request.form.get('froml')
        if from_l=="" : from_l=None
        to_l=request.form.get('tol')
        now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
        dt=now_ist.strftime("%Y-%m-%d %H:%M:%S")
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("INSERT INTO Movement(movement_id,product_id,from_location,to_location,Date_Time) VALUES(%s,%s,%s,%s,%s)",(m_id,p_id,from_l,to_l,dt))
        connection.commit()
        cur.close()
        connection.close()
        return render_template('product_movement.html',locations=location,products=product)
    return render_template('product_movement.html',locations=location,products=product)

if __name__=='__main__' :
    app.run(debug=True)