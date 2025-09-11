from django.test import TestCase, Client
from django.contrib.auth.models import User
from stadiapp.models import Stadium
import json

class StadiumAPITestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.stadium = Stadium.objects.create(
            name='Fenway Park',
            sport='Baseball',
            city='Boston',
            state='Massachusetts',
            capacity=37755
        )

    def test_get_stadium(self):
        """Test retrieving a single stadium"""
        response = self.client.get(f'/api/stadiums/{self.stadium.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], 'Fenway Park')
        self.assertEqual(data['sport'], 'Baseball')
        self.assertEqual(data['capacity'], 37755)

    def test_get_stadium_not_found(self):
        """Test 404 for non-existent stadium"""
        response = self.client.get('/api/stadiums/999')
        self.assertEqual(response.status_code, 404)

    def test_list_stadiums(self):
        """Test retrieving all stadiums"""
        # Create additional stadiums
        Stadium.objects.create(
            name='Yankee Stadium',
            sport='Baseball',
            city='New York',
            state='New York',
            capacity=54251
        )
        Stadium.objects.create(
            name='Gillette Stadium',
            sport='Football',
            city='Foxborough',
            state='Massachusetts',
            capacity=65878
        )

        response = self.client.get('/api/stadiums')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 3)  # Including the one from setUp

    def test_create_stadium(self):
        """Test creating a new stadium"""
        payload = {
            'name': 'TD Garden',
            'sport': 'Basketball',
            'city': 'Boston',
            'state': 'Massachusetts',
            'capacity': 19580
        }
        response = self.client.post('/api/stadiums', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify stadium was created
        stadium = Stadium.objects.get(name='TD Garden')
        self.assertEqual(stadium.sport, 'Basketball')
        self.assertEqual(stadium.capacity, 19580)

    def test_create_stadium_invalid_data(self):
        """Test validation on invalid stadium data"""
        payload = {
            'name': '',  # Invalid: empty name
            'sport': 'Basketball',
            'city': 'Boston',
            'state': 'Massachusetts',
            'capacity': -1000  # Invalid: negative capacity
        }
        response = self.client.post('/api/stadiums',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 422)  # Validation error

    def test_create_stadium_duplicate_name(self):
        """Test creating stadium with duplicate name"""
        payload = {
            'name': 'Fenway Park',  # Already exists
            'sport': 'Basketball',
            'city': 'Boston',
            'state': 'Massachusetts',
            'capacity': 20000
        }
        # This should fail due to unique constraint
        response = self.client.post('/api/stadiums',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        # Should return an error (400 or 500 depending on how errors are handled)
        self.assertNotEqual(response.status_code, 200)

    def test_update_stadium(self):
        """Test updating stadium data"""
        payload = {
            'name': 'Fenway Park',
            'sport': 'Baseball',
            'city': 'Boston',
            'state': 'Massachusetts',
            'capacity': 37800  # Updated capacity
        }
        response = self.client.put(f'/api/stadiums/{self.stadium.id}',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify update
        self.stadium.refresh_from_db()
        self.assertEqual(self.stadium.capacity, 37800)

    def test_update_stadium_not_found(self):
        """Test updating non-existent stadium"""
        payload = {
            'name': 'New Stadium',
            'sport': 'Football',
            'city': 'Boston',
            'state': 'Massachusetts',
            'capacity': 50000
        }
        response = self.client.put('/api/stadiums/999',
                                  data=json.dumps(payload),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_delete_stadium(self):
        """Test deleting a stadium"""
        response = self.client.delete(f'/api/stadiums/{self.stadium.id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['success'], True)
        
        # Verify deletion
        self.assertFalse(Stadium.objects.filter(id=self.stadium.id).exists())

    def test_delete_stadium_not_found(self):
        """Test deleting non-existent stadium"""
        response = self.client.delete('/api/stadiums/999')
        self.assertEqual(response.status_code, 404)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/healthcheck')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'ok')

class StadiumModelTestCase(TestCase):
    """Unit tests for Stadium model"""
    
    def test_stadium_creation(self):
        """Test stadium model creation"""
        stadium = Stadium.objects.create(
            name='Test Stadium',
            sport='Soccer',
            city='Test City',
            state='Test State',
            capacity=50000
        )
        self.assertTrue(isinstance(stadium, Stadium))
        self.assertEqual(stadium.name, 'Test Stadium')
        self.assertEqual(stadium.capacity, 50000)

    def test_stadium_str_method(self):
        """Test string representation of stadium"""
        stadium = Stadium(name='Test Stadium')
        self.assertEqual(str(stadium), 'Test Stadium')

    def test_stadium_default_capacity(self):
        """Test default capacity is 0"""
        stadium = Stadium.objects.create(
            name='New Stadium',
            sport='Hockey',
            city='New City',
            state='New State'
        )
        self.assertEqual(stadium.capacity, 0)

    def test_stadium_unique_name_constraint(self):
        """Test that stadium names must be unique"""
        Stadium.objects.create(
            name='Unique Stadium',
            sport='Baseball',
            city='City',
            state='State'
        )
        
        # Try to create another with same name
        with self.assertRaises(Exception):
            Stadium.objects.create(
                name='Unique Stadium',  # Duplicate name
                sport='Football',
                city='Other City',
                state='Other State'
            )

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

class StadiumIntegrationTestCase(TestCase):
    """Integration tests for Stadium API"""
    
    def setUp(self):
        self.client = Client()
    
    def test_stadium_workflow(self):
        """Test complete stadium CRUD workflow"""
        # Create stadium
        create_data = {
            'name': 'Integration Stadium',
            'sport': 'Soccer',
            'city': 'Integration City',
            'state': 'Integration State',
            'capacity': 45000
        }
        
        response = self.client.post('/api/stadiums', 
                                   data=json.dumps(create_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        created_data = response.json()
        stadium_id = created_data['id']
        
        # Retrieve stadium
        response = self.client.get(f'/api/stadiums/{stadium_id}')
        self.assertEqual(response.status_code, 200)
        retrieved_data = response.json()
        self.assertEqual(retrieved_data['name'], 'Integration Stadium')
        self.assertEqual(retrieved_data['capacity'], 45000)
        
        # Update stadium
        update_data = {
            'name': 'Updated Integration Stadium',
            'sport': 'Soccer',
            'city': 'Integration City',
            'state': 'Integration State',
            'capacity': 50000
        }
        response = self.client.put(f'/api/stadiums/{stadium_id}',
                                  data=json.dumps(update_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify update
        response = self.client.get(f'/api/stadiums/{stadium_id}')
        updated_data = response.json()
        self.assertEqual(updated_data['name'], 'Updated Integration Stadium')
        self.assertEqual(updated_data['capacity'], 50000)
        
        # List stadiums (should include our stadium)
        response = self.client.get('/api/stadiums')
        self.assertEqual(response.status_code, 200)
        stadiums_list = response.json()
        stadium_names = [stadium['name'] for stadium in stadiums_list]
        self.assertIn('Updated Integration Stadium', stadium_names)
        
        # Delete stadium
        response = self.client.delete(f'/api/stadiums/{stadium_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        response = self.client.get(f'/api/stadiums/{stadium_id}')
        self.assertEqual(response.status_code, 404)

class StadiumFilteringTestCase(TestCase):
    """Test filtering and querying stadiums"""
    
    def setUp(self):
        self.client = Client()
        # Create test stadiums
        Stadium.objects.create(name='Fenway Park', sport='Baseball', city='Boston', state='Massachusetts', capacity=37755)
        Stadium.objects.create(name='Yankee Stadium', sport='Baseball', city='New York', state='New York', capacity=54251)
        Stadium.objects.create(name='Gillette Stadium', sport='Football', city='Foxborough', state='Massachusetts', capacity=65878)
        Stadium.objects.create(name='TD Garden', sport='Basketball', city='Boston', state='Massachusetts', capacity=19580)
        
    def test_list_all_stadiums(self):
        """Test listing all stadiums returns correct count"""
        response = self.client.get('/api/stadiums')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 4)
    
    def test_stadium_data_structure(self):
        """Test that returned stadium data has correct structure"""
        response = self.client.get('/api/stadiums')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check first stadium has all required fields
        stadium = data[0]
        required_fields = ['id', 'name', 'sport', 'city', 'state', 'capacity']
        for field in required_fields:
            self.assertIn(field, stadium)

class StadiumErrorHandlingTestCase(TestCase):
    """Test error handling scenarios"""
    
    def setUp(self):
        self.client = Client()
    
    def test_invalid_json_payload(self):
        """Test handling of malformed JSON"""
        invalid_json = '{"name": "Test Stadium", "sport": "Baseball"'  # Missing closing brace
        
        response = self.client.post('/api/stadiums',
                                   data=invalid_json,
                                   content_type='application/json')
        # Should return 400 Bad Request for malformed JSON
        self.assertEqual(response.status_code, 400)
    
    def test_missing_content_type(self):
        """Test POST without content-type header"""
        payload = {
            'name': 'Test Stadium',
            'sport': 'Baseball',
            'city': 'Test City',
            'state': 'Test State',
            'capacity': 30000
        }
        
        # Send without content-type (will default to form data)
        response = self.client.post('/api/stadiums', data=payload)
        # This might fail depending on how Django Ninja handles form data
        self.assertNotEqual(response.status_code, 500)  # Should not cause server error
    
    def test_empty_request_body(self):
        """Test POST with empty request body"""
        response = self.client.post('/api/stadiums',
                                   data='',
                                   content_type='application/json')
        self.assertIn(response.status_code, [400, 422])  # Should return client error
    
    def test_extra_fields_in_payload(self):
        """Test handling of extra fields in request"""
        payload = {
            'name': 'Extra Fields Stadium',
            'sport': 'Baseball',
            'city': 'Test City',
            'state': 'Test State',
            'capacity': 30000,
            'extra_field': 'should be ignored',
            'another_extra': 123
        }
        
        response = self.client.post('/api/stadiums',
                                   data=json.dumps(payload),
                                   content_type='application/json')
        # Should succeed and ignore extra fields
        self.assertEqual(response.status_code, 200)
        
        # Verify stadium was created correctly
        stadium = Stadium.objects.get(name='Extra Fields Stadium')
        self.assertEqual(stadium.sport, 'Baseball')