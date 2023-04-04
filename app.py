import os
import openai
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi("")
handler = WebhookHandler("")
openai.api_key = ''

@ app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@ handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text.startswith("chat"):
        out = event.message.text.lstrip("chat")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=out,
            max_tokens=128,
            temperature=0.5,
       )   
        completed_text = response.choices[0].text
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=completed_text.lstrip()))
        


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
