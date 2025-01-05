import time

def test_rate_limit(client):
    """Test del rate limiting"""
    # Prima richiesta
    response = client.get('/api/')
    assert response.status_code == 200
    
    # Seconda richiesta (ancora permessa)
    response = client.get('/api/')
    assert response.status_code == 200
    
    # Terza richiesta (dovrebbe essere bloccata)
    response = client.get('/api/')
    assert response.status_code == 429
    
    # Attesa e nuova richiesta
    time.sleep(1)
    response = client.get('/api/')
    assert response.status_code == 200

def test_security_headers(client):
    """Test degli headers di sicurezza"""
    response = client.get('/api/')
    headers = response.headers
    assert 'X-Content-Type-Options' in headers 