import time

def test_rate_limit(client):
    """Test del rate limiting"""
    # Prima richiesta dovrebbe funzionare
    response = client.get('/')
    assert response.status_code == 200
    
    # Seconda richiesta immediata dovrebbe essere limitata
    response = client.get('/')
    assert response.status_code == 429  # Too Many Requests
    
    # Aspetta un secondo
    time.sleep(1)
    
    # Ora dovrebbe funzionare di nuovo
    response = client.get('/')
    assert response.status_code == 200

def test_security_headers(client):
    """Test degli headers di sicurezza"""
    response = client.get('/')
    headers = response.headers
    
    assert headers['X-Content-Type-Options'] == 'nosniff'
    assert headers['X-Frame-Options'] == 'SAMEORIGIN'
    assert headers['X-XSS-Protection'] == '1; mode=block' 