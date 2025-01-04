def test_swagger_ui(client):
    """Test che la documentazione Swagger UI sia accessibile"""
    response = client.get('/api/docs', follow_redirects=True)
    assert response.status_code == 200
    assert b'swagger-ui' in response.data

def test_swagger_json(client):
    """Test che lo Swagger JSON sia accessibile e valido"""
    response = client.get('/api/swagger.json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'swagger' in json_data
    assert 'paths' in json_data

def test_api_endpoints(client):
    """Test degli endpoint API"""
    # Test index
    response = client.get('/api/main/')
    assert response.status_code == 200
    assert response.json['success'] == True
    assert 'Flask API is running' in response.json['message']

    # Test error
    response = client.get('/api/main/test-error')
    assert response.status_code == 400
    assert response.json['success'] == False
    assert 'errore di test' in response.json['message'].lower() 