# 导入flask模块
import asyncio

from flask import Flask, request, jsonify
from rich.markdown import Markdown
import markdown
from flask import render_template, Markup
# 创建一个flask应用
app = Flask(__name__)


class EdgeGPTHelper:

    account_dict = {}

    @classmethod
    async def chat(cls, account, input, conversation_style="creative", wss_link="wss://sydney.bing.com/sydney/ChatHub"):
        # 没有创建会话的，会先创建会话
        if account not in cls.account_dict:
            cls.account_dict[account] = Chatbot(cookiePath="./cookies.json")

        # 从会话里创建对话
        res = (
            await cls.account_dict[account].ask(
                prompt=input,
                conversation_style=conversation_style,
                wss_link=wss_link,
            )
        )["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]

        return res




# 定义一个函数，根据输入的一句话，返回另一句话
def generate_response(user, input, conversation_style):
    # return asyncio.run(EdgeGPTHelper.chat(user, input, conversation_style))
    return asyncio.run(EdgeGPTHelper.chat("test", "你是谁？"))

    # 定义一个路由，接收POST请求，参数是input

async def generate_response_once(input):
    bot = Chatbot("./cookies.json")
    res = (await bot.ask(prompt=input, conversation_style=ConversationStyle.creative,
                        wss_link="wss://sydney.bing.com/sydney/ChatHub"))["item"]["messages"][1]["adaptiveCards"][0]["body"][0]["text"]
    return res


def md2html(mdcontent):
    exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
            'markdown.extensions.toc']
    html = markdown.markdown(mdcontent, extensions=exts)
    content = Markup(html)
    return content

import collections
queue = collections.deque(maxlen=10)

@app.route('/chat_v2', methods=['GET'])
def api2():
    input = request.args.get('input')
    print("Ask:", input)
    res = asyncio.run(generate_response_once(input))
    content = md2html(res)
    print("Answer:", content)
    return render_template('index.html', **locals())



@app.route('/chat', methods=['GET'])
def api():
    # 获取请求的参数
    input = request.args.get('input')
    user = request.args.get('user')
    conversation_style = request.args.get('conversation_style')
    print("正在调用：", input, user, conversation_style)
    # 调用函数，生成返回值
    # output = generate_response(user, input, conversation_style)
    output = asyncio.run(EdgeGPTHelper.chat(user, input, conversation_style))
    # 返回json格式的响应
    # output = asyncio.run(EdgeGPTHelper.chat("test", "你是谁？"))
    print(user, input, conversation_style, output)
    return output.replace("\n", "<br/>")

    # 运行flask应用

from EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = Chatbot(cookiePath="./cookies.json")
    print(await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative,wss_link="wss://sydney.bing.com/sydney/ChatHub"))
    await bot.close()


@app.route('/', methods=['GET'])
def index(output_text=""):
  # 渲染html文件，初始时输出框为空
  return render_template('ui_index.html', output_text=output_text)

@app.route('/bing_chat', methods=['POST'])
def chat_v3():
  input_text = request.form['input_text']
  print("Ask:", input_text)
  res = asyncio.run(generate_response_once(input_text))
  content = md2html(res)
  print("Answer:", content)
  return content

# if __name__ == "__main__":
#     asyncio.run(main())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)