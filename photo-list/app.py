import json
import os
from flask import Flask, request
from twilio.rest import Client

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.environ.get('TWILIO_NUMBER')

twilio = Client(ACCOUNT_SID, AUTH_TOKEN)
app = Flask(__name__)


@app.route('/photos', methods=['GET'])
def list_photos():
    return json.dumps([
        'https://api.twilio.com{}'.format(media.uri.replace('.json', '')) 
        for message in twilio.messages.list(to=PHONE_NUMBER) if message.sid.startswith('MM') 
        for media in message.media.list()
    ]), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)