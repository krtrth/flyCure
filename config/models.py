from django.db import models
from django.db.models.base import ModelBase
from django.utils.text import camel_case_to_spaces


def model_db_table(app_label: str, model_name: str) -> str:
    return f"{app_label}_{camel_case_to_spaces(model_name).replace(' ', '_')}"


class SnakeCaseModelBase(ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        meta = attrs.get("Meta")
        is_abstract = bool(meta and getattr(meta, "abstract", False))
        if name != "SnakeCaseModel" and not is_abstract:
            if meta is None:
                meta = type("Meta", (), {})
                attrs["Meta"] = meta
            if not getattr(meta, "db_table", None):
                snake_name = camel_case_to_spaces(name).replace(" ", "_")
                if snake_name != name.lower():
                    app_label = getattr(meta, "app_label", None) or attrs["__module__"].split(".")[0]
                    meta.db_table = model_db_table(app_label, name)
        return super().__new__(cls, name, bases, attrs, **kwargs)


class SnakeCaseModel(models.Model, metaclass=SnakeCaseModelBase):
    class Meta:
        abstract = True
