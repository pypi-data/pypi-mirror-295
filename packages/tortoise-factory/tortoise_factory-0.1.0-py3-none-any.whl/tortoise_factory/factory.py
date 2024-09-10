from collections.abc import Sequence, Type, TypeVar
from enum import Enum

import faker
from tortoise import Model, fields
from tortoise.contrib.postgres.fields import ArrayField
from tortoise.exceptions import IntegrityError
from tortoise.fields.data import CharEnumFieldInstance
from tortoise.fields.relational import ForeignKeyFieldInstance, ManyToManyFieldInstance

T = TypeVar("T", bound=Model)
TEXT_FIELD_LENGTH: int = 1000


def _extract_implicit_optionals(
    optionals: Sequence[str] | None,
    **kwargs,
) -> set[str]:
    """return the list of all optionals with included kwargs implcit ones."""
    return set(
        (list(optionals) if optionals else [])
        + list([field_name.split("__", 1)[0] for field_name in kwargs.keys()])
    )


async def model_factory(
    model_class: Type[T],  # type: ignore[misc]
    /,
    _optionals: Sequence[str] | None = None,
    **kwargs,
) -> T:  # type: ignore[misc]
    """Construct `model_class` (based on tortoise.models.Model) with random generated values

    you can pass values directly using keyword arguments.
    ex: await model_factory(User, first_name="Bill")

    you can also pass nested optional arguments using __ for relation
    ex: await model_factory(Project, title="Test Project", created_by__first_name="Bill")

    you can also use `optionals` to set fields that access NULL in the db to a random generated value
    """
    fake = faker.Faker()
    model_kwargs = dict(
        {k: v for k, v in kwargs.items() if k in model_class._meta.fields}
    )
    optionals = _extract_implicit_optionals(_optionals, **kwargs)
    for field_name, field in model_class._meta.fields_map.items():
        if isinstance(field, fields.BackwardFKRelation) or field_name == "id":
            continue

        if field.null and field_name not in optionals:
            model_kwargs.setdefault(field_name, None)

        elif field.default and field_name not in optionals:
            value = field.default
            try:
                # for enums we want to get the value behind the num
                if isinstance(field, Enum):
                    value = field.default.value
            except (ValueError, TypeError):
                pass
            model_kwargs.setdefault(field_name, value)
        elif isinstance(field, ForeignKeyFieldInstance):
            # do not create a new instance if the kwargs were provided
            # but add the fieldname_id with the instance id instead
            field_name_id = f"{field_name}_id"
            if field_name in kwargs:
                model_kwargs[field_name_id] = kwargs[field_name].id
                continue

            prefix = f"{field_name}__"
            instance = await model_factory(
                field.related_model,
                **{
                    k.removeprefix(prefix): v
                    for k, v in kwargs.items()
                    if k.startswith(prefix)
                },
            )
            model_kwargs[field_name] = instance
            model_kwargs[field_name_id] = instance.id

        elif isinstance(field, CharEnumFieldInstance):
            values = list(item.value for item in field.enum_type)
            model_kwargs.setdefault(
                field_name, fake.random_choices(values, length=1)[0]
            )
        elif isinstance(field, ArrayField):
            model_kwargs.setdefault(field_name, [])
        elif isinstance(field, ManyToManyFieldInstance):
            continue
        else:
            match type(field):
                case fields.IntField:
                    if not field_name.endswith("_id"):
                        min_value = (
                            max(
                                [
                                    validator.min_value
                                    for validator in field.validators
                                    if hasattr(validator, "min_value")
                                ]
                            )
                            if field.validators
                            else 0
                        )
                        model_kwargs.setdefault(
                            field_name, fake.random_int(min=min_value)
                        )
                case fields.FloatField:
                    model_kwargs.setdefault(
                        field_name, faker.random.random_number(digits=2)
                    )
                case fields.CharField:
                    model_kwargs.setdefault(
                        field_name,
                        "".join(fake.random_letters(length=field.max_length)),
                    )
                case fields.TextField:
                    model_kwargs.setdefault(
                        field_name,
                        "".join(fake.random_letters(length=TEXT_FIELD_LENGTH)),
                    )
                case fields.DateField:
                    model_kwargs.setdefault(
                        field_name, fake.date_this_year(before_today=False)
                    )
                case fields.DatetimeField:
                    model_kwargs.setdefault(
                        field_name, fake.date_time_this_year(before_now=False)
                    )
                case fields.BooleanField:
                    model_kwargs.setdefault(field_name, fake.boolean())
                case fields.BackwardFKRelation:
                    ...
                case other:
                    print(f"Warning: Unknown field type: {other}")

    try:
        return await model_class.create(**model_kwargs)
    except IntegrityError as error:
        print(f"Error in {model_class.__name__}: model kwargs: {model_kwargs}")
        raise error
