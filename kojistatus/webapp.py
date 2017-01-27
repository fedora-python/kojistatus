from flask import Flask, Response, request
from flask.helpers import NotFound
from requests.exceptions import HTTPError

from .status import status


app = Flask(__name__)


def session(app):
    if 'SESSION' in app.config:
        return app.config['SESSION']


app.__class__.session = session


@app.route('/')
@app.route('/<username>/')
def main(username=None):
    koji = request.args.get('koji')
    if koji == 'centos':
        kojiurl = 'https://cbs.centos.org/'
    elif koji == 'rpmfuison':
        kojiurl = 'http://koji.rpmfusion.org/'
    else:
        kojiurl = None
    try:
        lines = ('{} {}'.format(*s) for s in status(username,
                                                    session=app.session(),
                                                    kojiurl=kojiurl))
    except HTTPError:
        # This is most likely due to not existing username, so return 404
        # But it might also be a Koji problem, because it just gives 500
        raise NotFound()
    return Response('\n'.join(lines), mimetype='text/plain')
