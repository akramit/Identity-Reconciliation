from DBcm import UseDatabase
from datetime import datetime

dbconfig = {
    'host':'localhost',
    'user':'amit',
    'password':'amit',
    'database':'identity_db',
}
#data_to_insert = ("John Doe", "john@example.com")

# SQL query to insert data into the table with an auto-incrementing ID
#insert_query = "INSERT INTO customers (customer_name, customer_email) VALUES (%s, %s)"


def get_all():
    output = ''
    with UseDatabase(dbconfig) as cursor:
        _sql = """select * from Contact"""
        cursor.execute(_sql)
        for row in cursor.fetchall():
            output += str(row)+"<br>"
    return output

def get_all_linked_contacts(email,phoneNumber):
    _sql = """ SELECT * FROM Contact WHERE email=%s OR phoneNumber=%s"""
    values =(email,phoneNumber)
    output = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)
        output = cursor.fetchall()
    return output


def create_new_component(id, componentId):
    _sql = """INSERT INTO Components VALUES(%s,%s)"""
    values =(id,componentId)
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)


def create_new_contact(phoneNumber,email,linkPrecedence,linkedId=None) -> 'str':
    createdAt = datetime.now()
    updatedAt= createdAt
    deletedAt= None
    contact_values=(phoneNumber,email,linkedId,linkPrecedence,createdAt,updatedAt,deletedAt)
    _sql=""" INSERT INTO Contact VALUES(NULL,%s,%s,%s,%s,%s,%s,%s) """
    inserted_id = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,contact_values)
        inserted_id = cursor.lastrowid

    return inserted_id

def update_contact_precedence(id,linkedId) -> 'str':
    linkPrecedence = "secondary"
    value = (linkPrecedence,linkedId,id)
    _sql = """ UPDATE Contact SET linkPrecedence=%s, linkedId=%s, updatedAt=CURRENT_TIMESTAMP where id=%s"""
    updated_id = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql)
        updated_id = cursor.lastrowid
    return updated_id


def get_contacts_of_a_component(componentId) -> 'dict':
    _sql = """SELECT * FROM 
                Contact Inner Join Components
                  ON Contact.id = Components.id
                  WHERE Components.componentId = %s"""
    output = []
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,(componentId,))
        output = cursor.fetchall()
    return output



