# Telegram Bot Server (Flask)

from flask import Flask

PORT = 8080

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def main(*args, **kwargs):
    return "<b>Welcome to our server"


# SSL Certificate challenge verification
# @app.route('')

# The server is running on :DEFAULT HOST:443 -> THIS_PC:8080
# Port forwarding 433->8080 via main gateway interface

if __name__ == '__main__':
    app.run('0.0.0.0', port = PORT)