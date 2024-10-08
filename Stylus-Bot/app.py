import requests
from flask import Flask, request, make_response
from faunadb import query as q
from adminControls.adminCodes import messenger, CLIENT
from messages import interactiveReplies, normalReplies, mediaRepliesß

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, It Works"

@app.route("/whatsapi", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        response = make_response(request.args.get("hub.challenge"), 200)
        response.mimetype = "text/plain"
        return response
 
    data = request.get_json()

    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            message_type = messenger.get_message_type(data)
            mobile = messenger.get_mobile(data)
            try:
                CLIENT.query(q.get(q.match(q.index("loginData"), mobile)))
            except:
                CLIENT.query(q.create(q.ref(q.collection("userData"), mobile), {
                    "data": {
                        "id": mobile,
                        "conversation_level": "",
                        "trans_acc": "",
                        "address": {
                            "evm_address": [],
                            "tvm_address": [],
                        },
                        "key": {
                            "evm_key": [],
                            "tvm_key": []
                        },
                        "sale_type": "",
                        "token_address": "",
                        "tokens": {
                            "ETH": [],
                            "BSC": [],
                            "POLY": [],
                            "ARBI": [],
                            "ETHW": [],
                            "TRON": [],
                        },
                        "state": "testnet",
                        "tkey": "",
                        "chain": "",
                        "default": 0,
                        "amount": "",
                        "signed": ""
                    }
                }))
                
            if message_type == "text":
                normalReplies.normalmessage(data) ####Redirect to handler
            elif message_type == "interactive":
                interactiveReplies.interactivebuttons(data) #####Redirect to handler
            elif message_type == "image":
                mediaReplies.mediaReplies(data) #####Redirect to handler
                
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"

if __name__ == '__main__': 
    app.run(debug=True)
