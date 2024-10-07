from adminControls.adminCodes import CLIENT,messenger
from faunadb import query as q
import requests
import json

###############Normal Message Handler###################

def mediaReplies(data):
    """
    Media message handler to handle normal text messages

    :param: data carries message data (mobile number and message load)
    """
    name = messenger.get_name(data)
    mobile = messenger.get_mobile(data)
    print(f"{mobile} sent image")
    using = CLIENT.query(q.get(q.ref(q.collection("userData"), mobile)))
    conversation_level = using["data"]["conversation_level"]
    
    ng_mobile = mobile.replace("234", "0")
    if conversation_level == "invoice":
        a=2
        
        
    else:
        print (f"{name} a picture with no reply")
        messenger.send_reply_nofooter(button={
"header": "Unknown words",
"body": (f"""Hello there {name}, I don't really understandthis media file you just sent to me please try again?"""),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "BackToStart",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
        return "Done"
