import json

def test_post_correct(app, client):
    data = {"x_value": 1.88, "calculation_type": "red", "y_translation": 7}
    res = client.post('/calculations', data=json.dumps(data))
    assert res.status_code == 201
    #expected = {'id': 1}
    #assert expected == json.loads(res.get_data(as_text=True))

def test_post_typo(app, client):
    data = {"x_value": 1.88, "calculatio_type": "red", "y_translation": 7}
    res = client.post('/calculations', data=json.dumps(data))
    assert res.status_code == 400

def test_post_y_range(app, client):
    data = {"x_value": 1.88, "calculation_type": "red", "y_translation": 11}
    res = client.post('/calculations', data=json.dumps(data))
    assert res.status_code == 400

def test_post_calc_range(app, client):
    data = {"x_value": 1.88, "calculation_type": "brown", "y_translation": 11}
    res = client.post('/calculations', data=json.dumps(data))
    assert res.status_code == 400

def test_get(app, client):
    res = client.get('/calculations')
    assert res.status_code == 200

def test_get_since(app, client):
    res = client.get('/calculations?since=60')
    assert res.status_code == 200

def test_get_id(app, client):
    res = client.get('/calculations/1')
    assert res.status_code == 200

