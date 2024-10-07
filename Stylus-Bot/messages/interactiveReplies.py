from adminControls.adminCodes import CLIENT,messenger,ETHERS
from faunadb import query as q
import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
###############Interactive Message Handler##############

def isNumber(num) -> bool:
    my_number = phonenumbers.parse(num, "NG")
    can = phonenumbers.is_valid_number(my_number)
    return can


def interactivebuttons(data):
    """
    Interactive message handler to handle Interactive messages

    :param: data carries message data (mobile number and message load)
    
    """
    mobile = messenger.get_mobile(data)
    message_array = messenger.get_interactive_response(data)
    name = messenger.get_name(data)
    message = ""
    id = ""
    id_message = ""
    id_tag = ""
    using = CLIENT.query(q.get(q.ref(q.collection("userData"), mobile)))

    default = using["data"]["default"]
    address = address = using["data"]["address"]
    chain = using["data"]["chain"]
    tokens = ""
    if address == [] and chain == "":
        address = address = using["data"]["address"]
        addresses = using["data"]["address"]
    else:
        if chain in ["ARBI_TEST", "ARBI"]:
            try:
                address = using["data"]["address"]["evm_address"][int(default)]
            except:
                address = using["data"]["address"]["evm_address"][0]
            addresses = using["data"]["address"]["evm_address"]
            tokens = using["data"]["tokens"][chain]

    signed = using["data"]["signed"]
    token_address = using["data"]["token_address"]
    state = using["data"]["state"]
    trans_acc = using["data"]["trans_acc"]
    amount = using["data"]["amount"]


    try:
        message = message_array[0]
        id = message_array[1]
        id_seperated = id.split() #return id as array
        try:
            id_message = id_seperated[0] #pure id to lower case for tests and conditionals
            id_tag = id_seperated[1]
        except:
            pass
    except:
        message = message_array      
    if isinstance(message, dict):
        message = message_array["title"]
        id = message_array["id"]
        message_seperate = id.split()
        id_message = message_seperate[0]
        try:
            id_tag = message_seperate[1]
        except:
            pass
        p_message = message.lower() #pure message to lower case for tests and conditionals
    else:
        p_message = message.lower() #pure message to lower case for tests and conditionals

    ########Main Menu Block########
    if p_message in ['hello', "0", "hi", "main", "menu", "main menu", "good morning", "good afternoon", "start app", "start", "hey", "how are you"]:
        print (f"{name} activated main menu with {message}")
        if signed == "":
            messenger.send_reply_noheader(button={
"body": (f"""
Hi {name}, 
Welcome to Novichain

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
#        
        else:
            _chain = ETHERS.base(chain)
            chain_name = _chain['chain_name']
            messenger.send_reply_noheader(button={
"body": (f"""
Hi {name},
What would you like to do today

Current Chain: {chain_name}"""),
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
        return "Done"
#
    if p_message == "create account":
        print (f"{name} want's to set up transaction password")
        messenger.send_message(
            message=f"""
In one basic step your account would be setup {name},

Enter a 6 Digit Transaction password you can remember below 

WARNING ⚠:
Do not disclose this with anyone
""", recipient_id=mobile)
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "transkey"}}))
    ######## End Main Menu Block########

    ######## Account Block########
    elif p_message == "account" or id == "my account":
        print (f"{name} just entered account options")
        _chain = ETHERS.base(chain)
        chain_name = _chain['chain_name']
        messenger.send_button_nofooter(button={
"body": f"""Hello {name},
What would you like to do on your Novichain Account today

Current Chain: {chain_name}
            """,
"action": {
"button": "Account Options",
"sections":[
    {
    "title":"Account Options",
    "rows": [
            {
            "id":"send",
            "title": f"SEND",
            },{
            "id":"receive",
            "title": "RECEIVE",
            },{
            "id":"viewtokens",
            "title": "VIEW ASSETS",
            },{
            "id":"check balance",
            "title": "CHECK BALANCE",
            },{
            "id":"import tokens",
            "title": "ADD TOKEN",
            },{
            "id":"import account",
            "title": "IMPORT ACCOUNT",
            },{
            "id":"switch account",
            "title": "SWITCH ACCOUNT",
            },{
            "id":"export_account",
            "title": "EXPORT ACCOUNT",
            }
        ]
    }
]
}
}, recipient_id=mobile)
        return "Done"
#
        #### SEND Block ####
    elif p_message == "send":
        print (f"{name} wants to send tokens or eth")
        rows = [{
            "id":"import tokens",
            "title": "Import Tokens",
            "description": "add tokens"
            },{
            "id":"transfer eth",
            "title": f"{ETHERS.base(chain)['base']}",
            }]
        for i in tokens:
            token = ETHERS.token_details(chain, state, i)
            token_balance = ETHERS.token_bal(chain, state, address, i)
            if token_balance == 0 and token["symbol"] not in ["USDT", "USDC", "BUSD"]:
                print("not appending anything")
            else:
                print (f"""appending {token["symbol"]}""")
                new_token = {
                    "id": f"transfertokens {i}",
                    "title": f"""{token["symbol"]}""",
                }
                rows.append(new_token)

        chunked_list = list()
        chunk_size = 10
        for i in range(0, len(rows), chunk_size):
            chunked_list.append (rows[i:i+chunk_size])

        messenger.send_message(
        message=f"""What would you like to send today
        """, recipient_id=mobile)
        for row in chunked_list:
            messenger.send_button_nofooter(button={
"body": f"""
Currency Options
        """,
"action": {
"button": "Select Currency",
"sections":[
{
"title":"Select Currency",
"rows": row
}
]
}
}, recipient_id=mobile)
        return "Done"
#
        #### Eth Transfer Block 
    elif id == "transfer eth":
        print(f"{name} wants to transfer some base currency")
        messenger.send_message(
            message=f"""To transfer {ETHERS.base(chain)["base"]} please enter any of the following 

Address
Whatsapp Phone Number
Telegram username
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "eth_transfer"}}))

        return "Done"
