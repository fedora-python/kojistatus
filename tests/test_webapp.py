import pytest

from kojistatus import application


@pytest.fixture
def testapp(betamax_parametrized_session):
    application.config['TESTING'] = True
    application.config['SESSION'] = betamax_parametrized_session
    return application.test_client()


@pytest.fixture
def response(testapp):
    return testapp.get('/churchyard/')


def test_webapp_returns_200_for_good_username(response):
    assert response.status_code == 200


def test_webapp_works_with_and_without_trailing_slash(testapp):
    response = testapp.get('/churchyard')
    assert response.status_code == 200
    response_with_trailing_slash = testapp.get('/churchyard/')
    assert response_with_trailing_slash.status_code == 200
    assert response.text == response_with_trailing_slash.text


def test_webapp_works_with_slash_in_username(testapp):
    response = testapp.get('/mbs/mbs.fedoraproject.org')
    assert response.status_code == 200
    response_with_trailing_slash = testapp.get('/mbs/mbs.fedoraproject.org/')
    assert response_with_trailing_slash.status_code == 200


def test_webapp_returns_404_for_bad_username(testapp):
    assert testapp.get('/i_hope_nobody_has_this_username/').status_code == 404


def test_webapp_returns_text_in_prescribed_format(response):
    body = response.data.decode('utf-8')
    print(body)
    lines = body.splitlines()
    assert len(lines) == 50
    task, status = lines[0].split()
    assert int(task) > 17340000
    assert len(status) > 2


def test_webapp_returns_statuses_for_all(testapp):
    response = testapp.get('/')
    body = response.data.decode('utf-8')
    print(body)
    lines = body.splitlines()
    assert len(lines) == 50


@pytest.mark.parametrize('koji', ('centos', 'rpmfusion'))
def test_webapp_with_different_kojis(testapp, koji):
    # TODO spy it so we are sure what URL was fetched
    response = testapp.get('/?koji=' + koji)
    body = response.data.decode('utf-8')
    print(body)
    lines = body.splitlines()
    assert len(lines) == 50
