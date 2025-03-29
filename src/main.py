import hashlib
from flask import Flask, request

app = Flask(__name__)

# 请替换为你的企业微信令牌
TOKEN = "your_token"


@app.route('/wecom', methods=['GET'])
def verify_url():
    try:
        signature = request.args.get('msg_signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

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
    app.run(host='0.0.0.0', port=5000)
    