#
            #### Eth Amount Interactive
    elif id == "eth_transfer_amount":
        print (f"{name} wants to make raw eth transfer")
        messenger.send_message(
            message=f"""
Please Re-enter the amount of {ETHERS.base(chain)["base"]} you would like to transfer            
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethamount"}}))
        return "Done"
#
            #### Eth Password Interactive
    elif id == "eth_transfer_password":
        print (f"{name} wants to make raw eth transfer")
        messenger.send_message(
                    message=f"""
You are about to transfer {amount} {ETHERS.base(chain)['base']}

From: {address}
To: {trans_acc}

Please enter your Novichain password to continue
                    """, recipient_id=mobile
                )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethpassword"}}))
        return "Done"
#
            #### Token Transfer Amount
    elif id == "token_transfer_amount":
        print (f"{name} is about to enter token amount for tansfer") 
        token_deets = ETHERS.token_details(chain, state, token_address) 
        messenger.send_message(
        message=f"""
Please Re-enter the amount of {token_deets['symbol']} you would like to transfer            
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "token_amount"}}))
        return "Done"
#
            #### Eth Password Interactive
    elif id == "token_transfer_password":
        print (f"{name} wants to make raw eth transfer")
        token_deets = ETHERS.token_details(chain, state, token_address) 
        messenger.send_message(
                message=f"""
You are about to transfer {message} {token_deets['symbol']} 

From: {address}
To: {trans_acc}

Please enter your Novichain password to continue
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "ethamount"}}))
        return "Done"
#
            #### Transfer Address
    elif id_message == "transfertokens":
        print(f"{name} has selected {p_message} to transfer")
        token = ETHERS.token_details(chain, state, id_tag)
        messenger.send_message(
            message=f"""To transfer {token["symbol"]} please enter any of the following 

Address
Whatsapp Phone Number
Telegram username
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "token_transfer"}}))
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"token_address": id_tag}}))
#

    elif id_message == "re_transfertokens":
        print(f"{name} has selected {p_message} to transfer")
        token = ETHERS.token_details(chain, state, token_address)
        messenger.send_message(
            message=f"""To transfer {token["symbol"]} please enter any of the following 

Address
Whatsapp Phone Number
Telegram username
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "token_transfer"}}))
#

            #### Import Tokens
    elif p_message == "add token" or id == 'import tokens':
        print(f"{name} user would like to import an external token")
        messenger.send_message(
            message=f"""Please enter the address of the token you would like to import
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "import_token"}}))

        return "Done"
