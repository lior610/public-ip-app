from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
    
def get_client_ip_address():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

@app.route('/health')
def health_check():
    return 'OK'

@app.route('/')
def index():
    return render_template('index.html', ip=get_client_ip_address())

@app.route('/json')
def json_response():
    return jsonify({
        'ip': get_client_ip_address()
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)