# Identity-Reconciliation
Linking different orders made with different contact information to the same person. For detailed use case - [Read Here](https://bitespeed.notion.site/Bitespeed-Backend-Task-Identity-Reconciliation-53392ab01fe149fab989422300423199)


###  Run Application 
1. Clone the repo ```Identity-Reconciliation```
2. Go to directory ```/Identity-Reconciliation```
3. Execute ```docker-compose up -d```
4. ```/identify``` endpoint is exposed at - ```0.0.0.0:5432/identify```
5. Send a POST request with JSON body. JSON Body has format
   ```json
   {
   "email":"email",
   "phoneNumber":"phone"
   }
   ```

### Tests ###
<b>SET UP </b>: Fire a <b>POST</b> request - ```0.0.0.0:5432/identify``` 
#### Test 1 ####
 INPUT : 
 ```json 
 { "email":"mcfly@hillvalley.edu","phoneNumber":"123456" }
```

OUTPUT : 
```json
{
    "contact": {
        "emails": [
           "mcfly@hillvalley.edu"
        ],
        "phoneNumbers": [
            "123456"
        ],
        "primaryContactId": 1
    }
}
```

RESULT : PASS

#### Test 2 ####
 INPUT : 
 ```json
 { "email":"lorraine@hillvalley.edu","phoneNumber":"123456"}
``` 

OUTPUT :
```json
{
    "contact": {
        "emails": [
      
            "mcfly@hillvalley.edu",
            "lorraine@hillvalley.edu"
        ],
        "phoneNumbers": [
            "123456"
        ],
        "primaryContactId": 1,
        "secondaryContactId": [
            2
        ]
    }
}
```

RESULT : PASS

#### Test 3 ####
INPUT :
```json 
{ "email":"null","phoneNumber":"123456"}
```
OUTPUT :
```json
{
    "contact": {
        "emails": [
            "mcfly@hillvalley.edu",
            "lorraine@hillvalley.edu"
        ],
        "phoneNumbers": [
            "123456"
        ],
        "primaryContactId": 1,
        "secondaryContactId": [
            2
        ]
    }
}
```
RESULT : PASS

#### Test 4 ####
INPUT : 
```json
{ "eml":"null","phone":"123456"}
```
OUTPUT: 
```json
{"error": "Invalid JSON data. Missing Parameters"}
```
RESULT : PASS 

