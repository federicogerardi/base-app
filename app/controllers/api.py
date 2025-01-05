"""
Controller per le API
"""
from flask_restx import Resource, Namespace

# Crea il namespace principale
api_ns = Namespace('', description='API operations')

@api_ns.route('/')
class APIController(Resource):
    @api_ns.doc('get_status')
    @api_ns.response(200, 'Success')
    @api_ns.response(429, 'Too Many Requests')
    def get(self):
        """Endpoint principale dell'API"""
        return {
            'success': True,
            'message': 'Flask API is running'
        }
    
    @api_ns.doc('post_test')
    @api_ns.response(200, 'Success')
    @api_ns.response(429, 'Too Many Requests')
    def post(self):
        """Test endpoint POST"""
        return {
            'success': True,
            'message': 'POST request processed successfully'
        }