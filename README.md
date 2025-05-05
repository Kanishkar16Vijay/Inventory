# Project Name
Inventory Management System
## Prerequesties
- MySQL
- Python
- Flask
## Installation 
1. Open Command Prompt and install flask
   ```bash
   pip install flask
   ```
2. Then install Mysql
   ```bash
   pip install mysql-connector-python
   ```
## Procedure
### 1. Creating DataBase
- Create Database for the data storage and crete some table
  - Product -> To store the details of Products
  - Location -> To store the details of Location
  - Movement -> To store the movement of product in the table like(product_id, from_location_id, to_location_id, quantity)
  - Stock -> To store the product quantity details by their places and we can transport the product quantity to other place
### 2. Connecting DB
- This is the connecting procedure to connect DB
  ```bash
  def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='yourpassword',
        database='databasename'
    )
    return connection
  ```
- This is the query executing process
  ```bash
  connection=get_db_connection()
  cur=connection.cursor()
  cur.execute() # This is the query executing function we have give query here
  connection.commit()
  cur.close()
  connection.close()
  ```
### 3. Web Page 
- Using HTML code we can design the pages we want
  - index.html -> This page is an initial page which has lot of options in this page
    ![Screenshot 2025-05-05 172954](https://github.com/user-attachments/assets/5c209f5b-8976-4c8b-9508-8315221d921a)
  - add_product.html -> This page contains form which is help to get the product name and price
    ![Screenshot 2025-05-05 173015](https://github.com/user-attachments/assets/2e64e2e4-9fd4-40a0-b8bc-7a4b080bbd00)
  - view_product.html -> This page contains table which has product details with an option of **EDIT**
    ![Screenshot 2025-05-05 173033](https://github.com/user-attachments/assets/9454c74f-be67-49e9-a949-d226f1b43aba)
  - edit_product.html -> This is page for edit the add product in the table, this is not availale in the options in the index.html. This only in the *view_product.html*
    ![Screenshot 2025-05-05 173245](https://github.com/user-attachments/assets/7c5b4d2a-32ba-4ed3-86e8-4301729ecf8a)
  - add_location.html -> This page contains form which is help to get location name
    ![Screenshot 2025-05-05 173048](https://github.com/user-attachments/assets/0721f2f1-4d62-4e71-8bda-a2122c111f42)
  - view_location.html -> This page contains table which has location name
    ![Screenshot 2025-05-05 173103](https://github.com/user-attachments/assets/5206ae08-e708-4382-804c-999543b1c6c7)
  - add_movement.html -> This page contains form of getting product name, from location, to location, quantity and date&time
    ![Screenshot 2025-05-05 173135](https://github.com/user-attachments/assets/4dfeb23e-c012-4b9d-a898-8da87dff4ce5)
  - product_movement.html -> This page contains two table one for history of product movement
    ![Screenshot 2025-05-05 173206](https://github.com/user-attachments/assets/baa6ffe2-6401-4994-92f6-088f8238e57c)
    another one has quantity of product in certain location
    ![Screenshot 2025-05-05 173217](https://github.com/user-attachments/assets/c7cbf490-a222-434f-bcef-af8000322f34)
### 6. File Structure
```bash
Inventory
├──templates
      ├──index.html
      ├──add_product.html
      ├──view_product.html
      ├──edit_product.html
      ├──add_location.html
      ├──view_location.html
      ├──add_movement.html
      ├──product_movement.html
├──app.py
├──Demo Video.mp4
```
### 5. Execute
1. Open command prompt and type
   ```bash
   python app.py
   ```
2. Press the ```Ctrl+``` click on this link ```http://127.0.0.1:5000```
   ![Screenshot 2025-05-05 190903](https://github.com/user-attachments/assets/77bf3dc9-0394-44ed-b86c-6d26cf83ff29)
## Demo Video
https://drive.google.com/file/d/1dgN_tJDx-th9yVcs3KhsveS-56ZzaZci/view?usp=sharing
