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
    pics = []

    messages = twilio.messages.list(to=PHONE_NUMBER)
    for message in messages:
        if message.sid.startswith('MM'):
            media = message.media.list()
            pics.extend(['https://api.twilio.com{}'.format(m.uri.replace('.json', '')) for m in media])

    return json.dumps(pics), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)