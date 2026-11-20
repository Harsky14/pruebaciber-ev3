import re
from flask import Flask, request, make_response, abort
from markupsafe import escape
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

VALID_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-]{1,30}$')

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    return response

@app.route('/hello')
def hello():
    name = request.args.get('name', '').strip()
    if not name or not VALID_NAME_PATTERN.match(name):
        abort(400, description="Parámetro 'name' inválido o ausente.")

    safe_name = escape(name)
    response = make_response(f"Hello, {safe_name}!")
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)