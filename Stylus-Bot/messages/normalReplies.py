import math
from adminControls.adminCodes import CLIENT,messenger, ETHERS
from faunadb import query as q
from hexbytes import HexBytes
from web3.middleware import construct_sign_and_send_raw_middleware
import phonenumbers
import requests
from bs4 import BeautifulSoup

########################################################
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

###############Normal Message Handler###################
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def isInt(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
    
def isNumber(num) -> bool:
    if isInt(num):
        my_number = phonenumbers.parse(num, "NG")
        can = phonenumbers.is_valid_number(my_number)
        if can == True:
            return True
        else:
            return False
    else:
        return False

def isUserName(username: str):
    url = f'https://t.me/{username}'
    r = requests.get(url)
    soup = BeautifulSoup(url, features="html.parser")
    if r.status_code == 200:
        try:
            soup.find_all('div', class_='tgme_page_additional')
            return True
        except:
            return False
    else:
        return False

def getIdByUser(username: str) -> int:
    teleadmin = CLIENT.query(q.get(q.ref(q.collection("adminCollect"), 123456789)))
    user = teleadmin["data"]["username"]
    chat_id_index = user.index(username.lower())
    chat_id = teleadmin["data"]["chat_id"][int(chat_id_index)]
    return chat_id

def normalmessage(data):
    """
    Normal message handler to handle normal text messages

    :param: data carries message data (mobile number and message load)

    """
    mobile = messenger.get_mobile(data)
    message = messenger.get_message(data)
    name = messenger.get_name(data)
    using = CLIENT.query(q.get(q.ref(q.collection("userData"), mobile)))
    conversation_level = using["data"]["conversation_level"]
    default = using["data"]["default"]
    key = using["data"]["key"]
    address = address = using["data"]["address"]
    chain = using["data"]["chain"]


    tokens = ""
    if address == [] and chain == "":
        address = address = using["data"]["address"]
        key = using["data"]["key"]
    else:
        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            try:
                key = using["data"]["key"]["evm_key"][int(default)]
                address = using["data"]["address"]["evm_address"][int(default)]
            except:
                key = using["data"]["key"]["evm_key"][0]
                address = using["data"]["address"]["evm_address"][0]
            tokens = using["data"]["tokens"][chain]

        elif chain == "TRON":
            try:
                key = using["data"]["key"]["tvm_key"][int(default)]
                address = using["data"]["address"]["tvm_address"][int(default)]
            except:
                key = using["data"]["key"]["tvm_key"][0]
                address = using["data"]["address"]["tvm_address"][0]
            tokens = using["data"]["tokens"][chain]
    trans_acc = using["data"]["trans_acc"]
    tkey = using["data"]["tkey"]
    amount = using["data"]["amount"]
    token_address = using["data"]["token_address"]
    state = using["data"]["state"]
    signed = using["data"]["signed"]
   
    ####### Main Menu Block ######
    p_message = message.lower() #pure message to lower case for tests and conditionals

    
    if p_message in ['hello', "0", "hey", "hi", "main", "menu", "main menu", "good", "good morning", "start app", "start", "hey", "how are you"]:
        print (f"{name} activated main menu with {message}")
        if signed == "":
            messenger.send_reply_noheader(button={
"body": (f"""
Hi {name}, 
Welcome to NOVICHAIN

Send Crypto, Receive Crypto, Connect to DApps, Manage all your Crypto Tokens all on Whatsapp"""),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "create account",
        "title": "Create Account" 
    }
    }
] 
}
}, recipient_id=mobile)
        
        else:
            _chain = ETHERS.base(chain)
            chain_name = _chain['chain_name']
            messenger.send_reply_noheader(button={
"body": (f"""
Hi {name},
What would you like to do today

Your Current Chain: {chain_name}"""),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "account",
        "title": "Account" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "switch chain",
        "title": "Switch Chain" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "switch account",
        "title": "Switch Account" 
    }
    }
] 
}
}, recipient_id=mobile)
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))
        return "Done"
