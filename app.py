from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app) # This line adds the /metrics endpoint

@app.route('/')
def hello():
    return "SRE Project: Version 3.0 - Deployed via CI/CD!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)