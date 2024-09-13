from collections.abc import Callable as _Callable
from typing import Any as _Any

from django.db.models.query import QuerySet as _QuerySet
from rest_framework import fields as _fields
from rest_framework import relations as _relations
from rest_framework.serializers import Serializer as _SerializerClass

from b2_utils.decorators import deprecated as _deprecated
from b2_utils.serializers.mixins import (
    RelatedFieldWithSerializer as _RelatedFieldWithSerializer,
)

__all__ = [
    "PrimaryKeyRelatedFieldWithSerializer",
    "SlugRelatedFieldWithSerializer",
    "DynamicPrimaryKeyRelatedFieldWithSerializer",
    "DynamicFieldsSerializer",
    "DBFriendlyRelatedFieldWithSerializer",
]


@_deprecated(
    "Use b2_utils.serializers.relations.DBFriendlyRelatedFieldWithSerializer instead",
)
class PrimaryKeyRelatedFieldWithSerializer(
    _RelatedFieldWithSerializer,
    _relations.PrimaryKeyRelatedField,
):
    def to_representation(self, value):
        if callable(value):
            return self.representation_serializer(
                value.all(),
                context=self.context,
                many=True,
            ).data

        instance = self.queryset.get(pk=value.pk)

        return self.representation_serializer(instance, context=self.context).data


class SlugRelatedFieldWithSerializer(
    _RelatedFieldWithSerializer,
    _relations.SlugRelatedField,
):
    def to_representation(self, value):
        if callable(value):
            return self.representation_serializer(
                value.all(),
                context=self.context,
                many=True,
            ).data

        instance = self.queryset.get(
            **{self.slug_field: getattr(value, self.slug_field)},
        )

        return self.representation_serializer(instance, context=self.context).data


@_deprecated(
    "Use b2_utils.serializers.relations.DBFriendlyRelatedFieldWithSerializer instead",
)
class DynamicPrimaryKeyRelatedFieldWithSerializer(PrimaryKeyRelatedFieldWithSerializer):
    """
    Work like PrimaryKeyRelatedFieldWithSerializer but allow to specify fields to be serialized
    and the representation_serializer must be have DynamicFieldsSerializer as parent
    """

    def __init__(self, fields=None, **kwargs):
        self.representation_fields = fields

        super().__init__(**kwargs)

    def to_representation(self, value):
        kwargs = {}
        if callable(value):
            kwargs = {
                "instance": value.all(),
                "many": True,
            }
        else:
            kwargs["instance"] = self.queryset.get(pk=value.pk)

        if self.representation_fields:
            kwargs["fields"] = self.representation_fields

        return self.representation_serializer(context=self.context, **kwargs).data


@_deprecated("Will be moved to b2_utils.serializers.mixins")
class DynamicFieldsSerializer:
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class DBFriendlyRelatedFieldWithSerializer(_relations.PrimaryKeyRelatedField):
    """A PrimaryKeyRelatedField that uses a serializer to represent the related object.
    This serializer does not cause N+1 queries when using select_related or prefetch_related.

    Args:
        serializer_class (type[SerializerClass]): The serializer class to use for the related object.
        fields (list[str], optional): The fields to include in the representation. Defaults to None.
        queryset (Union[QuerySet, Callable[[dict[str, Any]], QuerySet]], optional): The queryset to use for the related object. Defaults to None. If a callable is provided, it will be called with the context as an argument.
        write_protected (bool, optional): Whether the field is write protected. Defaults to False.
    """

    def __init__(
        self,
        serializer_class: type[_SerializerClass],
        fields: list[str] | None = None,
        queryset: _Callable[[dict[str, _Any]], _QuerySet] | _QuerySet | None = None,
        write_protected: bool = False,
        **kwargs,
    ):
        self.serializer_class = serializer_class
        self.write_protected = write_protected
        self.representation_fields = fields

        kwargs["queryset"] = queryset

        super().__init__(**kwargs)

    def get_queryset(self):
        if callable(get_queryset := self.queryset):
            return get_queryset(self.context)

        return super().get_queryset()

    def validate_empty_values(self, data):
        if self.write_protected:
            raise _fields.SkipField

        return super().validate_empty_values(data)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        kwargs = {"context": self.context}
        if self.representation_fields:
            kwargs["fields"] = self.representation_fields

        serializer = self.serializer_class(**kwargs)
        return serializer.to_representation(value)
