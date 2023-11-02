import pyodbc


def Conexion():
    SERVER = 'UHYXI60121'
    DATABASE = 'Sueldos'
    USERNAME = 'Pier'
    PASSWORD = '123'
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + SERVER + ';DATABASE=' + DATABASE + ';UID=' + USERNAME + ';PWD=' + PASSWORD)
        print('Conexion exitosa')
        return conexion
    except Exception as e:
        print(e)