#
            #### Confirm New Token
    elif id_message == "confirmnewtoken":
        tokens.append(id_tag)
        messenger.send_reply_noheader(button={
    "body": (f"""
Token Import Successful
                """),
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "my account",
            "title": "Back To Account" 
        }
        }

    ] 
    }
    }, recipient_id=mobile)
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"tokens": { chain: tokens}}}))
        #### Check Balance Block
#
            #### View My tokens
    elif p_message == "view assets":
        print(f"{name} is about to view all the tokens on his account")
        token_print = ""
        for i in tokens:
            token_details = ETHERS.token_details(chain, state, i)
            token_print += f"{token_details['name']}\n"
        messenger.send_reply_nofooter(button={
"header": "My Assets",
"body": (f"""
Hi {name},
Here are the tokens imported to your ChatFi account

TOKENS:
{ETHERS.base(chain)["base"]}
{token_print}
"""),
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
#
            #### Check Balance block
    elif p_message == "check balance" or id == "check balance":
        print (f"{name} wants to check their balance")
        messenger.send_message(
            message=f"""
Please enter your Novichain transaction password

NOTE:
Tokens with 0 Balance will not be displayed
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "check_balance"}}))
        return "Done"
#
            #### Coming Soon Block
    elif p_message == "swap tokens" or p_message == "buy tokens":
        messenger.send_reply_noheader(button={
"body": (f"""Coming Soon"""),
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
#
            #### View Address
    elif p_message == "receive":
        print (f"{name} wants to see their Novichain account address")
        messenger.send_image(
            image = f"https://chart.googleapis.com/chart?chs=250x250&cht=qr&chl={address}", 
            caption = f"Your Novichain address is {address}",
            recipient_id=mobile)
#
            #### Import Account
    elif p_message == "import account" or id == "importaccount":
        messenger.send_reply_nofooter(button={
"header": "Import Method",
"body": (f"""Please select an import method"""),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "private key",
        "title": "Private Key" 
    }
    },{
    "type": "reply",
    "reply": {
        "id": "seed phrase",
        "title": "Seed Phrase" 
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

    elif p_message == "private key":
        print (f"{name} wants to add a new address to their list of addresses with private key")
        messenger.send_message(
            message=f"""Please paste your address private key to continue

WARNING:
Pasting your private key is a security risk to your account
Please delete your key after your message is sent
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "import_account_key"}}))
#
    elif p_message == "seed phrase":
        messenger.send_message(
            message=f"""Please paste your seed phrase to continue

WARNING:
Pasting your seed phrase is a security risk to your account
Please delete your phrase after your message is sent
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "import_account_phrase"}}))
#
            #### Switch Account:
    elif p_message == "switch account":
        print (f"{name} wants  to switch to a different account")
        rows = []
        add_no = 0
        for i in addresses:
            new_address = {
                    "id": f"select_address {add_no} {i}",
                    "title": f"""Address {add_no}""",
                    "description": f"{i[0:6]}...{i[-4: len(i)]}"
                }
            rows.append(new_address)
            add_no += 1
        messenger.send_button_nofooter(button={
"body": f"""
Please Select an address you would like to switch to
        """,
"action": {
"button": "Select Address",
"sections":[
{
"title":"Select Address",
"rows": rows
}
]
}
}, recipient_id=mobile)
#
                #### Select Address
    elif id_message == "select_address":
        print(f"{name} has just selected a new default address")
        message_seperate = id.split()
        id_address = message_seperate[2]
        _chain = ETHERS.base(chain)
        decimal = _chain["decimal"]
        raw_bal = int(ETHERS.base_bal(chain, state, id_address))
        real_bal = ""
        if chain in ["ARBI_TEST", "ARBI"]:
            real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))
        if chain == "TRON":
            real_bal = str(round(int(raw_bal), 3))
        messenger.send_reply_noheader(button={
"body": (f"""
You have successfully switched to a new address
Your Address:
{id_address},
Your Base currency is {(ETHERS.base(chain))["base"]},

You currently own {real_bal} {(ETHERS.base(chain))["base"]}
            """),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "My Account" 
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
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"default": int(id_tag)}}))
    ######## End Account Block########

    elif message == "export account" or id == "export_account":
        rows = []
        add_no = 0
        for i in addresses:
            new_address = {
                    "id": f"select_export {add_no} {i}",
                    "title": f"""Address {add_no}""",
                    "description": f"{i[0:6]}...{i[-4: len(i)]}"
                }
            rows.append(new_address)
            add_no += 1
        messenger.send_button_nofooter(button={
"body": f"""
Please Select an address you would like to export
        """,
"action": {
"button": "Select Address",
"sections":[
{
"title":"Select Address",
"rows": rows
}
]
}
}, recipient_id=mobile)
        
    elif id_message == "select_export":
        message_seperate = id.split()
        id_address = message_seperate[2]
        messenger.send_message(
            message=f"""
Address Selected
{id_address}

To export The private key of this Address,
Please enter your Novichain password
            """, recipient_id=mobile
        )
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"token_address": int(id_tag)}}))
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "export_account"}}))
          
    elif id == "re_export":
        messenger.send_reply_noheader(button={
"body": (f"""
Try Again 

To export your private key,
Please enter your Novichain password
            """),
"action": {
"buttons": [
    {
    "type": "reply",
    "reply": {
        "id": "my account",
        "title": "Cancel" 
    }
    }
] 
}
}, recipient_id=mobile)  
        CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"conversation_level": "export_account"}}))
  
    ####### Switch Chain Block #######
    elif p_message == "switch chain":
        print (f"{name} wants to switch base chain")
        messenger.send_button_nofooter(button={
"body": f"""Hello {name},
Please select a chain you would like to transact on today
            """,
"action": {
"button": "Select Chain",
"sections":[
    {
    "title":"Select Chain",
    "rows": [
            {
            "id":"switchto ARBI",
            "title": "Arbitrum",
            "description": "AGOR"
            },{
            "id":"switchto ARBI_TEST",
            "title": "Arbitrum_test",
            "description": "AGOR_TEST"
            },
        ]
    }
]
}
}, recipient_id=mobile)
        return "Done"
#
    elif id_message == "switchto":
        print(f"{name} has just switched to the {id_tag} chain")

        if id_tag in ["ARBI_TEST", "ARBI"]:
            address = using["data"]["address"]["evm_address"][0]
            _chain = ETHERS.base(id_tag)
            raw_bal = int(ETHERS.base_bal(id_tag, state,  address))
            real_bal = str(round(raw_bal/(10**(int(_chain["decimal"]))), 3))       
            messenger.send_reply_noheader(button={
    "body": (f"""
You have successfully switched to the {ETHERS.base(id_tag)["chain_name"]},
Your Base currency is {ETHERS.base(id_tag)["base"]},

You currently own {real_bal} {ETHERS.base(id_tag)["base"]}
Your address is {address}
                """),
    "action": {
    "buttons": [
        {
        "type": "reply",
        "reply": {
            "id": "main menu",
            "title": "Main Menu" 
        }
        }
    ] 
    }
    }, recipient_id=mobile)
            CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"chain": id_tag}}))
        elif id_tag == "TRON":
            address = using["data"]["address"]["tvm_address"][int(0)]
            _chain = ETHERS.base(id_tag)
            try:
                raw_bal = int(ETHERS.base_bal(id_tag, state, address))
                real_bal = str(round(raw_bal, 3))               
                messenger.send_reply_noheader(button={
        "body": (f"""
You have successfully switched to the {ETHERS.base(id_tag)["chain_name"]},
Your Base currency is {ETHERS.base(id_tag)["base"]},

You currently own {real_bal} {ETHERS.base(id_tag)["base"]}
Your address is {address}
                    """),
        "action": {
        "buttons": [
            {
            "type": "reply",
            "reply": {
                "id": "main menu",
                "title": "Main Menu" 
            }
            }
        ] 
        }
        }, recipient_id=mobile)
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"chain": id_tag}}))
                CLIENT.query(q.update(q.ref(q.collection("userData"), mobile), {"data": {"default": int(0)}}))
            except Exception as e:
                print (e)
                messenger.send_reply_noheader(button={
        "body": (f"""
Hello {name},
Your Tron Wallet address is not activated 

To activate your wallet, please send 1TRX to your address below:

{address}
                    """),
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
                "id": "main menu",
                "title": "Main Menu" 
            }
            }
        ] 
        }
        }, recipient_id=mobile)
        
    ##### End Switch Chain Block #####

    #### UnKnown Interaction #####
    else:
        print (f"{name} used an interactive button with no reply p_message = ({p_message} id = ({id}))")
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
