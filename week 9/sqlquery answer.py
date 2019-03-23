import pyodbc

server = 'raspberrypitest.database.windows.net'
database = 'licensedatabase'
username = 'testrole'
password = '56332389Yzh'
driver= '{ODBC Driver 17 for SQL Server}'

number = 'PT9442'

cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()
# cursor.execute("SELECT * FROM [license_plate]")
cursor.execute("SELECT * FROM [license_plate] WHERE Plate_number = '" + number + "'")
row = cursor.fetchone()
while row:
    for att in row:
        print (str(att) + " ", end = " ")
    print ("\n")
    row = cursor.fetchone()