from DBcm import UseDatabase
from datetime import datetime

# dbconfig = {
#     'host':'localhost',
#     'user':'amit',
#     'password':'amit',
#     'database':'identity_db',
# }
dbconfig = {
    'host':'db',
    'port':'3306',
    'user':'root',
    'password':'root',
    'database':'identity_db',
}


def get_component_with_phone(phoneNumber):
    _sql = """SELECT Contact.id,Components.componentId FROM Contact INNER JOIN Components 
                ON Components.id = Contact.id WHERE Contact.phoneNumber=%s"""
    values =(phoneNumber,)
    id,componentId = None,None
    output = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)
        output=cursor.fetchall()
        if len(output) > 0 :
            id,componentId = output[0]
    return (id,componentId)

def get_component_with_email(email):
    _sql = """SELECT Contact.id,Components.componentId FROM Contact INNER JOIN Components 
                ON Components.id = Contact.id WHERE Contact.email=%s"""
    values =(email,)
    id,componentId = None,None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)
        output=cursor.fetchall()
        if len(output) > 0 :
            id,componentId = output[0]
    return (id,componentId)

def create_new_component(id, componentId):
    _sql = """INSERT INTO Components VALUES(%s,%s)"""
    values =(id,componentId)
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)

def update_component(primary_id,secondary_id):
    _sql = """ UPDATE Components SET componentId=%s WHERE componentId=%s"""
    values = (primary_id,secondary_id)
    updated_id = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)
        updated_id = cursor.lastrowid
    return updated_id

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

def update_contact_precedence(primary_id,id) -> 'str':
    linkPrecedence = "secondary"
    values = (linkPrecedence,primary_id,id)
    _sql = """ UPDATE Contact SET linkPrecedence=%s, linkedId=%s, updatedAt=CURRENT_TIMESTAMP where id=%s"""
    updated_id = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)
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


def get_id_and_createdAt(component_with_phone,component_with_email):
    # 2 rows with id and created
    _sql = """SELECT id,createdAt FROM Contact WHERE id in (%s,%s)"""
    values = (component_with_phone,component_with_email)
    output = None
    with UseDatabase(dbconfig) as cursor:
        cursor.execute(_sql,values)
        output=cursor.fetchall()
    return output
