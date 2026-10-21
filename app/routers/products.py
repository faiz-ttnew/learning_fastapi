from fastapi import APIRouter, HTTPException, Query
from app.schemas.product_schema import Product
from app.services.product_service import (
    get_all_products,
    get_product_by_id,
    search_product
)

router = APIRouter(
    prefix='/products',
    tags=['Products']
)

@router.get('/', response_model=list[Product])
def fetch_products():
    """Return all products."""
    return get_all_products()

@router.get('/search')
def search_products(category: str = Query(...)):
    print('category', category)
    prod = search_product(category)
    if prod is None:
        HTTPException(
            status_code=404,
            detail='Product not found'
        )
    return prod

@router.get('/{id}', response_model=Product)
def fetch_product(id: int):
    prod = get_product_by_id(id)

    if prod is None:
        HTTPException(
            status_code=404,
            detail='Product not found'
        )
        return prod
