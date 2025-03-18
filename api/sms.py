import http.client
import json


def smssender(DAY,NAME):
    conn = http.client.HTTPSConnection("api.sms.ir")

    # Define the payload as a dictionary
    payload = {
        "mobile": "09902122798",
        "templateId": 636881,
        "parameters": [
            {"name":"NAME","value":NAME},{"name":"DAY", "value":DAY},
            {
                "name": "Code",
                "value": "12345"
            }
        ]
    }h

    # Convert the payload dictionary to a JSON string
    payload_json = json.dumps(payload)

    # Define headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': 'Your key here'
    }

    # Send the request with the JSON payload
    conn.request("POST", "/v1/send/verify", body=payload_json, headers=headers)

    # Get the response
    res = conn.getresponse()
    data = res.read()

    # Print the response
    print(data.decode("utf-8"))
    print("SMS has been sent")