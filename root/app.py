import sys
from flask import Flask, request
from root.DB_links import mysqlConnector, get_product_by_stage, quick_product_stage
from root.servers import send_message, quick_response, send_template, quick_response_product_stage, quick_response_one

app = Flask(__name__)

store_msg = []
product = []
postcard = []


@app.route('/', methods=['GET'])
def verify():
    # webhook verification
    if request.args.get("hub.mode") == 'subscribe' and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Tested and working fine", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                Sender_ID = messaging_event['sender']['id']
                Recipient_ID = messaging_event.get("recipient").get('id')
                callback = ''
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        get_msg = messaging_event['message']
                        if 'is_echo' not in get_msg:
                            mess = messaging_event['message']['text']
                            message = mess.lower()

                            if message in ['hi', 'hello', 'get started', 'bot']:
                                quick_response(Sender_ID,
                                               'What would you like to do today? ',
                                               'Buy', 'Sell', postcard1="buying", postcard2="selling")
                                store_msg.append(message)
                            elif 'okay' in message or 'alright' in message:
                                callback = 'Alright'
                            elif 'buy' in message:
                                callback = "What type of product would you like to buy ?"
                                store_msg.append(message)
                            elif ('buy' in store_msg) or 'another' in store_msg or mysqlConnector(message) and len(
                                    store_msg) != 0:
                                product.append(message)
                                try:
                                    if mysqlConnector(message):
                                        if len(quick_product_stage(message)) > 1:
                                            send_message(Sender_ID,
                                                         f'{message} is available in {len(quick_product_stage(message))} in stages')
                                            quick_response_product_stage(Sender_ID, message)
                                            postcard.append('view product')
                                            del store_msg[-1]
                                        else:
                                            quick_response_product_stage(Sender_ID, message)
                                            postcard.append('view product')
                                            del store_msg[-1]
                                    else:

                                        send_message(Sender_ID,
                                                     f'{message} is not available at the moment.')
                                        send_message(Sender_ID,
                                                     f'Would you like to buy another product apart from {message} ?')
                                        product.clear()
                                except:
                                    callback = "failed to connect to database"
                            elif 'another' in message and 'product' in message:
                                store_msg.append('another')
                                callback = "What product would you like to check ?"

                            elif len(postcard) != 0:
                                if postcard[0] == "view product":
                                    try:
                                        send_template(Sender_ID, product[0], message)
                                        del product[0]
                                        del postcard[0]
                                    except:
                                        callback = "Sorry, there was an error viewing the product"
                            elif 'check' in message and 'plants' in message or 'all' in message:
                                if 'instock' in message:
                                    callback = get_product_by_stage('instock')
                                elif 'germination' in message or 'germinate' in message:
                                    callback = get_product_by_stage('germinate')
                                elif 'harvest' in message:
                                    callback = get_product_by_stage('harvest')
                                elif 'growing' in message or 'grow' in message:
                                    callback = get_product_by_stage('growing')
                                elif 'near harvest' in message:
                                    callback = get_product_by_stage('near harvest')
                                else:
                                    callback = "incorrect entry"
                            elif 'chat with an advisor' in message:
                                callback = "https://www.messenger.com/t/clair.blair.376"
                            elif 'sell' in message or 'sale' in message:
                                quick_response_one(Sender_ID,
                                                   'You will need to sign up on Rucove, need some help with that?',
                                                   'Chat with an advisor', postcard1="chat advisor")
                            else:
                                callback = "Oh! please wait a second "
                    else:
                        callback = 'No text found'
                    print('store_msg :', store_msg)
                    print('postcard :', postcard)
                    print('product :', product)
                    send_message(Sender_ID, callback)
    return "ok", 200


# this flushes out the message dictionary to the terminal for debug purpose
# you can uncomment this to debug this code
def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run()
