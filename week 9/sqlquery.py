import pyodbc

## SQL datbase connection credentials
## Modify those attribute to meet your situation
server = '<server>.database.windows.net'
database = '<database>'
username = '<username>'
password = '<password>'
driver= '{ODBC Driver 17 for SQL Server}'

## License plate number
# number = 'PT9442'

## Open the connection throught the driver to connect Azure SQL database 
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()
## Execute the SQL command to query the databsae
cursor.execute("SELECT * FROM [license_plate]")
# cursor.execute("SELECT * FROM [license_plate] WHERE Plate_number = '" + number + "'")
row = cursor.fetchone()

## print out the information in the database
while row:
    for att in row:
        print (str(att) + " ", end = " ")
    print ("\n")
    row = cursor.fetchone()