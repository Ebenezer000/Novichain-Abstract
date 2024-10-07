"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""

import requests
import logging


class WhatsApp(object):
    def __init__(self, token="EAAXKtiII4zwBOZC0siUnpEF1cfEjiWfL9vL24saXKTA88OF9wVrFCR06MwKPJfnaXc7k2zDDBger8DKhbwDvrlmkPbIUeFAK0eFHGTJeBTwnKIJoO5zar3HYrb0uNwk8VwHKDZBKZALMHWELVQG4EZBKgZCZByvhzZCyq0lRG2t8BEExplprIhlIbLKybmENvEGjexPBl0ZAnBJIuExyTibNoxDMKnMZD", phone_number_id="101827599457114"):
        self.token = token
        self.base_url = "https://graph.facebook.com/v14.0"
        self.url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"
        self.headers = {
            "Authorization": "Bearer {}".format(self.token),
            "Content-Type": "application/json",
            
    }
    def send_message(
        self, message, recipient_id, recipient_type="individual", preview_url=True
    ):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        r = requests.post(f"{self.url}", headers=self.headers, json=data)
        return r.json()

    def send_template(self, template, recipient_id, lang="en_US"):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {"name": template, "language": {"code": lang}},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()
    
    def send_loaded_template(self, template, template_load, recipient_id, lang="en_US"):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {"name": template, "components": template_load, "language": {"code": lang}},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_location(self, lat, long, name, address, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "location",
            "location": {
                "latitude": lat,
                "longitude": long,
                "name": name,
                "address": address,
            },
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_image(
        self,
        image,
        recipient_id,
        recipient_type="individual",
        caption=None,
        link=True,
    ):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": image, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"id": image, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()


    def send_audio(self, audio, recipient_id, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"link": audio},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"id": audio},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_video(self, video, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"link": video, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"id": video, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_document(self, document, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"link": document, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"id": document, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def create_button(self, button):
        return {
            "type": "list",
            "header": {"type": "text", "text": button.get("header")},
            "body": {"text": button.get("body")},
            "footer": {"text": button.get("footer")},
            "action": button.get("action"),
        }
    
    def create_button_noheader(self, button):
        return {
            "type": "list",
            "body": {"text": button.get("body")},
            "footer": {"text": button.get("footer")},
            "action": button.get("action"),
        }
    
    def create_button_nofooter(self, button):
        return {
            "type": "list",
            "body": {"text": button.get("body")},
            "action": button.get("action"),
        }

    def create_reply_button(self, button):
        return {
            "type": "button",
            "header": {"type": "text", "text": button.get("header")},
            "body": {"text": button.get("body")},
            "footer": {"text": button.get("footer")},
            "action": button.get("action"),
        }

    def create_reply_no_header(self, button):
        return {
            "type": "button",
            "body": {"text": button.get("body")},
            "action": button.get("action"),
        }

    def create_reply_nofooter(self, button):
        return {
            "type": "button",
            "header": {"type": "text", "text": button.get("header")},
            "body": {"text": button.get("body")},
            "action": button.get("action"),
        }
    
    def create_reply_header(self, button):
        return {
            "type": "button",
            "header": {"type": "image", 
                       "image": {
                                "link": button.get("headerlink"),
                }},
            "body": {"text": button.get("body")},
            "action": button.get("action"),
        }
    
    def create_reply_headernofooter(self, button):
        return {
            "type": "button",
            "header": {"type": "image", 
                       "image": {
                                "link": button.get("headerlink"),
                }},
            "body": {"text": button.get("body")},
            "action": button.get("action"),
        }

    def send_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()
    
    def send_button_noheader(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button_noheader(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()
    
    def send_button_nofooter(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button_nofooter(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()
    
    def send_reply_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_reply_button(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_reply_noheader(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_reply_no_header(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_reply_nofooter(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_reply_nofooter(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_reply_header(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_reply_header(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_reply_headernofooter(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_reply_headernofooter(button),
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def preprocess(self, data):
        return data["entry"][0]["changes"][0]["value"]

    def get_mobile(self, data):
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]

    def get_name(self, data):
        contact = self.preprocess(data)
        if contact:
            return contact["contacts"][0]["profile"]["name"]

    def get_message(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["text"]["body"]

    def get_message_id(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["id"]

    def get_message_timestamp(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["timestamp"]

    def get_interactive_response(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            try:
                return data["messages"][0]["interactive"]["list_reply"]
            except:
                title = data["messages"][0]["interactive"]["button_reply"]["title"]
                id = data["messages"][0]["interactive"]["button_reply"]["id"]
                return [title,id]

    def get_message_type(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["type"]
    
    def query_media_url(self, media_id: str):
        """
        Query media url from media id obtained either by manually uploading media or received media
        Args:
            media_id[str]: Media id of the media
        Returns:
            str: Media url
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.query_media_url("media_id")
        """

        logging.info(f"Querying media url for {media_id}")
        r = requests.get(f"{self.base_url}/{media_id}", headers=self.headers)
        if r.status_code == 200:
            logging.info(f"Media url queried for {media_id}")
            return r.json()["url"]
        logging.info(f"Media url not queried for {media_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return None

    def download_media(self, media_url: str, mime_type: str, file_path: str = "temp"):
        """
        Download media from media url obtained either by manually uploading media or received media
        Args:
            media_url[str]: Media url of the media
            mime_type[str]: Mime type of the media
            file_path[str]: Path of the file to be downloaded to. Default is "temp"
                            Do not include the file extension. It will be added automatically.
        Returns:
            str: Media url
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.download_media("media_url", "image/jpeg")
            >>> whatsapp.download_media("media_url", "video/mp4", "path/to/file") #do not include the file extension
        """
        r = requests.get(media_url, headers=self.headers)
        content = r.content
        extension = mime_type.split("/")[1]
        # create a temporary file
        try:
            save_file_here = (
                f"{file_path}.{extension}" if file_path else f"temp.{extension}"
            )
            with open(save_file_here, "wb") as f:
                f.write(content)
            return f.name
        except Exception as e:
            print(e)
            print("Error downloading media to {save_file_here}")
            logging.info(f"Error downloading media to {save_file_here}")
            return None

    def get_image(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            if "image" in data["messages"][0]:
                return data["messages"][0]["image"]

    def get_delivery(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["status"]

    def changed_field(self, data):
        return data["entry"][0]["changes"][0]["field"]
