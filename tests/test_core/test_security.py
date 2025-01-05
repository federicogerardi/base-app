import time

def test_rate_limit(client):
    """Test del rate limiting"""
    # Prima richiesta dovrebbe funzionare
    response = client.get('/api/main/')
    assert response.status_code == 200
    
    # Seconda richiesta immediata dovrebbe essere limitata
    response = client.get('/api/main/')
    assert response.status_code == 429
    
    # Aspetta un secondo
    time.sleep(1)
    
    # Ora dovrebbe funzionare di nuovo
    response = client.get('/api/main/')
    assert response.status_code == 200

def test_security_headers(client):
    """Test degli headers di sicurezza"""
    response = client.get('/api/main/')
    headers = response.headers
    
    assert 'X-Content-Type-Options' in headers
    assert 'X-Frame-Options' in headers
    assert 'X-XSS-Protection' in headers 