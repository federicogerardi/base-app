def test_app_integration(client):
    """Test integrazione tra componenti"""
    
    # 1. Test routing e template
    response = client.get('/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    
    # 2. Test API e autenticazione
    response = client.get('/api/main/')
    assert response.status_code == 200
    assert response.json['success'] == True
    
    # 3. Test errori e logging
    response = client.get('/non-esistente')
    assert response.status_code == 404
    
    # 4. Test sicurezza
    response = client.get('/api/main/')
    assert 'X-Content-Type-Options' in response.headers 