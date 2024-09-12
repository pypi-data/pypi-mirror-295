from pydantic import BaseModel

__all__ = ("PydanticModel",)


def _set_pydantic_model():
    models = [BaseModel]

    try:
        from pydantic.v1 import BaseModel as BaseModelV1

        models.append(BaseModelV1)
    except ImportError:
        pass

    return frozenset(models)


PydanticModel = _set_pydantic_model()
