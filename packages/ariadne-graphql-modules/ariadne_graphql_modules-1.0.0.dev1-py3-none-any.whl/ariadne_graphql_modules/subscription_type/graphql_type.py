from typing import Any, Optional, cast

from ariadne.types import Resolver, Subscriber
from graphql import (
    FieldDefinitionNode,
    InputValueDefinitionNode,
    NameNode,
    ObjectTypeDefinitionNode,
    StringValueNode,
)

from ariadne_graphql_modules.base import GraphQLMetadata
from ariadne_graphql_modules.base_graphql_model import GraphQLModel
from ariadne_graphql_modules.base_object_type import (
    GraphQLBaseObject,
    GraphQLFieldData,
    GraphQLObjectData,
    validate_object_type_with_schema,
    validate_object_type_without_schema,
)
from ariadne_graphql_modules.base_object_type.graphql_field import (
    GraphQLObjectField,
    object_field,
    object_resolver,
)
from ariadne_graphql_modules.convert_name import convert_python_name_to_graphql
from ariadne_graphql_modules.description import get_description_node
from ariadne_graphql_modules.object_type import (
    GraphQLObjectFieldArg,
    GraphQLObjectResolver,
    GraphQLObjectSource,
    get_field_args_from_subscriber,
    get_field_args_out_names,
    get_field_node_from_obj_field,
    object_subscriber,
    update_field_args_options,
)
from ariadne_graphql_modules.subscription_type.models import GraphQLSubscriptionModel
from ariadne_graphql_modules.types import GraphQLClassType
from ariadne_graphql_modules.utils import parse_definition
from ariadne_graphql_modules.value import get_value_node


