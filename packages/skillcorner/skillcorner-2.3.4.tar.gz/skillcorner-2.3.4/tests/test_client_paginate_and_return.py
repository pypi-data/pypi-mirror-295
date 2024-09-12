import requests_mock
from fitrequest.method_generator import RequestMethod

from skillcorner.client import SkillcornerClient


def test_paginate_and_return_one_page():
    expected = [1, 2, 3]

    method = RequestMethod.get
    response = {'results': [1, 2, 3], 'next': None}
    result = SkillcornerClient()._paginate_and_return(method=method, response=response)
    assert result == expected


def test_paginate_and_return_two_pages():
    expected = [1, 2, 3, 4, 5]

    method = RequestMethod.get
    response = {'results': [1, 2, 3], 'next': 'https://skillcorner.com/test?foo=bar&offset=3'}
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/test?foo=bar&offset=3',
            headers={'Content-Type': 'application/json'},
            json={'results': [4, 5], 'next': None},
        )
        result = SkillcornerClient()._paginate_and_return(method=method, response=response)
    assert result == expected


def test_paginate_and_return_three_pages():
    expected = [1, 2, 3, 4, 5, 6, 12, 14]

    method = RequestMethod.get
    response = {'results': [1, 2, 3], 'next': 'https://skillcorner.com/test?foo=bar&offset=3'}
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/test?foo=bar&offset=3',
            headers={'Content-Type': 'application/json'},
            json={'results': [4, 5, 6], 'next': 'https://skillcorner.com/test?foo=bar&offset=6'},
        )
        mock.get(
            'https://skillcorner.com/test?foo=bar&offset=6',
            headers={'Content-Type': 'application/json'},
            json={'results': [12, 14], 'next': None},
        )
        result = SkillcornerClient()._paginate_and_return(method=method, response=response)
    assert result == expected
