def test_app_creation(app):
    """Test che l'app viene creata correttamente"""
    assert app.config['TESTING'] == True

def test_index_route(client):
    """Test della rotta principale"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] == True
    assert 'Flask API is running' in json_data['message']

def test_404_error(client):
    """Test della gestione 404"""
    response = client.get('/route-not-exists')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['success'] == False

def test_custom_error(client):
    """Test della gestione errori personalizzati"""
    response = client.get('/test-error')
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] == False
    assert 'errore di test' in json_data['message'].lower() 