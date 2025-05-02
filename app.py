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
        p_name=request.form.get('pname')
        price=request.form.get('price')
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("INSERT INTO Product(name,price) VALUES(%s,%s)",(p_name,price))
        connection.commit()
        cur.close()
        connection.close()
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
        p_name=request.form.get('pname')
        price=request.form.get('price')
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("SET SQL_SAFE_UPDATES = 0")
        cur.execute("UPDATE Product SET name=%s, price=%s WHERE product_id=%s",(p_name,price,id))
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
        l_name=request.form.get('lname')
        connection=get_db_connection()
        cur=connection.cursor()
        cur.execute("INSERT INTO Location(name) VALUES(%s)",[l_name])
        connection.commit()
        cur.close()
        connection.close()
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
        if to_l=="" : to_l=None
        now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
        dt=now_ist.strftime("%Y-%m-%d %H:%M:%S")
        quantity=request.form.get('quantity')
        if  from_l or to_l : #if any one date is given or not
            connection=get_db_connection()
            cur=connection.cursor()
            #------------------------------------
            if from_l is None and to_l :
                cur.execute("SELECT EXISTS(SELECT 1 FROM Stock WHERE product_id=%s AND location_id=%s)AS product_exist",(p_id,to_l))
                val=cur.fetchall()
                if val[0][0] :
                    cur.execute("SELECT quantity FROM Stock WHERE product_id=%s AND location_id=%s",(p_id,to_l))
                    q=cur.fetchall()
                    cur.execute("UPDATE Stock SET quantity=%s WHERE product_id=%s AND location_id=%s",(q[0][0]+int(quantity),p_id,to_l))
                    connection.commit()
                else :
                    cur.execute("INSERT INTO Stock(product_id,location_id,quantity) VALUES(%s,%s,%s)",(p_id,to_l,quantity))
                    connection.commit()
            elif from_l and to_l is None :
                cur.execute("SELECT EXISTS(SELECT 1 FROM Stock WHERE product_id=%s AND location_id=%s)AS product_exist",(p_id,from_l))
                val=cur.fetchall()
                if val[0][0] :
                    cur.execute("SELECT quantity FROM Stock WHERE product_id=%s AND location_id=%s",(p_id,from_l))
                    q=cur.fetchall()
                    cur.execute("UPDATE Stock SET quantity=%s WHERE product_id=%s AND location_id=%s",(q[0][0]-int(quantity),p_id,from_l))
                    connection.commit()
                else :
                    return render_template('add_movement.html',locations=location,products=product,act="Give the vaild location in From Locaton")
            else :# from_l and to_l
                #from check
                cur.execute("SELECT EXISTS(SELECT 1 FROM Stock WHERE product_id=%s AND location_id=%s)AS product_exist",(p_id,from_l))
                val=cur.fetchall()
                if val[0][0] :
                    cur.execute("SELECT quantity FROM Stock WHERE product_id=%s AND location_id=%s",(p_id,from_l))
                    q=cur.fetchall()
                    cur.execute("UPDATE Stock SET quantity=%s WHERE product_id=%s AND location_id=%s",(q[0][0]-int(quantity),p_id,from_l))
                    connection.commit()
                else :
                    return render_template('add_movement.html',locations=location,products=product,act="Give the vaild location in From Locaton")
                #to check
                cur.execute("SELECT EXISTS(SELECT 1 FROM Stock WHERE product_id=%s AND location_id=%s)AS product_exist",(p_id,to_l))
                val=cur.fetchall()
                if val[0][0] :
                    cur.execute("SELECT quantity FROM Stock WHERE product_id=%s AND location_id=%s",(p_id,to_l))
                    q=cur.fetchall()
                    cur.execute("UPDATE Stock SET quantity=%s WHERE product_id=%s AND location_id=%s",(q[0][0]+int(quantity),p_id,to_l))
                    connection.commit()
                else :
                    cur.execute("INSERT INTO Stock(product_id,location_id,quantity) VALUES(%s,%s,%s)",(p_id,to_l,quantity))
                    connection.commit()
            #------------------------------------
            cur.execute("INSERT INTO Movement(movement_id,product_id,from_location,to_location,quantity,Date_Time) VALUES(%s,%s,%s,%s,%s,%s)",(m_id,p_id,from_l,to_l,quantity,dt))
            connection.commit()
            cur.close()
            connection.close()
        else :
            return render_template('add_movement.html',locations=location,products=product,act="Movement is not added, Please enter ony one location")
    return render_template('add_movement.html',locations=location,products=product,act="Add the Movement")

@app.route('/productmovement')
def product_movement() :
    connection=get_db_connection()
    cur=connection.cursor(dictionary=True)
    cur.execute('''
        SELECT 
        m.movement_id,
        p.name AS product_name,
        COALESCE(fl.name,'N/A') AS from_location_name,
        COALESCE(tl.name,'N/A') AS to_location_name,
        m.quantity,
        m.Date_Time
        FROM Movement m
        JOIN Product p ON m.product_id = p.product_id
        LEFT JOIN Location fl ON m.from_location = fl.location_id
        LEFT JOIN Location tl ON m.to_location = tl.location_id;
    ''')
    movement=cur.fetchall()
    cur.execute('''
        SELECT
        s.stock_id,
        p.name as product_name,
        l.name as location_name,
        s.quantity 
        from Stock s
        JOIN Product p ON s.product_id = p.product_id
        JOIN Location l ON s.location_id = l.location_id ;
    ''')
    stock=cur.fetchall()
    cur.close()
    connection.close()
    return render_template('product_movement.html',movements=movement,stocks=stock)

if __name__=='__main__' :
    app.run(debug=True)