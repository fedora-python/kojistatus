import pytest

import kojistatus


@pytest.mark.parametrize(
    ('kojiurl', 'username'),
    (
        ('https://koji.fedoraproject.org/', 'churchyard'),
        ('https://cbs.centos.org/', 'cbs-kojira'),
        ('http://koji.rpmfusion.org/', 'kojira')
    )
)
def test_different_kojis_work(betamax_parametrized_session, kojiurl, username):
    i = kojistatus.status(username, kojiurl=kojiurl,
                          session=betamax_parametrized_session)
    assert list(i)  # just test that something is there


@pytest.fixture(params=('churchyard', 'pviktori', None))
def status_results(request, betamax_parametrized_session):
    return kojistatus.status(request.param,
                             session=betamax_parametrized_session)


def test_status_returns_50_results(status_results):
    # we know both users here have at least 50 builds
    assert len(list(status_results)) == 50


@pytest.mark.parametrize('idx', range(0, 50, 5))
def test_status_returns_ids_as_ints(status_results, idx):
    assert isinstance(list(status_results)[idx][0], int)
