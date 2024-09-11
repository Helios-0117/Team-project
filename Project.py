import os, ssl, json, requests
from urllib.request import urlopen
from flask import Flask, request, abort
from imgur01 import upload_to_imgur
from imgurpython import ImgurClient
from bs4 import BeautifulSoup
from test__openai import chat
from linebot import LineBotApi, WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (Configuration,ApiClient,MessagingApi,ReplyMessageRequest,TextMessage,ImageMessage)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)
Chat_key = os.getenv('Chat_key',None)
CWA_key = os.getenv('CWA_key',None)
Secret = os.getenv('Linebot_Secret', None)
Token = os.getenv('Linebot_Token',None)
client_id = os.getenv('Imgur_id', None)
client_secret = os.getenv('Imgur_secret', None)
line_bot_api = LineBotApi(Token)
line_handler = WebhookHandler(Secret)
config = Configuration(access_token=Token)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

Conservative_url = 'https://docs.google.com/presentation/d/1kz9kJLOwAZKSX9lB-xSoHYDCsT1q_vMTyThYQwn54LU/edit?usp=sharing'
Steady_url       = 'https://docs.google.com/presentation/d/1t3Y77y0cuNoOv6RBhaqPbEAyk-72Ds5wpNyBgAFJi-Q/edit?usp=sharing'
Aggressive_url   = 'https://docs.google.com/presentation/d/1gePcfifIGZBjnC2Io4xMOuAZOcQLfHi2kiyHEi8B3DY/edit?usp=sharing'
GoogleNews_url   = 'https://news.google.com/home?hl=zh-TW&gl=TW&ceid=TW:zh-Hant'
GoogleNews_Finance_url  = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
stock_url        = 'https://www.wantgoo.com/stock'
twse_url         = 'https://www.twse.com.tw/zh/index.html#statistics'
twse_check_url   = 'https://www.twse.com.tw/zh/stocks/inquiry.html'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):    
    if event.message.text in ['1','保守型']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，審閱你的投資建議 :) \n' + str(Conservative_url))
        )

    elif event.message.text in ['2','穩健型']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，審閱你的投資建議 :) \n' + str(Steady_url))
        )

    elif event.message.text in ['3','積極型']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，審閱你的投資建議 :) \n' + str(Aggressive_url))
        )
    elif event.message.text in ['4','財經新聞']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，閱讀近日財經新聞 :) \n' + str(GoogleNews_Finance_url))
        )

    elif event.message.text in ['5','台股大盤']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，股票大盤 :) \n' + str(stock_url))
        )

    elif event.message.text in ['6','台灣證劵交易所台股大盤']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，台灣證劵交易所台股大盤 :) \n' + str(twse_url))
        )

    elif event.message.text in ['7','台灣證劵交易所股票查詢']:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請至以下的連結，查詢台灣證劵交易所 :) \n' + str(twse_check_url))
        )
        
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='本理財機器人功能選單:\n 1.(保守型)\n 2.(穩健型)\n 3.(積極型)\n 4.(財經新聞)\n 5.(台股大盤)\n 6.(台灣證劵交易所台股大盤)\n 7.(台灣證劵交易所股票查詢)'))

if __name__ == "__main__":
    app.run()
