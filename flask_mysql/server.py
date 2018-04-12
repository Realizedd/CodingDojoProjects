from flask import Flask
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'mydb')
# an example of running a query
print mysql.query_db('SELECT countries.name, cities.name, cities.district, cities.population FROM cities LEFT JOIN countries ON countries.id = country_id WHERE country_id=9 AND district="Buenos Aires" AND cities.population > 500000')
app.run(debug=True)