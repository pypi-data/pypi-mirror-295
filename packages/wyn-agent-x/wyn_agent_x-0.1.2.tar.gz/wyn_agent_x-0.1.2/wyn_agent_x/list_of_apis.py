from typing import Dict, Any
from twilio.rest import Client
from wyn_agent_x.helper import register_function

@register_function("send_sms")
def send_sms(payload: Dict[str, str], account_sid: str, auth_token: str, event_stream: list) -> Dict[str, Any]:
    """
    Simulate sending an SMS using the Twilio API.
    The event_stream argument is used to log the result of the API call.
    """
    print(f"API Call: Sending SMS with payload: {payload}")
    
    # Initialize Twilio Client with provided credentials
    client = Client(account_sid, auth_token)

    # Simulate sending a message (replace with actual logic for real SMS sending)
    message = client.messages.create(
        body=f"Hello {payload['name']}, this is a test message.",
        from_="+18552060350",  # Replace with a valid Twilio number
        to='+15859538396'  # Replace with the destination number
    )

    print(f"Message SID: {message.sid}")
    response = {"status": f"success: {message.sid}", "model_name": "None"}

    # Append the result to the event stream
    event_stream.append({"event": "api_call", "api_name": "send_sms", "response": response})
    
    return response

# Future API functions can also be registered in the same way:
# @register_function("another_api")
# def another_api(payload: Dict[str, str], account_sid: str, auth_token: str, event_stream: list) -> Dict[str, Any]:
#     # Simulate another API functionality here
#     pass
