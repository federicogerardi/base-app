def test_swagger_ui(client):
    """Test che la documentazione Swagger UI sia accessibile"""
    response = client.get('/api/docs')
    assert response.status_code == 200

def test_swagger_json(client):
    """Test che lo Swagger JSON sia accessibile"""
    response = client.get('/api/swagger.json')
    assert response.status_code == 200

def test_api_endpoints(client):
    """Test degli endpoint API"""
    # Test index
    response = client.get('/api/main/')
    assert response.status_code == 200
    assert response.json['success'] == True

    # Test error
    response = client.get('/api/main/test-error')
    assert response.status_code == 400
    assert response.json['success'] == False 