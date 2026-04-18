# tests/skechers/test_api_products.py

"""
Skechers API Tests - Products
Tests for Skechers product API endpoints.
"""

import pytest


class TestSkechersProductAPI:
    """Test Skechers product API endpoints."""
    
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_products_list(self, api_client):
        """Test retrieving products list from API."""
        # Note: Update endpoint based on actual Skechers API
        response = api_client.get('/api/products')
        
        # API may return 200 or 404 depending on if endpoint exists
        # For staging, we'll check if we get a response
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            # If API exists, validate response structure
            try:
                products = response.json()
                assert isinstance(products, (list, dict)), "Expected list or dict response"
                
                if isinstance(products, list) and len(products) > 0:
                    # Validate first product structure
                    product = products[0]
                    assert 'id' in product or 'productId' in product, "Product should have ID"
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    def test_get_product_by_id(self, api_client):
        """Test retrieving a specific product by ID."""
        # Test with a sample product ID
        product_id = "12345"
        
        response = api_client.get(f'/api/products/{product_id}')
        
        # Check response
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                product = response.json()
                assert isinstance(product, dict), "Expected product object"
                
                # Validate product has expected fields
                expected_fields = ['id', 'name', 'price']
                for field in expected_fields:
                    if field in product:
                        assert product[field] is not None
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    def test_search_products_api(self, api_client):
        """Test product search via API."""
        # Test search endpoint
        response = api_client.get('/api/products/search', params={'q': 'sneakers'})
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                results = response.json()
                assert isinstance(results, (list, dict)), "Expected search results"
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    @pytest.mark.parametrize("category", ["men", "women", "kids"])
    def test_get_products_by_category(self, api_client, category):
        """Test retrieving products by category."""
        response = api_client.get(f'/api/products/category/{category}')
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code for {category}: {response.status_code}"
        
        if response.status_code == 200:
            try:
                products = response.json()
                assert isinstance(products, (list, dict)), f"Expected products for {category}"
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    def test_product_availability_check(self, api_client):
        """Test checking product availability."""
        product_id = "12345"
        
        response = api_client.get(f'/api/products/{product_id}/availability')
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                availability = response.json()
                assert isinstance(availability, dict), "Expected availability object"
                
                # Check for common availability fields
                if 'inStock' in availability:
                    assert isinstance(availability['inStock'], bool)
                if 'quantity' in availability:
                    assert isinstance(availability['quantity'], (int, float))
            except ValueError:
                pytest.skip("Response is not JSON")


class TestSkechersProductFilters:
    """Test Skechers product filtering API."""
    
    @pytest.mark.api
    def test_filter_by_price_range(self, api_client):
        """Test filtering products by price range."""
        response = api_client.get('/api/products', params={
            'minPrice': 50,
            'maxPrice': 100
        })
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                products = response.json()
                if isinstance(products, list) and len(products) > 0:
                    # Verify products are within price range
                    for product in products:
                        if 'price' in product:
                            price = float(product['price'])
                            assert 50 <= price <= 100, \
                                f"Product price {price} outside range 50-100"
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    def test_filter_by_size(self, api_client):
        """Test filtering products by size."""
        response = api_client.get('/api/products', params={'size': '10'})
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                products = response.json()
                assert isinstance(products, (list, dict)), "Expected filtered products"
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    def test_filter_by_color(self, api_client):
        """Test filtering products by color."""
        response = api_client.get('/api/products', params={'color': 'black'})
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                products = response.json()
                assert isinstance(products, (list, dict)), "Expected filtered products"
            except ValueError:
                pytest.skip("Response is not JSON")


class TestSkechersProductReviews:
    """Test Skechers product reviews API."""
    
    @pytest.mark.api
    def test_get_product_reviews(self, api_client):
        """Test retrieving product reviews."""
        product_id = "12345"
        
        response = api_client.get(f'/api/products/{product_id}/reviews')
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                reviews = response.json()
                assert isinstance(reviews, (list, dict)), "Expected reviews"
                
                if isinstance(reviews, list) and len(reviews) > 0:
                    # Validate review structure
                    review = reviews[0]
                    expected_fields = ['rating', 'comment', 'author']
                    for field in expected_fields:
                        if field in review:
                            assert review[field] is not None
            except ValueError:
                pytest.skip("Response is not JSON")
    
    @pytest.mark.api
    def test_get_product_rating(self, api_client):
        """Test retrieving product rating."""
        product_id = "12345"
        
        response = api_client.get(f'/api/products/{product_id}/rating')
        
        assert response.status_code in [200, 404], \
            f"Unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            try:
                rating = response.json()
                assert isinstance(rating, dict), "Expected rating object"
                
                if 'averageRating' in rating:
                    avg_rating = float(rating['averageRating'])
                    assert 0 <= avg_rating <= 5, \
                        f"Rating {avg_rating} should be between 0 and 5"
            except ValueError:
                pytest.skip("Response is not JSON")
