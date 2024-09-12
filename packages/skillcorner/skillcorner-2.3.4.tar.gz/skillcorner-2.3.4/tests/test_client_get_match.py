import pytest
import requests_mock
from requests.exceptions import HTTPError

from skillcorner.client import SkillcornerClient


def test_get_match():
    body = {
        'date_time': '2021-08-13T19:00:00Z',
        'home_team': {'id': 754, 'short_name': 'Brentford FC'},
        'away_team': {'id': 3, 'short_name': 'Arsenal'},
    }
    match_id = 42
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/42/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        response = SkillcornerClient().get_match(match_id=match_id)
    assert response == body


def test_get_match_raise_on_status():
    with requests_mock.Mocker(real_http=False) as mock, pytest.raises(HTTPError):
        mock.get(
            'https://skillcorner.com/api/match/7/',
            status_code=404,
        )
        SkillcornerClient().get_match(7)


def test_get_match_with_params():
    body = {
        'date_time': '2021-08-13T19:00:00Z',
        'home_team': {'id': 754, 'short_name': 'Brentford FC'},
        'away_team': {'id': 3, 'short_name': 'Arsenal'},
    }
    match_id = 42
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/42/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        response = SkillcornerClient().get_match(match_id, {'unused_param': 'foo'})
    assert response == body


def test_get_match_with_random_kwargs():
    body = {
        'date_time': '2021-08-13T19:00:00Z',
        'home_team': {'id': 754, 'short_name': 'Brentford FC'},
        'away_team': {'id': 3, 'short_name': 'Arsenal'},
    }
    match_id = 42
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/42/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        response = SkillcornerClient().get_match(match_id, kwarg_1='kwarg_1', kwarg_2='kwarg_2')
    assert response == body


def test_get_match_with_unknown_arg():
    match_id = 33
    with pytest.raises(TypeError):
        SkillcornerClient().get_match(match_id, {'unused_param': 'foo'}, 'raise_for_status_arg', 'unknown_arg')
