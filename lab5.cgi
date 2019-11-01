#! /usr/bin/python3
import cgi
import cgitb
import os
import passwords
import json
import MySQLdb
cgitb.enable()


if 'PATH_INFO' in os.environ:
    path = os.environ['PATH_INFO']
else:
    path = ""

if path == "":
    print('Status: 302 Redirect')
    print('Location: http://100.27.20.36/cgi-bin/lab5.cgi/json/')

elif path =="/home":
    print('Content-Type: text/html')
    print("Status: 200 OK")
    print()
    print('''<html><head><title>Home</title>
           </head>
           <h1> Home </h1>
           <body>
            <a href="/cgi-bin/lab5.cgi/view">View People</a>
            <br>
            <a href="/cgi-bin/lab5.cgi/person">Add a new Person</a>
           </body>
        </html>''')


elif path == "/person":
    print("Content-Type: text/html")
    print("Status: 200 OK")
    print()
    print('''<html><head>
            </head><body><h1>Add Person</h1>
                    <form action="http://100.27.20.36/cgi-bin/lab5.cgi/add" method="POST">
                       Person Name <input type="text" name="name"><br>
                       Age <input type="text" name="age"><br>
                       City <input type="text" name="city"><br>
                       <input type="submit"></form>
                       </form><br><p>Search for ID<br><form action="/cgi-bin/lab5.cgi/get" method="GET">
                       <input type=number name="id"><br>
                       <input type=submit></form>
              </body>
           </html>''')

elif path =="/add":
    if "REQUEST_METHOD" in os.environ and os.environ["REQUEST_METHOD"] == "POST":
        form = cgi.FieldStorage()
        conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db = "coleshearer")

        name = form['name'].value
        age = form['age'].value
        city = form['city'].value
        cursor = conn.cursor()
        cursor.execute("INSERT INTO lab5(name, age, city) VALUES (%s,%s,%s)", (name,age,city))
        new_id = cursor.lastrowid
        cursor.close()
        conn.commit()

        print('Status: 302 Redirect')
        print('Location: http://100.27.20.36/cgi-bin/lab5.cgi/view')
        print()
elif path =="/get":
    if "REQUEST_METHOD" in os.environ and os.environ["REQUEST_METHOD"] == "GET":
        print('Content-Type: application/json')
        print("Status: 200 OK")
        print()
        form = cgi.FieldStorage()
        conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db = "coleshearer")
        ID = form['id'].value
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM lab5 WHERE id=%s;', (ID,))
        results = cursor.fetchall()
        cursor.close()
        test = []
        fields = ['ID', 'Name', 'Age', 'City']
        for record in results:
            entry = {}
            num = 0
            for row in record:
                num = num % len(fields)
                field = fields[num]
                entry[field] = row
                num += 1
            test.append(entry)
        test_json = json.dumps(test, indent=2)
        print(test_json)

elif path == "/view":
    print('Content-Type: application/json')
    print("Status: 200 OK")
    print()
    conn = MySQLdb.connect(host = passwords.SQL_HOST, user = passwords.SQL_USER, passwd = passwords.SQL_PASSWD, db = "coleshearer")
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM lab5;')
    results = cursor.fetchall()
    test = []
    fields = ['ID', 'Name', 'Age', 'City']
    for record in results:
        entry = {}
        num = 0
        for row in record:
            num = num % len(fields)
            field = fields[num]
            entry[field] = row
            num += 1
        test.append(entry)
    test_json = json.dumps(test, indent=2)
    print(test_json)
    cursor.close()

else:

        print("Content-Type: text/html")
        print("Status: 200 OK")
        print()
        print('''<!DOCTYPE html>
        <html lang="en" dir="ltr">
           <head>
              <meta charset="utf-8">
              <title>Home</title>
           </head>
           <body>
           <center>Invalid path: %s</center>
                <a href="/cgi-bin/view">View People</a>
                <br>
                <a href="/cgi-bin/add">Add a new person</a>
           </body>
        </html>''' % (path,))
