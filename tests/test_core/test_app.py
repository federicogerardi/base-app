def test_app_creation(app):
    """Test che l'app viene creata correttamente"""
    assert app.config['TESTING'] == True

def test_404_error(client):
    """Test della gestione 404"""
    response = client.get('/api/not-exists')
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data['success'] == False
