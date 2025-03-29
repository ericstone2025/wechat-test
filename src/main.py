import hashlib
import os
from flask import Flask, request
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 从环境变量获取令牌，如果没有则使用默认值
TOKEN = os.getenv('WECOM_TOKEN', 'your_token')

@app.route('/')
def index():
    return {"status": "running", "message": "企业微信测试服务已启动"}

@app.route('/wecom', methods=['GET'])
def verify_url():
    try:
        signature = request.args.get('msg_signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        if not all([signature, timestamp, nonce, echostr]):
            return "Missing required parameters", 400

        # 对参数进行排序
        params = [TOKEN, timestamp, nonce, echostr]
        params.sort()

        # 拼接字符串
        param_str = ''.join(params)

        # 计算SHA1签名
        sha1 = hashlib.sha1()
        sha1.update(param_str.encode('utf-8'))
        calculated_signature = sha1.hexdigest()

        # 验证签名
        if calculated_signature == signature:
            return echostr
        else:
            return "Signature verification failed", 400
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    