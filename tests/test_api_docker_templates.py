
import pytest
import json


MIMETYPE = 'application/json'
HEADERS = {
    'Content-Type': MIMETYPE,
    'Accept': MIMETYPE
}
PAYLOAD = {
    'title': "Untitled Test Template",
    'url': "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/yacht/Template/template.json"
}


def setup_function(function):
    print("setting up", function)


def test_template_index(client, db):
    response = client.get(
        '/api/templates/')
    assert response.status_code == 200, 'invalid response status'
    json_data = json.loads(response.data)
    assert json_data['data'] == []

    response = client.post(
        '/api/templates/',
        data=json.dumps(PAYLOAD),
        headers=HEADERS)
    assert response.status_code == 201, 'invalid response status'
    json_data = json.loads(response.data)
    assert 'id' in json_data['data'], 'id missing'

    response = client.get(
        '/api/templates/')
    assert response.status_code == 200, 'invalid response status'
    json_data = json.loads(response.data)
    assert len(json_data['data']) > 0


def test_template_show(client, db):
    response = client.post(
        '/api/templates/',
        data=json.dumps(PAYLOAD),
        headers=HEADERS)
    assert response.status_code == 201, 'invalid response status'
    json_data = json.loads(response.data)
    assert 'id' in json_data['data'], 'id missing'
    id = json_data['data']['id']

    response = client.get(
        f'/api/templates/{id}')
    assert response.status_code == 200, 'invalid response status'
    json_data = json.loads(response.data)
    assert len(json_data['data']) > 0


def test_template_create(client, db):
    for i in range(2):
        response = client.post(
            '/api/templates/',
            data=json.dumps(PAYLOAD),
            headers=HEADERS)
        if i == 0:
            assert response.status_code == 201, 'invalid response status'
            json_data = json.loads(response.data)
            assert 'id' in json_data['data'], 'id missing'
            for key, val in PAYLOAD.items():
                assert key in json_data['data'], f'{key} missing'
                assert json_data['data'][key] == val, f'{key} missing'
        else:
            # test uniquness
            assert response.status_code == 409, 'invalid response status'

    # testt missing parameters
    payloads = [
        {
            'title': "Untitled Test Template"
        },
        {
            'url': "http://localhost.local:8080/path/to/template.json"
        }
    ]
    for payload in payloads:
        response = client.post(
            '/api/templates/',
            data=json.dumps(payload),
            headers=HEADERS)
        assert response.status_code == 422, 'invalid response status'


# def test_template_update(client):
#     pass


def test_template_delete(client, db):
    response = client.post(
        '/api/templates/',
        data=json.dumps(PAYLOAD),
        headers=HEADERS)
    assert response.status_code == 201, 'invalid response status'
    json_data = json.loads(response.data)
    assert 'id' in json_data['data'], 'id missing'
    id = json_data['data']['id']

    response = client.delete(
        f'/api/templates/{id}',
        headers=HEADERS)
    assert response.status_code == 200, 'invalid response status'


def test_template_refresh(client, db):
    response = client.post(
        '/api/templates/',
        data=json.dumps(PAYLOAD),
        headers=HEADERS)
    assert response.status_code == 201, 'invalid response status'
    json_data = json.loads(response.data)
    assert 'id' in json_data['data'], 'id missing'
    id = json_data['data']['id']

    response = client.get(
        f'/api/templates/{id}')
    assert response.status_code == 200, 'invalid response status'
    json_data = json.loads(response.data)
    assert len(json_data['data']) > 0
    updated_at = json_data['data']['updated_at']
    items = json_data['data']['items']

    response = client.post(
        f'/api/templates/{id}/refresh',
        headers=HEADERS)
    print(response.data)
    assert response.status_code == 200, 'invalid response status'

    response = client.get(
        f'/api/templates/{id}')
    assert response.status_code == 200, 'invalid response status'
    json_data = json.loads(response.data)
    assert len(json_data['data']) > 0
    # assert json_data['data']['items'] == items
    assert json_data['data']['updated_at'] != updated_at

    pass
