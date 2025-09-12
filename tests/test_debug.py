from django.test import TestCase, Client
from stadiapp.models import Stadium
import json

class DebugStadiumAPITestCase(TestCase):
    """Debug tests to understand what's happening with the API"""
    
    def setUp(self):
        self.client = Client()
        self.stadium = Stadium.objects.create(
            name='Debug Stadium',
            sport='Baseball',
            city='Debug City',
            state='Debug State',
            capacity=50000
        )
    
    def test_debug_create_stadium_simple(self):
        """Debug: Test creating stadium with minimal payload"""
        payload = {
            'name': 'Simple Stadium',
            'sport': 'Baseball',
            'city': 'Simple City',
            'state': 'Simple State'
        }
        
        response = self.client.post('/api/stadiums', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        print(f"Simple create response status: {response.status_code}")
        print(f"Simple create response content: {response.content}")
        
        # Try without capacity field
        if response.status_code != 200:
            # Let's see what the error is
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Could not parse error response as JSON")
    
    def test_debug_create_stadium_with_capacity(self):
        """Debug: Test creating stadium with capacity"""
        payload = {
            'name': 'Capacity Stadium',
            'sport': 'Football',
            'city': 'Capacity City',
            'state': 'Capacity State',
            'capacity': 75000
        }
        
        response = self.client.post('/api/stadiums', 
                                   data=json.dumps(payload),
                                   content_type='application/json')
        
        print(f"With capacity response status: {response.status_code}")
        print(f"With capacity response content: {response.content}")
        
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"Capacity error details: {error_data}")
            except:
                print(f"Could not parse capacity error response as JSON")
    
    def test_debug_different_content_types(self):
        """Debug: Test different ways of sending data"""
        payload = {
            'name': 'Content Type Stadium',
            'sport': 'Basketball',
            'city': 'Content City',
            'state': 'Content State',
            'capacity': 20000
        }
        
        # Test 1: JSON with proper content type
        print("=== Testing JSON with application/json ===")
        response1 = self.client.post('/api/stadiums', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        print(f"JSON response: {response1.status_code}, {response1.content}")
        
        # Test 2: Form data
        print("=== Testing form data ===")
        response2 = self.client.post('/api/stadiums', data=payload)
        print(f"Form response: {response2.status_code}, {response2.content}")
        
        # Test 3: JSON without content type
        print("=== Testing JSON without content-type ===")
        response3 = self.client.post('/api/stadiums',
                           data=json.dumps(payload),
                           content_type='application/json')
        print(f"No content-type response: {response3.status_code}, {response3.content}")
    
    def test_debug_schema_import(self):
        """Debug: Test if schemas can be imported"""
        try:
            from stadiapp.schemas import CreateStadiumSchema, StadiumSchema
            print("✓ Schemas imported successfully")
            
            # Test creating schema instances
            test_data = {
                'name': 'Schema Test',
                'sport': 'Soccer',
                'city': 'Schema City',
                'state': 'Schema State',
                'capacity': 30000
            }
            
            try:
                create_schema = CreateStadiumSchema(**test_data)
                print(f"✓ CreateStadiumSchema created: {create_schema}")
                print(f"  name: {create_schema.name}")
                print(f"  capacity: {create_schema.capacity}")
                print(f"  capacity type: {type(create_schema.capacity)}")
            except Exception as e:
                print(f"✗ Error creating CreateStadiumSchema: {e}")
            
            # Test with stadium instance
            try:
                stadium_schema = StadiumSchema.from_orm(self.stadium)
                print(f"✓ StadiumSchema created from model: {stadium_schema}")
            except Exception as e:
                print(f"✗ Error creating StadiumSchema from model: {e}")
                
        except ImportError as e:
            print(f"✗ Could not import schemas: {e}")
    
    def test_debug_api_endpoints(self):
        """Debug: Test which endpoints actually exist"""
        endpoints_to_test = [
            '/api/stadiums',
            '/api/stadiums/',
            '/stadiums',
            '/stadiums/',
        ]
        
        for endpoint in endpoints_to_test:
            response = self.client.get(endpoint)
            print(f"GET {endpoint}: {response.status_code}")
    
    def test_debug_get_stadium_works(self):
        """Debug: Verify GET endpoints work"""
        # Test list
        response = self.client.get('/api/stadiums')
        print(f"List stadiums: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Number of stadiums: {len(data)}")
            if data:
                print(f"First stadium: {data[0]}")
        
        # Test detail
        response = self.client.get(f'/api/stadiums/{self.stadium.id}')
        print(f"Get stadium detail: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Stadium detail: {data}")
    
    def test_debug_minimal_create(self):
        """Debug: Try creating with absolute minimal data"""
        # Test what happens if we only send required fields
        minimal_payloads = [
            {'name': 'Minimal1'},
            {'name': 'Minimal2', 'sport': 'Test'},
            {'name': 'Minimal3', 'sport': 'Test', 'city': 'Test'},
            {'name': 'Minimal4', 'sport': 'Test', 'city': 'Test', 'state': 'Test'},
        ]
        
        for i, payload in enumerate(minimal_payloads):
            response = self.client.post('/api/stadiums',
                                       data=json.dumps(payload),
                                       content_type='application/json')
            print(f"Minimal payload {i+1}: {response.status_code}")
            if response.status_code != 200:
                print(f"  Error: {response.content}")

class DebugSchemaTestCase(TestCase):
    """Debug schema behavior specifically"""
    
    def test_debug_schema_fields(self):
        """Debug: Check what fields are expected by schemas"""
        try:
            from stadiapp.schemas import CreateStadiumSchema
            
            # Get schema info
            schema_info = CreateStadiumSchema.schema()
            print("CreateStadiumSchema info:")
            print(f"Required fields: {schema_info.get('required', [])}")
            print(f"Properties: {list(schema_info.get('properties', {}).keys())}")
            
            # Check each field
            for field_name, field_info in schema_info.get('properties', {}).items():
                print(f"  {field_name}: {field_info.get('type')} (default: {field_info.get('default', 'No default')})")
                
        except Exception as e:
            print(f"Error getting schema info: {e}")