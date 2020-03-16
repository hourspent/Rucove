import requests
import json
from root.DB_links import get_product_by_image, quick_product_stage


# # Facebook Page Access Token
page_access_token = "EAANQWM038XUBAGbzTDWh5PDMMLTO38c1cKOGirwHB9ZALg4RZAm52v26PZBVEihRLD7d2p3Ep0Bp4Arjt5DeB5oMlkAZCrwUtqbBeZBBeFMKXuMMCJOF3oJKJzxoHXLbgrBQl9OtCBU96wb9JSGjyilxSKX5P13s3vTUrZCEJtHQB1rPjbXwz3"


#
#
# # This function sends back a message to the user base on the user request
def send_message(sender_id, message_text):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

                      params={"access_token": page_access_token},

                      headers={"Content-Type": "application/json"},

                      data=json.dumps({
                          "recipient": {"id": sender_id},
                          "message": {"text": message_text}
                      }))


#
#
# # This is a quick reply function that gives users option for their replies
def quick_response(sender_id, message_text, title1, title2, postcard1="", postcard2=""):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

                      params={"access_token": page_access_token},

                      headers={"Content-Type": "application/json"},

                      data=json.dumps({
                          "recipient": {"id": sender_id},
                          "messaging_type": "RESPONSE",
                          "message": {
                              "text": message_text,
                              "quick_replies": [
                                  {
                                      "content_type": "text",
                                      "title": title1,
                                      "payload": postcard1
                                  }, {
                                      "content_type": "text",
                                      "title": title2,
                                      "payload": postcard2
                                  }
                              ]
                          }
                      }))


def quick_response_one(sender_id, message_text, title1, postcard1=""):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

                      params={"access_token": page_access_token},

                      headers={"Content-Type": "application/json"},

                      data=json.dumps({
                          "recipient": {"id": sender_id},
                          "messaging_type": "RESPONSE",
                          "message": {
                              "text": message_text,
                              "quick_replies": [
                                  {
                                      "content_type": "text",
                                      "title": title1,
                                      "payload": postcard1
                                  }
                              ]
                          }
                      }))


def quick_response_product_stage(sender_id, product):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

                      params={"access_token": page_access_token},

                      headers={"Content-Type": "application/json"},

                      data=json.dumps({
                          "recipient": {"id": sender_id},
                          "messaging_type": "RESPONSE",
                          "message": {
                              "text": 'Make your choice',
                              "quick_replies": quick_product_stage(product)
                          }
                      }))


# This template function sends the product feedback with images,contact and product details/information
def send_template(sender_id, product_name, status):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",

                      params={"access_token": page_access_token},

                      headers={"Content-Type": "application/json"},

                      data=json.dumps({
                          "recipient": {"id": sender_id},
                          "messaging_type": "RESPONSE",
                          "message": {
                              "attachment": {
                                  "type": "template",
                                  "payload": {
                                      "template_type": "generic",
                                      "elements": get_product_by_image(product_name, status)
                                  }
                              }
                          }
                      }))


def reset():
    r = requests.delete("https://graph.facebook.com/v6.0/me/messenger_profile",

                        params={"access_token": page_access_token},

                        headers={"Content-Type": "application/json"},

                        data=json.dumps({
                            "fields": [
                                "persistent_menu",
                                "get_started"
                            ]
                        }))
