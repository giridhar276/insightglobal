

products = [
    {"id": 101, "name": "Laptop", "price": 75000},
    {"id": 102, "name": "Mobile", "price": 25000},
    {"id": 103, "name": "Tablet", "price": 15000}
]


if isinstance(products, list):
    for item in products:
        if isinstance(item, dict):
            print(item['name'] , item['price'])