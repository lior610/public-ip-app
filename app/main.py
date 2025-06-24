from flask import Flask, request, jsonify

app = Flask(__name__)
    
def get_client_ip_address():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    return f'<h1>Your public IP address is:bla bla</h1>'

@app.route('/json')
def json_response():
    return jsonify({
        'ip': get_client_ip_address()
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)