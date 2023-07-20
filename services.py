import dao
from datetime import datetime

def generate_output_from_DB(componentId):
    results = dao.get_contacts_of_a_component(componentId)
    output = {'contact':{}}
    contact = {}
    for data in results:
        if data[4] == 'primary':
            contact['primaryContactId']=data[0]
        else:
            contact.setdefault('secondaryContactId', []).append(data[0])
        contact.setdefault('emails', set()).add(data[2])
        contact.setdefault('phoneNumbers', set()).add(data[1])
    contact['emails']=list(contact['emails'])
    contact['phoneNumbers']=list(contact['phoneNumbers'])
    output['contact'] = contact 
    
    return output
    

def identify_operations(email,phoneNumber):
    plinkId,component_with_phone = dao.get_component_with_phone(phoneNumber) # componentId
    elinkId,component_with_email = dao.get_component_with_email(email)
    componentId = None
    if component_with_phone is None and component_with_email is None:
        print("primary")
        # Add new contact with primary
        linkPrecedence = "primary"
        id = dao.create_new_contact(phoneNumber,email,linkPrecedence)
        # Add Component
        assert id is not None
        dao.create_new_component(id,id)
        componentId = id
    elif component_with_phone is None :
        # Add secondary contact 
        linkPrecedence = "secondary"
        linkedId = elinkId
        assert linkedId is not None 
        id = dao.create_new_contact(phoneNumber,email,linkPrecedence,linkedId)
        assert id is not None
        dao.create_new_component(id,component_with_email)
        componentId = component_with_email
    elif  component_with_email is None:
        # Add secondary contact
        linkPrecedence = "secondary"
        linkedId = plinkId
        assert linkedId is not None 
        id = dao.create_new_contact(phoneNumber,email,linkPrecedence,linkedId)
        assert id is not None
        dao.create_new_component(id,component_with_phone)
        componentId = component_with_phone
    elif component_with_phone != component_with_email: # 1,2 : [primary of 1, primary of 2]
        # Merge or update components
        id_and_createdAt = dao.get_id_and_createdAt(component_with_phone,component_with_email) # 2 rows with id and created
        primary_id = sorted(id_and_createdAt, key=lambda x:x[1])[0][0]  # primary
        secondary_id = sorted(id_and_createdAt, key=lambda x:x[1])[1][0] # 
        dao.update_contact_precedence(primary_id,secondary_id)
        dao.update_component(primary_id,secondary_id)
        componentId = primary_id
    else:
        componentId = component_with_email
    assert componentId is not None
    return componentId
    
