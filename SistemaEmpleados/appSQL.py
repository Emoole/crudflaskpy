import pyodbc

server='DESKTOP-0JTS6LU'
database='BEERSDB'
username='sa'
password='Eliana1234'
driver='{ODBC Driver 17 for SQL Server}'

#Cadena Conexión
connectionString=f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

def listData():
    connection=pyodbc.connect(connectionString)
    cursor=connection.cursor()
    cursor=cursor.execute("SELECT BrandId,BrandName,BrandType FROM Brands")
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

def addData(name,type):
    connection=pyodbc.connect(connectionString)
    cursor=connection.cursor()
    cursor=cursor.execute(f"INSERT INTO Brands (BrandName,BrandType,createdDate) VALUES (?,?, NULL)",(name,type))
    connection.commit()
    connection.close()
    return "End"

""" rows=listData()
for row in rows:
    print(row) """

#addData("VVV","Nacional")
def deleteData(brandId):
    connection=pyodbc.connect(connectionString)
    cursor=connection.cursor()
    cursor=cursor.execute(f"DELETE FROM Brands WHERE BrandID=?",(brandId,))
    connection.commit()
    connection.close()
    return "End"

#deleteData(5)
def updateData(brandName,brandType, brandId):
    connection=pyodbc.connect(connectionString)
    cursor=connection.cursor()
    cursor=cursor.execute(f"UPDATE Brands SET BrandName=?, BrandType=? WHERE BrandID=?",(brandName,brandType,brandId))
    connection.commit()
    connection.close()
    return "End"

updateData('La Vikingota','Nacional',4)