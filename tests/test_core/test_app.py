def test_app_creation(app):
    """Test che l'app viene creata correttamente"""
    assert app.config['TESTING'] == True


