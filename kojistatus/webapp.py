from flask import Flask, Response, request
from requests.exceptions import HTTPError
from werkzeug.exceptions import NotFound

from .status import status


app = Flask(__name__)


def session(app):
    if 'SESSION' in app.config:
        return app.config['SESSION']


app.__class__.session = session


# We need to explicitly define both possible user
# URLs because the automatic redirect does not work.
# See https://github.com/pallets/werkzeug/issues/2533
@app.route('/')
@app.route('/<path:username>')
@app.route('/<path:username>/')
def main(username=None):
    koji = request.args.get('koji')
    if koji == 'centos':
        kojiurl = 'https://cbs.centos.org/'
    elif koji == 'rpmfusion':
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
