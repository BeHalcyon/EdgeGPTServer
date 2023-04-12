import asyncio
from flask import Flask, request
import markdown
from flask import render_template, Markup
from EdgeGPT import Chatbot, ConversationStyle

app = Flask(__name__)

async def generate_response_once(input):
    bot = Chatbot("./cookies.json")
    res = (await bot.ask(prompt=input, conversation_style=ConversationStyle.creative,
                         wss_link="wss://sydney.bing.com/sydney/ChatHub"))["item"]["messages"][1]["adaptiveCards"][0][
        "body"][0]["text"]
    return res


def md2html(mdcontent):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    html = markdown.markdown(mdcontent, extensions=exts)
    content = Markup(html)
    return content


@app.route('/', methods=['GET'])
def index(output_text=""):
    return render_template('ui_index.html', output_text=output_text)


@app.route('/bing_chat', methods=['POST'])
def chat_v3():
    try:
        input_text = request.form['input_text']
        print("Ask:", input_text)
        res = asyncio.run(generate_response_once(input_text))
        if "500 Internal Server Error" in res:
            res = "Internal Server Error. Please Try Again."
    except:
        res = "Internal Server Error. Please Try Again."
    content = md2html(res)
    print("Answer:", content)
    return content


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5000)
    app.run()
