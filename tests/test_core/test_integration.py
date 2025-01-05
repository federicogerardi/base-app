def test_app_integration(client):
    """Test integrazione tra componenti"""
    # Test API base
    response = client.get('/api/')
    assert response.status_code == 200
    
    # Test documentazione API
    response = client.get('/api/docs')
    assert response.status_code == 200
    
    # Test errori
    response = client.get('/api/non-esistente')
    assert response.status_code == 404 