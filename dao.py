from DBcm import UseDatabase

dbconfig = {
    'host':'localhost',
    'user':'amit',
    'password':'amit',
    'database':'identity_db',
}

def get_all():
    output = ''
    with UseDatabase(dbconfig) as cursor:
        _SQL = """select * from Contact"""
        cursor.execute(_SQL)
        for row in cursor.fetchall():
            output += str(row)+"<br>"
    return output