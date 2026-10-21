products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 55000,
        "category": "Electronics"
    },
    {
        "id": 2,
        "name": "Keyboard",
        "price": 1500,
        "category": "Accessories"
    },
    {
        "id": 3,
        "name": "Mouse",
        "price": 700,
        "category": "Accessories"
    }
]

def get_all_products():
    return products

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