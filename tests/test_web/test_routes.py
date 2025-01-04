def test_index_page(client):
    """Test della homepage"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Benvenuto' in response.data

def test_about_page(client):
    """Test della pagina about"""
    response = client.get('/about')
    assert response.status_code == 200

def test_dashboard_page(client):
    """Test della dashboard"""
    response = client.get('/dashboard')
    assert response.status_code == 200 