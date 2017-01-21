from flask import Flask, Response

from .status import status


app = Flask(__name__)


@app.route('/<username>/')
def main(username):
    try:
        lines = ['{} {}'.format(*s) for s in status(username)]
    except:
        lines = []
        ...  # TODO return 500-ish error
    return Response('\n'.join(lines), mimetype='text/plain')
