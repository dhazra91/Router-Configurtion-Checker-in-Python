import twilio
from twilio.rest import TwilioRestClient

def inform_phone(message):

    """This function is used to call or send a message to a network admin with certain details.
    Uses the twilio module.

    """


    account = "AC22a5e9d5f644be5fb674f288500ae03a"

    token = "b827727ee17914ebbc6522ff4d4c393e"


    client = TwilioRestClient(account, token)

    call = client.messages.create(to="7202780658",from_="7205360943",body=message)


    print call.sid


def main():
    inform_phone("message")

if __name__=="__main__":
    main()
