import pytest
import requests_mock

from skillcorner.client import SkillcornerClient


def test_get_matches():
    body = {
        'count': 1,
        'result': [
            {
                'id': 46771,
                'date_time': '2021-08-13T19:00:00Z',
                'home_team': {'id': 754, 'short_name': 'Brentford FC'},
                'away_team': {'id': 3, 'short_name': 'Arsenal'},
                'status': 'closed',
            },
        ],
    }
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/matches/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        response = SkillcornerClient().get_matches()
    assert response == body


def test_get_matches_paginated():
    body_1 = {
        'count': 6,
        'next': 'https://skillcorner.com/api/matches/?limit=3&offset=3',
        'previous': None,
        'results': [
            {
                'id': 1,
            },
            {
                'id': 2,
            },
            {
                'id': 3,
            },
        ],
    }
    body_2 = {
        'count': 6,
        'next': None,
        'previous': 'https://skillcorner.com/api/matches/?limit=3',
        'results': [
            {
                'id': 4,
            },
            {
                'id': 5,
            },
            {
                'id': 6,
            },
        ],
    }
    expected = [
        {
            'id': 1,
        },
        {
            'id': 2,
        },
        {
            'id': 3,
        },
        {
            'id': 4,
        },
        {
            'id': 5,
        },
        {
            'id': 6,
        },
    ]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/matches/',
            headers={'Content-Type': 'application/json'},
            json=body_1,
        )
        mock.get(
            'https://skillcorner.com/api/matches/?limit=3&offset=3',
            headers={'Content-Type': 'application/json'},
            json=body_2,
        )
        response = SkillcornerClient().get_matches()
    assert response == expected


def test_get_matches_with_params():
    body = [
        {
            'id': 46771,
            'date_time': '2021-08-13T19:00:00Z',
            'home_team': {'id': 754, 'short_name': 'Brentford FC'},
            'away_team': {'id': 3, 'short_name': 'Arsenal'},
            'status': 'closed',
        },
    ]
    params = {'competition_edition': [287, 387]}
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/matches/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        response = SkillcornerClient().get_matches(params)
    assert response == body


def test_get_matches_with_random_kwargs():
    body = [
        {
            'id': 46771,
            'date_time': '2021-08-13T19:00:00Z',
            'home_team': {'id': 754, 'short_name': 'Brentford FC'},
            'away_team': {'id': 3, 'short_name': 'Arsenal'},
            'status': 'closed',
        },
    ]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/matches/',
            headers={'Content-Type': 'application/json'},
            json=body,
        )
        response = SkillcornerClient().get_matches(kwarg_1='kwarg_1', kwarg_2='kwarg_2')
    assert response == body


def test_get_matches_with_unknown_arg():
    with pytest.raises(TypeError):
        SkillcornerClient().get_matches({'arg1_is': 'params'}, 'raise_for_status_arg', 'unknown_arg')
