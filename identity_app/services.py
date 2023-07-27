import dao
from datetime import datetime

def generate_output_from_DB(componentId):
    results = dao.get_contacts_of_a_component(componentId)
    output = {'contact':{}}
    primaryEmail = None
    primaryPhone = None
    contact = {}
    for data in results:
        if data[4] == 'primary':
            contact['primaryContactId']=data[0]
            primaryEmail = data[2]
            primaryPhone = data[1]
        else:
            contact.setdefault('secondaryContactId', []).append(data[0])
        contact.setdefault('emails', set()).add(data[2])
        contact.setdefault('phoneNumbers', set()).add(data[1])
    contact['emails']=list(contact['emails'])
    contact['emails'].remove(primaryEmail)
    contact['emails'].insert(0,primaryEmail)
    contact['phoneNumbers']=list(contact['phoneNumbers'])
    contact['phoneNumbers'].remove(primaryPhone)
    contact['phoneNumbers'].insert(0,primaryPhone)
    output['contact'] = contact 
    
    return output
    

def identify_operations(email,phoneNumber):
    plinkId,component_with_phone = None, None
    elinkId,component_with_email = None, None
    if phoneNumber != "null" :
        plinkId,component_with_phone = dao.get_component_with_phone(phoneNumber)
    if email != "null" :
        elinkId,component_with_email = dao.get_component_with_email(email)
    componentId = None
    if component_with_phone is None and component_with_email is None:
        # Add new contact with primary
        linkPrecedence = "primary"
        id = dao.create_new_contact(phoneNumber,email,linkPrecedence)
        # Add Component
        assert id is not None
        dao.create_new_component(id,id)
        componentId = id
    elif phoneNumber != "null" and component_with_phone is None :
        # Add secondary contact 
        linkPrecedence = "secondary"
        linkedId = elinkId
        assert linkedId is not None 
        id = dao.create_new_contact(phoneNumber,email,linkPrecedence,linkedId)
        assert id is not None
        dao.create_new_component(id,component_with_email)
        componentId = component_with_email
    elif  email !="null" and component_with_email is None:
        # Add secondary contact
        linkPrecedence = "secondary"
        linkedId = plinkId
        assert linkedId is not None 
        id = dao.create_new_contact(phoneNumber,email,linkPrecedence,linkedId)
        assert id is not None
        dao.create_new_component(id,component_with_phone)
        componentId = component_with_phone
    elif component_with_phone != component_with_email: 
        # Merge or update components
        id_and_createdAt = dao.get_id_and_createdAt(component_with_phone,component_with_email) 
        primary_id = sorted(id_and_createdAt, key=lambda x:x[1])[0][0]  
        if len(id_and_createdAt) > 1:
            secondary_id = sorted(id_and_createdAt, key=lambda x:x[1])[1][0] 
            dao.update_contact_precedence(primary_id,secondary_id)
            dao.update_component(primary_id,secondary_id)
        componentId = primary_id
    else:
        componentId = component_with_email
    assert componentId is not None
    return componentId
    
