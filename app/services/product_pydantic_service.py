from fastapi import HTTPException
from app.schemas.product_pydantic_schema import(
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

products = dict[int, ProductResponse] = {}
next_employee_id = 2

def get_all_products(
        name: str | None = None,
        skip: int = 0,
        limit: int = 10
):
    result = list(products.values())

    if name is not None:
        result = [
            prod for prod in result
            if prod.name.lower() == name.lower()
        ]
    return result[skip: skip + limit]

def get_product_by_id(id: int):
    for prod in products:
        if prod['id']==id:
            return prod

    return None

def search_product(category: str):
    result = []

    for prod in products:
        if category.lower() in prod['category'].lower():
            result.append(prod)
    return result