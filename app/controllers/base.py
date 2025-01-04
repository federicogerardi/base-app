from flask import Blueprint, jsonify

class BaseController:
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self):
        items = self.model_class.query.all()
        return jsonify([item.to_dict() for item in items])
