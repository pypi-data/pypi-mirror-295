# Usage
```python
from tortoise import Model, fields
from tortoise_factory import model_factory


class User(Model):
    id = fields.IntField(primary_key=True)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    email = fields.CharField(max_length=200)


class Product(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=200)
    description = fields.TextField(null=True, default=None)
    price = fields.FloatField()
    created_by = fields.ForeignKeyField(
        "models.User",
        on_delete=fields.CASCADE,
        related_name="products",
    )

    def __str__(self) -> str:
        return self.name
```
## Generalities
All returned models are saved in db, meaning they will all have a `.id` value, the same is true for any ForeignKeyField


## Random values
To get a simple random product:
```python
product = await model_factory(Product)
```
the `created_by` will be created automaticaly since it cannot be None, when possible, the factory will put None into optional fields.


## Specify some fields
```python
product = await model_factory(Product, name="something", created_by__name="Bob")
```
we use `__` to go throught relations


## Fill optional values
```python
product = await model_factory(Product, _optionals=["description"])
```

now you will have a `product.description` wich won't be `None`

