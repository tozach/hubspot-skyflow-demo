import json
import requests

def query(email):

    url = "https://ebfc9bee4242.vault.skyflowapis.com/v1/vaults/cf7ee93a562c42edb4a547a9c2d464ec/query"

    payload = json.dumps({
          "query": "select redaction(name,'PLAIN_TEXT'), redaction(ssn,'PLAIN_TEXT'), redaction(date_of_birth,'PLAIN_TEXT'), redaction(email_address,'PLAIN_TEXT'), redaction(ssn,'PLAIN_TEXT'), redaction(date_of_birth,'PLAIN_TEXT'), state from \"persons\" where email_address = " + "'" + email + "'" })

    print(payload)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-SKYFLOW-ACCOUNT-ID': 'g9f7efc3a598441190763688562fda46',
        'Authorization': 'Bearer sky-m0732-hed95b2aa08046018566795cf362f841'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
    print(response)
    hs_response = {
                    "results": 
                        [
                            {
                                "objectId": 245,
                                "title": "Contact PII",
                                "ssn": response['records'][0]['fields']['ssn'],
                                "email": response['records'][0]['fields']['email_address'],
                                "dob": response['records'][0]['fields']['date_of_birth'],
                                "state": response['records'][0]['fields']['state'],
                                "name": response['records'][0]['fields']['name']
                            }
                        ]
                    }
    print(hs_response)

query("email@someemail.com")