from faunadb.client import FaunaClient
from heyoo import WhatsApp
from web3_hooks import WEBPY
import os



############### Admin Codes ###############
fauna_secret = "fnAFAZYyLKAAUY3-ZL5ntrRfZBPfifwOvF-EUD8v"
CLIENT = FaunaClient(secret=fauna_secret, domain="db.us.fauna.com")
messenger = WhatsApp(token ="EAAXKtiII4zwBOZC0siUnpEF1cfEjiWfL9vL24saXKTA88OF9wVrFCR06MwKPJfnaXc7k2zDDBger8DKhbwDvrlmkPbIUeFAK0eFHGTJeBTwnKIJoO5zar3HYrb0uNwk8VwHKDZBKZALMHWELVQG4EZBKgZCZByvhzZCyq0lRG2t8BEExplprIhlIbLKybmENvEGjexPBl0ZAnBJIuExyTibNoxDMKnMZD", phone_number_id="257257560810302") #You can use any random characters in here
TOKEN = os.getenv("TOKEN") #application secret here
ETHERS = WEBPY()
############### Admin Codes ###############

"""
if request.method == "GET":
        if request.args.get("hub.verify_token") == "heroku whatsapp token":
            responsed = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        return "Invalid verification token"
    data = request.get_json()

BECOMES

if request.method == "GET":
    response = make_response(request.args.get("hub.challenge"), 200)
    response.mimetype = "text/plain"
    return response

    data = request.get_json()

    

    {
    
tokens: {
    ETH: [],
    BSC: [
      "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd",
      "0x64544969ed7EBf5f083679233325356EbE738930",
      "0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee"
    ],
    POLY: [],
    ARBI: []
  },
state: [],

{
  id: "2348077642325",
  conversation_level: "ethamount",
  trans_acc: "0x248EE58d8A0E682181204Eb06b16A2f898D030c6",
  address: {
      evm_address: [
        "0x248EE58d8A0E682181204Eb06b16A2f898D030c6",
        "0x59eA7e5F4d8718034861f7724b8376581e93D550"
        ],
      "tvm_address": [
        "TP3yxca8KuWTpXoe29MsjmZ53jLzzLSYS9",
        "TQEqNWBPFpDpp52VEWUraobPGiAZir7uVz"
      ]
  },
  key: {
      evm_key: [
        "0x343f6a5a8453e1e5b41acc6079570cad685033beab2eb0b2590b22f1d3c411ea",
        "b46b3f9d077787c5f78ddba26dc6980b7000e307d0928b95a59c7b00fb34a3a7"
    ],
      "tvm_key": [
        "e1fd2025e5fd43529adcf52f3ed6db0350102174f6bb96202fe07f4359b22976",
        "7446fbe3a23e47fe03ad834258befd02720061a9eb5b829277c373edf9809c72"
      ]
  },
  sale_type: "",
  token_address: "0x6dd4546917b2ff494a2c8307dcb1550149e78999",
  tokens: {
    ETH: [],
    BSC: [
      "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd",
      "0x64544969ed7EBf5f083679233325356EbE738930",
      "0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee"
    ],
    POLY: [],
    ARBI: [],
    ETHW: []
  },
  state: "testnet",
  tkey: "1234",
  chain: "BSC",
  default: "1",
  amount: "100000000000000000000000000",
  signed: "Done"
}


{
  id: "2347039182352",
  conversation_level: "",
  trans_acc: "0x248EE58d8A0E682181204Eb06b16A2f898D030c6",
  address: {
      evm_address: [
        "0x41a7b616eE4258A8166576d0fD7cf2747dBC68F7",
        "0xC386dA46A64C0cE2F9824C9C929F575c0961A5d3",
        "0x3bC1851CB7C374DEd00753291De9FD137604C7A3"
        ],
      tvm_address: [
        "TXjWErhpqNLyMRBV25ji7t49dmkBpkBsBL"
      ],
  },
  key: {
      evm_key: [
        "0x8c3220d5b74ce935a526dc6d3bf928cca6039b95ee97acbece43506976278abd",
        "21030e823b9df4f89986f41d056da1a976131de5df193e42fbf2d81f02f2ada5",
        "2b30d7fa0d1cb7c0bf31efbac18a7b6c7817ef2a821d8b5b81493b000c75ee2a"
    ],
      tvm_key: [
        "98fff707ff493479048da30b5596fd019e06ce76100b36c27fafa429cafb5cae"
      ]
  },
  token_address: "",
  tokens: {
    ETH: [],
    BSC: [
      "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd",
      "0x64544969ed7EBf5f083679233325356EbE738930",
      "0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee",
      "0x6Dd4546917B2FF494a2C8307DCB1550149E78999",
      "0x7533552d45a1050796485bf07e71cd5764a2bf5d"
    ],
    POLY: [],
    ARBI: [],
    ETHW: []
  },
  state: "testnet",
  tkey: "123456",
  chain: "BSC",
  default: "2",
  amount: "0.01",
  signed: "Done"
}


{
  id: "2349050791379",
  conversation_level: "import_token",
  trans_acc: "0x41a7b616eE4258A8166576d0fD7cf2747dBC68F7",
  address: {
    evm_address: ["0x037FC3241d0F7AD030A61C1E5E1edA8D93a164f1"],
    "tvm_address": [
        "TMSZJV5ZDYqWjU2YFS7j3QPMFF4APVuJ2C"
      ]
  },
  key: {
      evm_key: [
        "0x82fcec66dde277d19f2c253b4871a6438649968d4100e4490289244c8f0911ef"
    ],
      tvm_key: [
        "e3dc2be009003c804a29390f8165cec484d464f20b0afecf899e5ce153b2ac7e"
      ]
  },
  token_address: "",
  tokens: {
    ETH: [],
    BSC: [
      "0x337610d27c682E347C9cD60BD4b3b107C9d34dDd",
      "0x64544969ed7EBf5f083679233325356EbE738930",
      "0xeD24FC36d5Ee211Ea25A80239Fb8C4Cfd80f12Ee"
    ],
    POLY: [],
    ARBI: [],
    ETHW: []
  },
  state: "testnet",
  tkey: "111111",
  chain: "BSC",
  default: 0,
  amount: "0.05",
  signed: "Done"
}

"""