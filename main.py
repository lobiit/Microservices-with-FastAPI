from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-10343.c90.us-east-1-3.ec2.cloud.redislabs.com",
    port=10343,

    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'product': product.quantity,
    }


# Getting a single product
@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get_single_product(pk: str):
    return Product.get(pk)


# @app.patch('/products/{pk}')
# def update(product: Product):
#     return Product.save()
#

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)