#
    elif conversation_level == "transkey":
        account = ETHERS.create_wallet("BSC")
        evm_address = []
        evm_key =[]
        evm_address.append(account["evm_address"])
        evm_key.append(account["evm_key"])
        tvm_address = []
        tvm_key = []
        tvm_address.append(account["tvm_address"])
        tvm_key.append(account["tvm_key"])
        

        messenger.send_reply_noheader(button={
    "body": (f"""
Congrats {name}, your ChatFi account has been created. 
You can now Send Crypto, Receive Crypto, Retrieve Account Private Keys, Import Private Keys, Swap Crypto on the ChatFi.

Your Current Chain: BSC

Your address: {evm_address[0]}

What would you like to do next?"""),
    "action": {
    "buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "account",
        "title": "Account" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "switch chain",
        "title": "Switch Chain" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "Switch account",
        "title": "Switch Account" 
    }
    }
    ] 
    }
    }, recipient_id=mobile)
        raw_list_bsc = ETHERS.default_token_list('BSC', state)
        raw_list_eth = ETHERS.default_token_list('ETH', state)
        raw_list_poly = ETHERS.default_token_list('POLY', state)
        raw_list_arbi = ETHERS.default_token_list('ARBI', state)
        raw_list_tron = ETHERS.default_token_list('TRON', state)
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {
            "data": {
                "chain": "BSC",
                "address": {
                    "evm_address": evm_address,
                    "tvm_address": tvm_address,
                },
                "key": {
                    "evm_key": evm_key,
                    "tvm_key": tvm_key
                },
                "tkey": message,
                "conversation_level": "",
                "signed": "Done",
                "tokens":{
                    "BSC" : raw_list_bsc,
                    "POLY" : raw_list_poly,
                    "ETH" : raw_list_eth,
                    "ARBI" : raw_list_arbi,
                    "TRON" : raw_list_tron
                    }
                }}))

        return "Done" 
    ####### End Main Menu Block ######
    
    ###### Account Block ######
        #### Eth Transfer Block
    elif conversation_level == "eth_transfer":
        print (f"{name} wants to make raw eth transfer")
        if ETHERS.is_address(chain, message) == True:
            messenger.send_message(
                message=f"""
Please enter the amount of {ETHERS.base(chain)["base"]} you would like to transfer            
                """, recipient_id=mobile
            )
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethamount"}}))
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"trans_acc": message}}))        
        elif isNumber(message) == True:
            my_number = phonenumbers.parse(message, "NG")
            new_num = phonenumbers.format_number(my_number, phonenumbers.PhoneNumberFormat.E164)
            ng_mobile = new_num.replace("+", "")
            try:
                recipient = ""
                use_num = CLIENT.query(q.get(q.ref(q.collection("userData"), ng_mobile)))
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    recipient = use_num["data"]["address"]["evm_address"][0]
                elif chain == "TRON":
                    recipient = use_num["data"]["address"]["tvm_address"][0]
                messenger.send_message(
                    message=f"""
Please enter the amount of {ETHERS.base(chain)["base"]} you would like to transfer            
                    """, recipient_id=mobile
                )
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethamount"}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"trans_acc": recipient}}))
            except:
                messenger.send_reply_noheader(button={
    "body": (f"""
Hi {name}, 
The phone number you have entered does not have an account with NOVICHAIN at the moment
    """),
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "transfer eth",
            "title": "Re-Enter Number" 
        }
        },{
        "type": "reply",
        "reply": {
            "id": "my account",
            "title": "Back To Account" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)

        elif isUserName(message) == True:
            try:
                recipient : str = ""
                id_user = getIdByUser(message)
                use_num = CLIENT.query(q.get(q.ref(q.collection("tele_userData"), id_user)))
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    recipient = use_num["data"]["address"]["evm_address"][0]
                
                elif chain == "TRON":
                    recipient = use_num["data"]["address"]["tvm_address"][0]
                messenger.send_message(
                    message=f"""
Please enter the amount of {ETHERS.base(chain)["base"]} you would like to transfer            
                    """, recipient_id=mobile
                )
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethamount"}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"trans_acc": recipient}}))
            
            except:
                messenger.send_reply_noheader(button={
    "body": (f"""
Hi {name}, 
The username you have entered does not have an account with NOVICHAIN at the moment
    """),
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "transfer eth",
            "title": "Re-Enter Number" 
        }
        },{
        "type": "reply",
        "reply": {
            "id": "my account",
            "title": "Back To Account" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)

        
        else:
            messenger.send_message(
                message=f"""
What you have entered is not any of the following:

Address
Whatsapp Phone Number
Telegram username

Please try again
                """, recipient_id=mobile
            )
        return "Done"
#
            #### Transfer Amount
    elif conversation_level == "ethamount":
        print (f"{name} is about to complete eth transfer with password")
        _chain = ETHERS.base(chain)
        decimal = _chain["decimal"]
        if isfloat(message) == True or isInt(message) == True:
            upamount = math.floor((float(message))*(10**(decimal)))
            norm_bal = ETHERS.base_bal(chain, state, address)
            user_bal = ""
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                user_bal = norm_bal
            if chain == "TRON":
                user_bal = math.floor((float(norm_bal))*(10**(decimal)))
            print(f"{upamount}")
            if user_bal > upamount:
                print("Working")
                messenger.send_message(
                    message=f"""
You are about to transfer {message} {ETHERS.base(chain)['base']}

From: {address}
To: {trans_acc}

Please enter your NOVICHAIN password to continue
                    """, recipient_id=mobile
                )
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethpassword"}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"amount": message}}))

            else:
                print("Insufficient Balance")
                raw_bal = int(ETHERS.base_bal(chain, state, address))
                real_bal = ""
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                if chain == "TRON":
                    real_bal = str(round(int(raw_bal), 3))
                messenger.send_reply_nofooter(button={
"header": "Insufficient Funds",
"body": (f"""
You do not have enough {ETHERS.base(chain)["base"]} to complete this transaction

Your Balance: {real_bal} {ETHERS.base(chain)['base']}"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "eth_transfer_amount",
        "title": "Re-Enter Amount" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
        else:
            messenger.send_message(
                message=f"""
I'm sorry 
You just entered an invalid amount 
Please try again
                """, recipient_id=mobile
            )           
#       
            #### Password
    elif conversation_level == "ethpassword":
        print (f"{name} has put in their password")
        if message == tkey:
            print (f"{name} has entered the right password")
            _chain = ETHERS.base(chain)
            decimal = _chain["decimal"]
            upamount = (int(float(amount)*10**(int(decimal))))
            norm_bal = ETHERS.base_bal(chain, state, address)
            user_bal = ""
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                user_bal = norm_bal
            if chain == "TRON":
                user_bal = math.floor((float(norm_bal))*(10**(decimal)))
            if int(user_bal) > int(upamount):
                print("I'm at this level now")
                try:
                    trans_link = ETHERS.send_eth(chain, state, address, trans_acc, upamount, key)
                    messenger.send_reply_nofooter(button={
"header": "Transaction Successful",
"body":f"""You sent {amount} {_chain["base"]} to {trans_acc}

Proceed to: {trans_link} to view transaction
                    """,
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
                    CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))

                    return "Done"
                except Exception as e:
                    print(e)
                    raw_bal = int(ETHERS.base_bal(chain, state, address))
                    real_bal = ""
                    if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                        real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                    if chain == "TRON":
                        real_bal = str(round(int(raw_bal), 3))
                    messenger.send_reply_nofooter(button={
"header": "Transaction Failed",
"body": (f"""
Insufficient Funds

You do not have enough {ETHERS.base(chain)["base"]} to pay gas fees for this transaction

Your Balance: {real_bal} {ETHERS.base(chain)['base']}"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "eth_transfer_amount",
        "title": "Re-Enter Amount" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
            else:
                raw_bal = int(ETHERS.base_bal(chain, state, address))
                real_bal = ""
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                if chain == "TRON":
                    real_bal = str(round(int(raw_bal), 3))
                messenger.send_reply_nofooter(button={
"header": "Transaction Failed",
"body": (f"""
Insufficient Funds

You do not have enough {ETHERS.base(chain)["base"]} to pay gas fees for this transaction

Your Balance: {real_bal} {ETHERS.base(chain)['base']}"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "eth_transfer_amount",
        "title": "Re-Enter Amount" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)

        else:
            messenger.send_reply_nofooter(button={
"header": "Transaction Failed",
"body": (f"""
Incorrect Password
"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "eth_transfer_password",
        "title": "Re-Enter Password" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Back To Account" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
#
        #### Token Tansfer Block
    elif conversation_level == "token_transfer":
        print (f"{name} is about to enter token amount for tansfer")
        token_deets = ETHERS.token_details(chain, state, token_address)
        if ETHERS.is_address(chain, message) == True:       
            messenger.send_message(
                message=f"""
Please enter the amount of {token_deets["symbol"]} you would like to transfer            
                """, recipient_id=mobile
            )
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "token_amount"}}))
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"trans_acc": message}}))

        elif isNumber(message) == True:
            my_number = phonenumbers.parse(message, "NG")
            new_num = phonenumbers.format_number(my_number, phonenumbers.PhoneNumberFormat.E164)
            ng_mobile = new_num.replace("+", "")
            try:
                recipient = ""
                use_num = CLIENT.query(q.get(q.ref(q.collection("userData"), ng_mobile)))
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    recipient = use_num["data"]["address"]["evm_address"][0]
                elif chain == "TRON":
                    recipient = use_num["data"]["address"]["tvm_address"][0]
                messenger.send_message(
                message=f"""
    Please enter the amount of {token_deets['symbol']} you would like to transfer            
                    """, recipient_id=mobile
                )
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "token_amount"}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"trans_acc": recipient}}))

                return "Done"
            except:
                messenger.send_reply_noheader(button={
"body": (f"""
Hi {name}, 
The phone number you have entered does not have an account with NOVICHAIN at the moment
"""),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "re_transfertokens",
        "title": "Re-Enter Number" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Back To Account" 
    }
    }
] 
}
}, recipient_id=mobile)
        
        elif isUserName(message) == True:
            try:
                recipient : str = ""
                id_user = getIdByUser(message)
                use_num = CLIENT.query(q.get(q.ref(q.collection("tele_userData"), id_user)))
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    recipient = use_num["data"]["address"]["evm_address"][0]
                
                elif chain == "TRON":
                    recipient = use_num["data"]["address"]["tvm_address"][0]
                messenger.send_message(
                message=f"""
    Please enter the amount of {token_deets['symbol']} you would like to transfer            
                    """, recipient_id=mobile
                )
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "token_amount"}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"trans_acc": recipient}}))
            
            except:
                messenger.send_reply_noheader(button={
    "body": (f"""
Hi {name}, 
The username you have entered does not have an account with NOVICHAIN at the moment
    """),
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "re_transfertokens",
            "title": "Re-Enter Username" 
        }
        },{
        "type": "reply",
        "reply": {
            "id": "my account",
            "title": "Back To Account" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)
     
        else:
            messenger.send_message(
                message=f"""
What you have entered is not any of the following:

Address
Whatsapp Phone Number
Telegram username

Please try again
                """, recipient_id=mobile
            )
        return "Done"
#
            #### Transfer Amount
    elif conversation_level == "token_amount":
        print (f"{name} is about to complete token transfer with password")
        token_deets = ETHERS.token_details(chain, state, token_address)
        if isfloat(message) == True or isInt(message) == True:
            upamount = math.floor(float(message))*(10**(int(token_deets["decimal"])))
            user_bal = ETHERS.token_bal(chain, state, address, token_address)
            real_token_bal = str(round(user_bal/(10**(int(token_deets["decimal"]))), 3))
            print(f"{upamount}")
            if user_bal > upamount:
                messenger.send_message(
                    message=f"""
You are about to transfer {message} {token_deets['symbol']} 

From: {address}
To: {trans_acc}

Please enter your NOVICHAIN password to continue
                    """, recipient_id=mobile
                )
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "tokenpassword"}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"amount": message}}))
            else:
                print("Insufficient Balance")
                _chain = ETHERS.base(chain)
                decimal = _chain["decimal"]
                raw_bal = int(ETHERS.base_bal(chain, state, address))
                real_bal = ""
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                if chain == "TRON":
                    real_bal = str(round(int(raw_bal), 3))
                messenger.send_reply_nofooter(button={
"header": "Insufficient Funds",
"body": (f"""
You do not have enough {token_deets['symbol']} to complete this transaction

Your Balance: 
{real_token_bal} {token_deets["symbol"]}

{real_bal} {ETHERS.base(chain)['base']}"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "token_transfer_amount",
        "title": "Re-Enter Amount" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
        else:
            messenger.send_message(
                message=f"""
I'm sorry 
You just entered an invalid amount 
Please try again
                """, recipient_id=mobile
            )                 
#
            #### Password
    elif conversation_level == "tokenpassword":
        print(f"{name} has put their password to make token transfer")
        if message == tkey:
            print (f"{name} has entered the right password")
            token = ETHERS.token_details(chain, state, token_address)
            upamount = float(amount)*10**(int(token["decimal"]))
            user_bal = ETHERS.token_bal(chain, state, address, token_address)
            real_token_bal = str(round(user_bal/(10**(int(token["decimal"]))), 3))
            if int(user_bal) > int(upamount):
                try:
                    trans_link = ETHERS.send_token(chain, state, address, trans_acc, math.floor(upamount), token_address, key)
                    messenger.send_reply_nofooter(button={
"header": "Transaction Successful",
"body":f"""You sent {amount} {token['symbol']} to {trans_acc}

Proceed to: {trans_link} to view transaction
                    """,
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
                    CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))
                    return "Done"
                except Exception as e:
                    print(e)
                    _chain = ETHERS.base(chain)
                    decimal = _chain["decimal"]
                    raw_bal = int(ETHERS.base_bal(chain, state, address))
                    real_bal = ""
                    if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                        real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                    if chain == "TRON":
                        real_bal = str(round(int(raw_bal), 3))
                    messenger.send_reply_nofooter(button={
"header": "Transaction Failed",
"body": (f"""
Insufficient Funds

Hello {name},
You do not have enough {ETHERS.base(chain)["base"]} to pay gas fees for this transaction

Your Balance: 
{real_token_bal} {token["symbol"]}

{real_bal} {ETHERS.base(chain)['base']}"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "token_transfer_amount",
        "title": "Re-Enter Amount" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)

            else:
                messenger.send_reply_nofooter(button={
"header": "Transaction Failed",
"body": (f"""
Insufficient Funds

Hello {name},
You do not have enough {token['symbol']} tokens to complete this transaction

Your Balance: {ETHERS.base_bal(chain, state, address)} {ETHERS.base(chain)['base']}"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Go To Back" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
        else:
            messenger.send_reply_nofooter(button={
"header": "Transaction Failed",
"body": (f"""
Incorrect Password
"""
         ),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "token_transfer_password",
        "title": "Re-Enter Password" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Back To Account" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }
] 
}
}, recipient_id=mobile)
            return "Done"
#
        #### Import Token Block
    elif conversation_level == "import_token":
        print(f"{name} just entered token address to import")
        if message in tokens:
            print(f"{name} tried to import a token twice")
            messenger.send_reply_noheader(button={
"body": (f"""
Hi {name},

You have already imported this token
            """),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Return to Account" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }

] 
}
}, recipient_id=mobile)
        else:
            try:
                token = ETHERS.token_details(chain, state, message)
                raw_token_bal = int(ETHERS.token_bal(chain, state, address, message))
                real_token_bal = str(round(raw_token_bal/(10**(token["decimal"])), 3))
                messenger.send_reply_noheader(button={
        "body": (f"""
You are about to Import:
Token Name: {token["name"]}
Token Symbol: {token["symbol"]}
Token Decimal: {token["decimal"]}
Your Current Balance: {real_token_bal} {token['symbol']}

                    """),
        "action": {
        "buttons": [
            {
            "type": "reply",
            "reply": {
                "id": f"confirmnewtoken {message}",
                "title": "Confirm" 
            }
            },{
            "type": "reply",
            "reply": {
                "id": "my account",
                "title": "Back To Account" 
            }
            }

        ] 
        }
        }, recipient_id=mobile)
                return "Done"
            except Exception as e:
                messenger.send_message(
                        message=f"""
Hello {name},
The address you sent is not a Token on this chain 
Please confirm address and try again
""", recipient_id=mobile
                    )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))      
#       
        #### Balance Check Block
    elif conversation_level == "check_balance":
        print(f"{name} has typed their password to check their balance")
        if message == tkey:
            print(f"{name} has typed the right password")
            ##Remember to iterate through imported token balances
            token_print = ""
            _chain = ETHERS.base(chain)
            for i in tokens:
                token_details = ETHERS.token_details(chain, state,  i)
                token_balance = ETHERS.token_bal(chain, state, address, i)
                if tokens.index(i) > 2 and token_balance == 0:
                    pass
                else:
                    raw_token_bal = int(ETHERS.token_bal(chain,state, user_address = address, token_address = i))
                    real_token_bal = str(round(raw_token_bal/(10**int(token_details['decimal'])), 3))
                    token_print += f"{token_details['name']}: {real_token_bal} {token_details['symbol']} \n"
            raw_bal = int(ETHERS.base_bal(chain, state,  address))
            real_bal = ""
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
            if chain == "TRON":
                real_bal = str(round(int(raw_bal), 3))
            messenger.send_message(
                message=f"""
Your {(ETHERS.base(chain))["base"]} balance is {real_bal} {(ETHERS.base(chain))["base"]}

TOKENS:

{token_print}
                """, recipient_id=mobile
            )
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))

        else:
            print(f"{name} has typed in the wrong password")
            messenger.send_reply_noheader(button={
"body": (f"""
Incorrect Password
Please Retype your Password

            """),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Return to Account" 
    }
    }

] 
}
}, recipient_id=mobile)
#
        #### Import Account Block
            #####Import With Key
    elif conversation_level == "import_account_key":
        print(f"{name} is about to add a new account to their address list with private key")
        _chain = ETHERS.base(chain)
        addr = ""
        keys = ""
        account = ""
        try:
            account = ETHERS.key_to_account(chain, message)
            new_address = account['address']
            raw_bal = int(ETHERS.base_bal(chain, state, new_address))
            real_bal = ""
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                addr = using["data"]["address"]["evm_address"]
                keys = using["data"]["key"]["evm_key"]
                addr.append(new_address)
                keys.append(message)
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"address": {"evm_address": addr}}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"key": {"evm_key": keys}}}))
            elif chain == "TRON":
                addr = using["data"]["address"]["tvm_address"]
                real_bal = str(round(int(raw_bal), 3))
                keys = using["data"]["key"]["tvm_key"]
                addr.append(new_address)
                keys.append(message)
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"address": {"tvm_address": addr}}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"key": {"tvm_key": keys}}}))
            
            messenger.send_reply_nofooter(button={
    "header": "Import Successful",
    "body":f"""You have successfully added a new address to your account 
New Address:
{new_address}

Balance:
{real_bal} {(ETHERS.base(chain))["base"]}

                    """,
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
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))
            
        except Exception as e:
            print(e)
            print(account)
            messenger.send_reply_nofooter(button={
    "header": "Import Failed",
    "body":f"""Hello {name}
The private key you provided is invalid 
Please try again
                    """,
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "importaccount",
            "title": "Try Again" 
        }
        },{
        "type": "reply",
        "reply": {
            "id": "BackToStart",
            "title": "Main Menu" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))
#
#           #####Import With Phrase            
    elif conversation_level == "import_account_phrase":
        print(f"{name} is about to add a new account to their address list with seed phrase")
        _chain = ETHERS.base(chain)
        addr = ""
        keys = ""
        account = ""
        try:
            account = ETHERS.phrase_to_account(chain, message)
            new_address = account['address']
            new_key = account['key']
            raw_bal = int(ETHERS.base_bal(chain, state, new_address))
            real_bal = ""
            if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                addre = using["data"]["address"]["evm_address"]
            else:
                addre = using["data"]["address"]["tvm_address"]

            if new_address in addre:
                messenger.send_reply_nofooter(button={
    "header": "Import Failed",
    "body":f"""You have already imported this address
New Address:
{new_address}

Balance:
{real_bal} {(ETHERS.base(chain))["base"]}

                    """,
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
            else:
                if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
                    real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
                    addr = using["data"]["address"]["evm_address"]
                    keys = using["data"]["key"]["evm_key"]
                    addr.append(new_address)
                    keys.append(new_key)

                    keys.append(message)
                    CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"address": { "evm_address" :  addr}}}))
                    CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"key": { "evm_key" : keys}}}))
                elif chain == "TRON":
                    real_bal = str(round(int(raw_bal), 3))
                    addr = using["data"]["address"]["tvm_address"]
                    keys = using["data"]["key"]["tvm_key"]
                    addr.append(new_address)
                    keys.append(new_key)
                    CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"address": { "tvm_address" : addr}}}))
                    CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"key": { "tvm_key" :  keys}}}))  
                messenger.send_reply_nofooter(button={
        "header": "Import Successful",
        "body":f"""You have successfully added a new address to your account 
    New Address:
    {new_address}

    Balance:
    {real_bal} {(ETHERS.base(chain))["base"]}

                        """,
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
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))
        except Exception as e:
            print(e)
            print(account)
            messenger.send_reply_nofooter(button={
    "header": "Import Failed",
    "body":f"""Hello {name}
The seed phrase you provided is invalid 
Please try again
                    """,
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "importaccount",
            "title": "Try Again" 
        }
        },{
        "type": "reply",
        "reply": {
            "id": "BackToStart",
            "title": "Main Menu" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))

    elif conversation_level == 'export_account':
        address_index = token_address
        pkey = ""
        addr = ""
        if chain in ["ETH", "ARBI", "POLY", "BSC", "ETHW"]:
            pkey = using["data"]["key"]["evm_key"][int(address_index)]
            addr = using["data"]["address"]["evm_address"][int(address_index)]
        elif chain == "TRON":
            pkey = using["data"]["key"]["tvm_key"][int(address_index)]
            addr = using["data"]["address"]["tvm_address"][int(address_index)]

        if message == tkey:
            messenger.send_reply_nofooter(button={
    "header": "Export Successful",
    "body":f"""
Address:
{addr}

Private Key:
{pkey}

Warning ⚠:
Do not disclose your private key to anyone
                    """,
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "my account",
            "title": "Back To Account" 
        }
        },{
        "type": "reply",
        "reply": {
            "id": "BackToStart",
            "title": "Main Menu" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))
        else:
            messenger.send_reply_noheader(button={
"body": (f"""
"Export Failed"

Incorrect Password

            """),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "re_export",
        "title": "Re-Enter Password" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Return to Account" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "main menu",
        "title": "Main Menu" 
    }
    }

] 
}
}, recipient_id=mobile)
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": ""}}))       
    ###### Unknown Text ######
    else:
        print (f"{name} sent a message with no response")
        messenger.send_reply_nofooter(button={
"header": "Unknown words",
"body": (f"""Hello there {name}, I don't really understand what you have just said, would you mind saying something else?"""),
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