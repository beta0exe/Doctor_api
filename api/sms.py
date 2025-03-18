import http.client
import json


def smssender(DAY,NAME,PHONE_NUMBER):
    conn = http.client.HTTPSConnection("api.sms.ir")

    payload = {
        "mobile": str(PHONE_NUMBER),
        "templateId": 636881,
        "parameters": [
            {"name":"NAME","value":NAME},{"name":"DAY", "value":DAY},
            {
                "name": "Code",
                "value": "12345"
            }
        ]
    }

    # Convert the payload dictionary to a JSON string
    payload_json = json.dumps(payload)

    # Define headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': 'Change this to your own key '
    }

    # Send the request with the JSON payload
    conn.request("POST", "/v1/send/verify", body=payload_json, headers=headers)

    # Get the response
    res = conn.getresponse()
    data = res.read()

    # Print the response
    print(data.decode("utf-8"))
    print("SMS has been sent")