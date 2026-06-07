# tests/skechers/api_endpoints.py

"""
Skechers E-commerce API Endpoints and Request Builders.

All API knowledge lives here. Tests only pass field values to builders.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== CONFIG ====================

API_BASE_URL = os.getenv("SKECHERS_API_URL", "https://api.skechers.com")
API_AUTH_TOKEN = os.getenv("SKECHERS_API_TOKEN", "")
API_TIMEOUT = 30

# ==================== ENDPOINTS ====================

GET_PRODUCTS = "/products"
GET_PRODUCT_BY_ID = "/products/{product_id}"
SEARCH_PRODUCTS = "/products/search"
GET_CATEGORIES = "/categories"
GET_CATEGORY_BY_ID = "/categories/{category_id}"
CREATE_ORDER = "/orders"
GET_ORDER_BY_ID = "/orders/{order_id}"
GET_CART = "/cart"
ADD_TO_CART = "/cart/items"
GET_REVIEWS = "/products/{product_id}/reviews"


# ==================== BUILDERS ====================

def build_get_products(limit=20, offset=0, category=None, **overrides):
    """Build GET products request."""
    params = {"limit": limit, "offset": offset}
    if category:
        params["category"] = category
    params.update(overrides)
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": GET_PRODUCTS,
        "auth_token": API_AUTH_TOKEN,
        "params": params,
    }


def build_get_product_by_id(product_id="12345"):
    """Build GET product by ID request."""
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": GET_PRODUCT_BY_ID.format(product_id=product_id),
        "auth_token": API_AUTH_TOKEN,
    }


def build_search_products(query="shoes", limit=10, **overrides):
    """Build product search request."""
    params = {"q": query, "limit": limit}
    params.update(overrides)
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": SEARCH_PRODUCTS,
        "auth_token": API_AUTH_TOKEN,
        "params": params,
    }


def build_get_categories():
    """Build GET categories request."""
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": GET_CATEGORIES,
        "auth_token": API_AUTH_TOKEN,
    }


def build_create_order(product_id="12345", qty=1, size="10",
                       shipping="standard", **overrides):
    """Build create order request."""
    payload = {
        "items": [{"productId": product_id, "quantity": qty, "size": size}],
        "shipping": shipping,
        "status": "pending"
    }
    payload.update(overrides)
    return {
        "method": "POST",
        "base_url": API_BASE_URL,
        "endpoint": CREATE_ORDER,
        "auth_token": API_AUTH_TOKEN,
        "payload": payload,
    }


def build_add_to_cart(product_id="12345", qty=1, size="10", **overrides):
    """Build add to cart request."""
    payload = {"productId": product_id, "quantity": qty, "size": size}
    payload.update(overrides)
    return {
        "method": "POST",
        "base_url": API_BASE_URL,
        "endpoint": ADD_TO_CART,
        "auth_token": API_AUTH_TOKEN,
        "payload": payload,
    }


def build_get_reviews(product_id="12345", limit=10):
    """Build GET product reviews request."""
    return {
        "method": "GET",
        "base_url": API_BASE_URL,
        "endpoint": GET_REVIEWS.format(product_id=product_id),
        "auth_token": API_AUTH_TOKEN,
        "params": {"limit": limit},
    }
