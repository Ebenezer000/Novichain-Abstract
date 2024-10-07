from faunadb.client import FaunaClient
from heyoo import WhatsApp
from web3_hooks import WEBPY
import os

############### Admin Codes ###############
fauna_secret = "fnAFAZYyLKAAUY3-ZL5ntrRfZBPfifwOvF-EUD8v"
CLIENT = FaunaClient(secret=fauna_secret, domain="db.us.fauna.com")
messenger = WhatsApp(token ="EAAXKtiII4zwBO9cZCav9yZC62kWbPJTs2djodZAWv2TthAYeTROIuOnphZAgEzr5VIlnXEeZBULgnnUW5p5u68EJ0TD8ZCtf2vZBgdlRKRpjSFYBrdtJpdjvvXmFXRFJy5uOuniqDnAVukAC8dHWikpNRyFOuGi0JTVnBKm4o0NRZBsnEBDVMSXXEIaJEsOoOsORZBPgI5PtYayX7FrxJM9oQMxwFM8QZD", phone_number_id="257257560810302") #You can use any random characters in here
TOKEN = os.getenv("TOKEN") #application secret here
ETHERS = WEBPY()
############### Admin Codes ###############
