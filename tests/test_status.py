import betamax
import pytest

import kojistatus


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'


@pytest.fixture(params=('churchyard', 'pviktori'))
def status_results(request, betamax_parametrized_session):
    return kojistatus.status(request.param,
                             session=betamax_parametrized_session)


def test_status_returns_50_results(status_results):
    # we know both users here have at least 50 builds
    assert len(list(status_results)) == 50


@pytest.mark.parametrize('idx', range(0, 50, 5))
def test_status_returns_ids_as_ints(status_results, idx):
    assert isinstance(list(status_results)[idx][0], int)
