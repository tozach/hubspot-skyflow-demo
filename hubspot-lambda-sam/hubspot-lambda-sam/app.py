import requests
import json

def query(email):

    url = "https://ebfc9bee4242.vault.skyflowapis.com/v1/vaults/cf7ee93a562c42edb4a547a9c2d464ec/query"

    payload = json.dumps({
          "query": "select redaction(name,'PLAIN_TEXT'), redaction(ssn,'PLAIN_TEXT'), redaction(date_of_birth,'PLAIN_TEXT'), redaction(email_address,'PLAIN_TEXT'), redaction(ssn,'PLAIN_TEXT'), redaction(date_of_birth,'PLAIN_TEXT'), state from \"persons\" where email_address = " + "'" + email + "'"
    })

    print(payload)

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-SKYFLOW-ACCOUNT-ID': 'g9f7efc3a598441190763688562fda46',
        'Authorization': 'Bearer <API Key here>'
    }

    response = requests.request("POST", url, headers=headers, data=payload).json()
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
    return hs_response

def lambda_handler(event, context):

    # 200 is the HTTP status code for "ok".
    print("Hubspot event is :"+str(event))
    status_code = 200
    # From the input parameter named "event", get the body, which contains
    # the input rows.
    query_params = event.get('queryStringParameters', {})
    print(query_params)
    
    # Accessing specific query parameters
    email = query_params.get('email', 'NONE')

    print(email)

    # The return value will contain an array of arrays (one inner array per input row).

    try:
        # From the input parameter named "event", get the body, which contains
        # the input rows.
        print("Going to call query API ...")
        queryResponse = query(email)
        print("Query response is: "+str(queryResponse))
        # Convert the input from a JSON string into a JSON object.
        payload = queryResponse
        print(payload)
        return json.dumps(queryResponse, indent=4, sort_keys=True)

    except Exception as err:
        # 400 implies some type of error.
        print(err)

        error_response= {
                    "results": 
                        [
                            {
                                "objectId": 245,
                                "title": "Contact PII",
                                "ssn": "Not found",
                                "email": "Not found",
                                "dob": "Not found",
                                "state": "Not found",
                                "name": "Not found"
                            }
                        ]
                    }
        return json.dumps(error_response, indent=4, sort_keys=True)