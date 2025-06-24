from flask import Flask, request, jsonify
import requests

PUBLIC_IP_URL = 'https://api.ipify.org?format=json'

app = Flask(__name__)

def get_ip_address():
    res = requests.get(PUBLIC_IP_URL)
    if res.status_code == 200:
        return res.json().get('ip')
    else:
        return 'Unable to fetch IP address'
    
def get_client_ip_address():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
        print(f"Client IP from X-Forwarded-For: {ip}")
    else:
        ip = request.remote_addr
        print(f"Client IP from remote_addr: {ip}")
    return ip

def get_headers():
    return dict(request.headers)

@app.route('/')
def index():
    return f'<h1>Your public IP address is: {get_client_ip_address()}</h1>'
    # return jsonify(get_headers())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)