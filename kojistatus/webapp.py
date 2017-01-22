from flask import Flask, Response
from flask.helpers import NotFound
from requests.exceptions import HTTPError

from .status import status


app = Flask(__name__)


def session(app):
    if 'SESSION' in app.config:
        return app.config['SESSION']


app.__class__.session = session


@app.route('/<username>/')
def main(username):
    try:
        lines = ('{} {}'.format(*s) for s in status(username,
                                                    session=app.session()))
    except HTTPError:
        # This is most likely due to not existing username, so return 404
        # But it might also be a Koji problem, because it just gives 500
        raise NotFound()
    return Response('\n'.join(lines), mimetype='text/plain')
