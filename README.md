# Author: Yicheng Jin  Update: 2021/8/10

# Web demo URI: http://120.25.217.202:5656/ (currently the service is down)

# Chinese-Restuarant-Ordering-System
The ordering system consists of three modules: back-end management system, lobby ordering homepage and mobile catering interface. 
Realized Functions: 
1) back-end management system for staff information, orders, products information, products classification, stores, members of the management; 
2) The lobby ordering system showes the food information, and shopping cart function, and the orders and order details could appear in the back-end management system;
3) mobile catering interface, realized the function of personal center and view past orders, through the mobile phone number and verification code to achieve membership login, and can use the mobile phone to place orders.

# Instructions
1) Back-end Language: Python 3.5.3
2) Project Framework: Django 2.2.24
3) Database: MySQL 8.0.21

# Step
1) Download all files under "Chinese_Restuarant_Ordering_System" 
2) Create a local database on your MySQL, named "osdb", The base character set is "utf8" and Database collation is "utf8_general_ci"
3) Then execute the SQL script "osdb_data.sql" against the database "osdb"
4) Open the CMD or SHELL in the directory of the file "manage.py"
5) Type "python manage.py runserver" to launch this project
6) Use this link(http://localhost:8000/) in your browser Entering the backend management system
7) The first screen you will see is the lobby ordering screen. And use the link on the page to enter the back-end management or mobile terminal!

# Attention 
The template file of the project came from the Internet, and the backend was written by the author himself, If there is infringement, please contact me! Thanks!
