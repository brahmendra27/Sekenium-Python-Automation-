# tests/api/test_api_example.py

"""
Example API tests demonstrating REST API testing capabilities.
This example uses JSONPlaceholder API for demonstration.
"""

import pytest
from framework.api_client import APIClient, APIResponse


class TestAPIBasics:
    """Basic API testing examples."""
    
    def test_get_request(self, api_client):
        """Test GET request to retrieve data."""
        response = api_client.get('/posts/1')
        
        # Assert status code
        assert response.status_code == 200
        
        # Parse and validate response
        data = response.json()
        assert 'id' in data
        assert data['id'] == 1
        assert 'title' in data
        assert 'body' in data
    
    def test_get_with_query_params(self, api_client):
        """Test GET request with query parameters."""
        response = api_client.get('/posts', params={'userId': 1})
        
        assert response.status_code == 200
        
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0
        
        # Verify all posts belong to userId 1
        for post in posts:
            assert post['userId'] == 1
    
    def test_post_request(self, api_client):
        """Test POST request to create data."""
        new_post = {
            'title': 'Test Post',
            'body': 'This is a test post body',
            'userId': 1
        }
        
        response = api_client.post('/posts', json_data=new_post)
        
        assert response.status_code == 201
        
        created_post = response.json()
        assert created_post['title'] == new_post['title']
        assert created_post['body'] == new_post['body']
        assert created_post['userId'] == new_post['userId']
        assert 'id' in created_post
    
    def test_put_request(self, api_client):
        """Test PUT request to update data."""
        updated_post = {
            'id': 1,
            'title': 'Updated Title',
            'body': 'Updated body content',
            'userId': 1
        }
        
        response = api_client.put('/posts/1', json_data=updated_post)
        
        assert response.status_code == 200
        
        result = response.json()
        assert result['title'] == updated_post['title']
        assert result['body'] == updated_post['body']
    
    def test_patch_request(self, api_client):
        """Test PATCH request to partially update data."""
        partial_update = {
            'title': 'Patched Title'
        }
        
        response = api_client.patch('/posts/1', json_data=partial_update)
        
        assert response.status_code == 200
        
        result = response.json()
        assert result['title'] == partial_update['title']
    
    def test_delete_request(self, api_client):
        """Test DELETE request."""
        response = api_client.delete('/posts/1')
        
        assert response.status_code == 200


class TestAPIResponseWrapper:
    """Test using APIResponse wrapper for enhanced assertions."""
    
    def test_response_wrapper_assertions(self, api_client, api_response_wrapper):
        """Test APIResponse wrapper assertion methods."""
        response = api_client.get('/posts/1')
        api_response = api_response_wrapper(response)
        
        # Status code assertions
        api_response.assert_status_code(200)
        api_response.assert_status_in([200, 201])
        
        # JSON content assertions
        api_response.assert_json_contains('id')
        api_response.assert_json_contains('title')
        api_response.assert_json_value('id', 1)
        
        # Header assertions
        api_response.assert_header_exists('Content-Type')
        
        # Get JSON values
        title = api_response.get_json_value('title')
        assert title is not None
    
    def test_response_wrapper_with_list(self, api_client, api_response_wrapper):
        """Test APIResponse wrapper with list response."""
        response = api_client.get('/posts')
        api_response = api_response_wrapper(response)
        
        api_response.assert_status_code(200)
        
        posts = api_response.json_data
        assert isinstance(posts, list)
        assert len(posts) > 0


class TestAPIAuthentication:
    """Test API authentication scenarios."""
    
    def test_with_auth_token(self, api_client):
        """Test API request with authentication token."""
        # Set authentication token
        api_client.set_auth_token('fake-token-12345')
        
        # Make request (will include Authorization header)
        response = api_client.get('/posts/1')
        
        assert response.status_code == 200
        
        # Clean up - remove auth header
        api_client.remove_header('Authorization')
    
    def test_with_custom_headers(self, api_client):
        """Test API request with custom headers."""
        custom_headers = {
            'X-Custom-Header': 'CustomValue',
            'X-Request-ID': '12345'
        }
        
        response = api_client.get('/posts/1', headers=custom_headers)
        
        assert response.status_code == 200


class TestAPIErrorHandling:
    """Test API error handling scenarios."""
    
    def test_not_found_error(self, api_client):
        """Test handling of 404 Not Found error."""
        response = api_client.get('/posts/99999')
        
        assert response.status_code == 404
    
    def test_invalid_endpoint(self, api_client):
        """Test handling of invalid endpoint."""
        response = api_client.get('/invalid-endpoint')
        
        # Should handle gracefully without raising exception
        assert response.status_code in [404, 400]
    
    def test_response_validation_failure(self, api_client, api_response_wrapper):
        """Test response validation failure."""
        response = api_client.get('/posts/99999')
        api_response = api_response_wrapper(response)
        
        # This should raise AssertionError
        with pytest.raises(AssertionError):
            api_response.assert_status_code(200)


class TestAPIDataValidation:
    """Test API response data validation."""
    
    def test_validate_post_structure(self, api_client):
        """Test that post has expected structure."""
        response = api_client.get('/posts/1')
        post = response.json()
        
        # Validate required fields
        required_fields = ['userId', 'id', 'title', 'body']
        for field in required_fields:
            assert field in post, f"Missing required field: {field}"
        
        # Validate data types
        assert isinstance(post['userId'], int)
        assert isinstance(post['id'], int)
        assert isinstance(post['title'], str)
        assert isinstance(post['body'], str)
    
    def test_validate_posts_list(self, api_client):
        """Test that posts list has valid structure."""
        response = api_client.get('/posts')
        posts = response.json()
        
        assert isinstance(posts, list)
        assert len(posts) > 0
        
        # Validate first post structure
        first_post = posts[0]
        assert 'id' in first_post
        assert 'userId' in first_post
        assert 'title' in first_post
        assert 'body' in first_post


@pytest.mark.parametrize("post_id", [1, 2, 3, 4, 5])
def test_multiple_posts(api_client, post_id):
    """Test retrieving multiple posts using parametrization."""
    response = api_client.get(f'/posts/{post_id}')
    
    assert response.status_code == 200
    
    post = response.json()
    assert post['id'] == post_id
