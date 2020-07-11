
import pytest
import json


MIMETYPE = 'application/json'
HEADERS = {
    'Content-Type': MIMETYPE,
    'Accept': MIMETYPE
}
PAYLOAD = {

}


def setup_function(function):
    print("setting up", function)


def test_template_item_deploy(client, db):
    response = client.post(
        '/api/templates/',
        data=json.dumps({
            'title': "Untitled Test Template",
            'url': "https://raw.githubusercontent.com/SelfhostedPro/selfhosted_templates/yacht/Template/template.json"
        }),
        headers=HEADERS)
    assert response.status_code == 201, 'invalid response status'
    json_data = json.loads(response.data)
    assert 'id' in json_data['data'], 'id missing'
    template_id = json_data['data']['id']

    response = client.post(
        f'/api/templates/{template_id}/refresh',
        headers=HEADERS)
    print(response.data)
    assert response.status_code == 200, 'invalid response status'

    response = client.get(
        f'/api/templates/{template_id}')
    assert response.status_code == 200, 'invalid response status'
    json_data = json.loads(response.data)
    assert len(json_data['data']) > 0
    assert len(json_data['data']['items']) > 0
    app_id = json_data['data']['items'][0]['id']

    response = client.post(
        f'/api/apps/{app_id}/deploy',
        data=json.dumps({
            'title': "My First Container",
            'image': "my:container", 
        }),
        headers=HEADERS)
    assert response.status_code == 200, 'invalid response status'
    # json_data = json.loads(response.data)
    pass