class GraphQLSubscription(GraphQLBaseObject):
    __graphql_type__ = GraphQLClassType.SUBSCRIPTION
    __abstract__: bool = True
    __description__: Optional[str] = None
    __graphql_name__ = GraphQLClassType.SUBSCRIPTION.value

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.__dict__.get("__abstract__"):
            return

        cls.__abstract__ = False

        if cls.__dict__.get("__schema__"):
            cls.__kwargs__ = validate_object_type_with_schema(
                cls, ObjectTypeDefinitionNode
            )
        else:
            cls.__kwargs__ = validate_object_type_without_schema(cls)

    @classmethod
    def __get_graphql_model_with_schema__(cls) -> "GraphQLModel":  # noqa: C901
        definition = cast(
            ObjectTypeDefinitionNode,
            parse_definition(ObjectTypeDefinitionNode, cls.__schema__),
        )

        descriptions: dict[str, StringValueNode] = {}
        args_descriptions: dict[str, dict[str, StringValueNode]] = {}
        args_defaults: dict[str, dict[str, Any]] = {}
        resolvers: dict[str, Resolver] = {}
        subscribers: dict[str, Subscriber] = {}

        for attr_name in dir(cls):
            cls_attr = getattr(cls, attr_name)
            if isinstance(cls_attr, GraphQLObjectResolver):
                resolver = cls_attr.resolver
                if isinstance(resolver, staticmethod):
                    resolver = resolver.__func__  # type: ignore[attr-defined]
                resolvers[cls_attr.field] = cls_attr.resolver
            if isinstance(cls_attr, GraphQLObjectSource):
                subscriber = cls_attr.subscriber
                if isinstance(subscriber, staticmethod):
                    subscriber = subscriber.__func__  # type: ignore[attr-defined]
                subscribers[cls_attr.field] = subscriber
                description_node = get_description_node(cls_attr.description)
                if description_node:
                    descriptions[cls_attr.field] = description_node

                field_args = get_field_args_from_subscriber(cls_attr.subscriber)
                if field_args:
                    args_descriptions[cls_attr.field] = {}
                    args_defaults[cls_attr.field] = {}

                    final_args = update_field_args_options(field_args, cls_attr.args)

                    for arg_name, arg_options in final_args.items():
                        arg_description = get_description_node(arg_options.description)
                        if arg_description:
                            args_descriptions[cls_attr.field][
                                arg_name
                            ] = arg_description

                        arg_default = arg_options.default_value
                        if arg_default is not None:
                            args_defaults[cls_attr.field][arg_name] = get_value_node(
                                arg_default
                            )

        fields: list[FieldDefinitionNode] = []
        for field in definition.fields:
            field_args_descriptions = args_descriptions.get(field.name.value, {})
            field_args_defaults = args_defaults.get(field.name.value, {})

            args: list[InputValueDefinitionNode] = []
            for arg in field.arguments:
                arg_name = arg.name.value
                args.append(
                    InputValueDefinitionNode(
                        description=(
                            arg.description or field_args_descriptions.get(arg_name)
                        ),
                        name=arg.name,
                        directives=arg.directives,
                        type=arg.type,
                        default_value=(
                            arg.default_value or field_args_defaults.get(arg_name)
                        ),
                    )
                )

            fields.append(
                FieldDefinitionNode(
                    name=field.name,
                    description=(
                        field.description or descriptions.get(field.name.value)
                    ),
                    directives=field.directives,
                    arguments=tuple(args),
                    type=field.type,
                )
            )

        return GraphQLSubscriptionModel(
            name=definition.name.value,
            ast_type=ObjectTypeDefinitionNode,
            ast=ObjectTypeDefinitionNode(
                name=NameNode(value=definition.name.value),
                fields=tuple(fields),
            ),
            resolvers=resolvers,
            subscribers=subscribers,
            aliases=getattr(cls, "__aliases__", {}),
            out_names={},
        )

    @classmethod
    def __get_graphql_model_without_schema__(
        cls, metadata: GraphQLMetadata, name: str
    ) -> "GraphQLModel":
        type_data = cls.get_graphql_object_data(metadata)
        type_aliases = getattr(cls, "__aliases__", None) or {}

        fields_ast: list[FieldDefinitionNode] = []
        resolvers: dict[str, Resolver] = {}
        subscribers: dict[str, Subscriber] = {}
        aliases: dict[str, str] = {}
        out_names: dict[str, dict[str, str]] = {}

        for attr_name, field in type_data.fields.items():
            fields_ast.append(get_field_node_from_obj_field(cls, metadata, field))
            if attr_name in type_aliases and field.name:
                aliases[field.name] = type_aliases[attr_name]
            elif field.name and attr_name != field.name and not field.resolver:
                aliases[field.name] = attr_name

            if field.resolver and field.name:
                resolvers[field.name] = field.resolver

            if field.subscriber and field.name:
                subscribers[field.name] = field.subscriber

            if field.args and field.name:
                out_names[field.name] = get_field_args_out_names(field.args)

        return GraphQLSubscriptionModel(
            name=name,
            ast_type=ObjectTypeDefinitionNode,
            ast=ObjectTypeDefinitionNode(
                name=NameNode(value=name),
                description=get_description_node(
                    getattr(cls, "__description__", None),
                ),
                fields=tuple(fields_ast),
            ),
            resolvers=resolvers,
            aliases=aliases,
            out_names=out_names,
            subscribers=subscribers,
        )

    @staticmethod
    def source(
        field: str,
        graphql_type: Optional[Any] = None,
        args: Optional[dict[str, GraphQLObjectFieldArg]] = None,
        description: Optional[str] = None,
    ):
        """Shortcut for object_resolver()"""
        return object_subscriber(
            args=args,
            field=field,
            graphql_type=graphql_type,
            description=description,
        )

    @staticmethod
    def resolver(field: str, *args, **_):
        """Shortcut for object_resolver()"""
        return object_resolver(
            field=field,
        )

    @staticmethod
    def field(
        f: Optional[Resolver] = None,
        *,
        name: Optional[str] = None,
        **_,
    ) -> Any:
        """Shortcut for object_field()"""
        return object_field(
            f,
            name=name,
        )

    @staticmethod
    def _process_class_attributes(  # noqa: C901
        target_cls, fields_data: GraphQLFieldData
    ):
        for attr_name in dir(target_cls):
            if attr_name.startswith("__"):
                continue
            cls_attr = getattr(target_cls, attr_name)
            if isinstance(cls_attr, GraphQLObjectField):
                if attr_name not in fields_data.fields_order:
                    fields_data.fields_order.append(attr_name)

                fields_data.fields_names[attr_name] = (
                    cls_attr.name or convert_python_name_to_graphql(attr_name)
                )
                if cls_attr.resolver:
                    resolver = cls_attr.resolver
                    if isinstance(resolver, staticmethod):
                        resolver = resolver.__func__  # type: ignore[attr-defined]
                    fields_data.fields_resolvers[attr_name] = resolver
            elif isinstance(cls_attr, GraphQLObjectResolver):
                resolver = cls_attr.resolver
                if isinstance(resolver, staticmethod):
                    resolver = resolver.__func__  # type: ignore[attr-defined]
                fields_data.fields_resolvers[cls_attr.field] = resolver
            elif isinstance(cls_attr, GraphQLObjectSource):
                if (
                    cls_attr.field_type
                    and cls_attr.field not in fields_data.fields_types
                ):
                    fields_data.fields_types[cls_attr.field] = cls_attr.field_type
                if (
                    cls_attr.description
                    and cls_attr.field not in fields_data.fields_descriptions
                ):
                    fields_data.fields_descriptions[cls_attr.field] = (
                        cls_attr.description
                    )
                subscriber = cls_attr.subscriber
                if isinstance(subscriber, staticmethod):
                    subscriber = subscriber.__func__  # type: ignore[attr-defined]
                fields_data.fields_subscribers[cls_attr.field] = subscriber
                field_args = get_field_args_from_subscriber(subscriber)
                if field_args:
                    fields_data.fields_args[cls_attr.field] = update_field_args_options(
                        field_args, cls_attr.args
                    )

            elif attr_name not in fields_data.aliases_targets and not callable(
                cls_attr
            ):
                fields_data.fields_defaults[attr_name] = cls_attr

    @classmethod
    def create_graphql_object_data_without_schema(cls) -> GraphQLObjectData:
        fields_data = GraphQLFieldData()
        cls._process_type_hints_and_aliases(fields_data)
        cls._process_class_attributes(cls, fields_data)

        return GraphQLObjectData(
            fields=cls._build_fields(fields_data=fields_data),
            interfaces=[],
        )

    @classmethod
    def _collect_inherited_objects(cls):
        return []
