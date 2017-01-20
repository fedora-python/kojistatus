import re

import requests


RE_ID = re.compile(r'<td>(\d+)</td>', re.ASCII)
RE_STATUS = re.compile(r'<img class="stateimg" src="/koji-static/images/\w+.'
                       r'png" title="(\w+)" alt="\w+"/>', re.ASCII)


def status(username, *,
           kojiurl='https://koji.fedoraproject.org/',
           session=None):
    """
    For given username, return the last builds with status information.
    Returns an iterable of 2-tuples, sorted descending.

    Only the first page with maximum 50 results is fetched.
    """
    session = session or requests.Session()
    url = '{}koji/tasks?owner={}&state=all&?view=toplevel'.format(kojiurl,
                                                                  username)
    response = session.get(url)
    response.raise_for_status()
    return _parse(response.text)


def _parse(html):
    """
    Parses the given HTML source using regular expressions (I know :P)
    Returns status information for status()
    """
    ids = RE_ID.findall(html)
    statuses = RE_STATUS.findall(html)
    for idx, status in enumerate(statuses):
        yield (int(ids[idx]), status)
