from xml.etree import ElementTree

import pytest
import requests_mock
from defusedxml.ElementTree import fromstring

from skillcorner.client import SkillcornerClient


def test_get_match_tracking_data():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 42
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/42/tracking/',
            headers={'Content-Type': 'application/json-l'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id=match_id)
    assert response == expected


def test_get_match_tracking_data_with_params_file_format_jsonl():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 138
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/138/tracking/',
            headers={'Content-Type': 'application/json-l'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id, {'file_format': 'jsonl'})
    assert response == expected


def test_get_match_tracking_data_with_params_file_format_fifa_data():
    content = b'<root><child name="child1">Fifa data</child></root>'
    match_id = 12
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/12/tracking/',
            headers={'Content-Type': 'binary/octet-stream'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id, {'file_format': 'fifa-data'})
    assert response == content


def test_get_match_tracking_data_with_params_file_format_fifa_xml():
    content = b'<root><child name="child1">Fifa xml</child></root>'
    match_id = 2006
    expected = fromstring(content)
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/2006/tracking/',
            headers={'Content-Type': 'application/xml'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id, {'file_format': 'fifa-xml'})
    assert ElementTree.tostring(response) == ElementTree.tostring(expected)


def test_get_match_tracking_data_with_params_file_format_unknown():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 89
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/89/tracking/',
            headers={'Content-Type': 'application/json-l'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id, {'file_format': 'unknown'})
    assert response == expected


def test_get_match_tracking_data_with_params_typo_or_unknown():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 2018
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/2018/tracking/',
            headers={'Content-Type': 'application/json-l'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id, {'fileformat': 'any'})
    assert response == expected


def test_get_match_tracking_data_with_random_kwargs():
    content = b'{"frame": 1}\n{"frame": 2}\n{"frame": 3}\n'
    match_id = 5077
    expected = [{'frame': 1}, {'frame': 2}, {'frame': 3}]
    with requests_mock.Mocker(real_http=False) as mock:
        mock.get(
            'https://skillcorner.com/api/match/5077/tracking/',
            headers={'Content-Type': 'application/json-l'},
            content=content,
        )
        response = SkillcornerClient().get_match_tracking_data(match_id, kwarg_1='kwarg_1', kwarg_2='kwarg_2')
    assert response == expected


def test_get_match_tracking_data_with_unknown_arg():
    with pytest.raises(TypeError):
        match_id = 1998
        SkillcornerClient().get_match_tracking_data(
            match_id, {'unused_param': 'foo'}, 'raise_for_status_arg', 'unknown_arg'
        )
