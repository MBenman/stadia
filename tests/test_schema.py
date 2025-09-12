from django.test import TestCase, Client
from django.contrib.auth.models import User
from stadiapp.models import Stadium
import json

class StadiumSchemaTestCase(TestCase):
    """Test Ninja schemas and validation"""
    
    def test_stadium_input_schema_valid(self):
        """Test valid stadium input schema"""
        from stadiapp.schemas import CreateStadiumSchema
        
        valid_data = {
            'name': 'Valid Stadium',
            'sport': 'Tennis',
            'city': 'Valid City',
            'state': 'Valid State',
            'capacity': 15000
        }
        schema = CreateStadiumSchema(**valid_data)
        self.assertEqual(schema.name, 'Valid Stadium')
        self.assertEqual(schema.capacity, 15000)

    def test_stadium_input_schema_invalid(self):
        """Test invalid stadium input schema"""
        from stadiapp.schemas import CreateStadiumSchema
        from pydantic import ValidationError
        
        invalid_data = {
            'name': '',  # Should not be empty
            'sport': 'Tennis',
            'city': 'Valid City',
            'state': 'Valid State',
            'capacity': -100  # Negative capacity
        }
        
        with self.assertRaises(ValidationError):
            CreateStadiumSchema(**invalid_data)