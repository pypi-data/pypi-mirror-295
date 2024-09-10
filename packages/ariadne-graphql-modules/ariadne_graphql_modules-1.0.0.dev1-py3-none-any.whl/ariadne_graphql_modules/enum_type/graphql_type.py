from enum import Enum
from inspect import isclass
from typing import Any, Optional, Union, cast

from graphql import EnumTypeDefinitionNode, EnumValueDefinitionNode, NameNode

from ariadne_graphql_modules.base import GraphQLMetadata, GraphQLModel, GraphQLType
from ariadne_graphql_modules.description import get_description_node
from ariadne_graphql_modules.enum_type.models import GraphQLEnumModel
from ariadne_graphql_modules.utils import parse_definition
from ariadne_graphql_modules.validators import validate_description, validate_name


class GraphQLEnum(GraphQLType):
    __abstract__: bool = True
    __schema__: Optional[str]
    __description__: Optional[str]
    __members__: Optional[Union[type[Enum], dict[str, Any], list[str]]]
    __members_descriptions__: Optional[dict[str, str]]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        if cls.__dict__.get("__abstract__"):
            return

        cls.__abstract__ = False
        cls._validate()

    @classmethod
    def __get_graphql_model__(cls, metadata: GraphQLMetadata) -> "GraphQLModel":
        name = cls.__get_graphql_name__()

        if getattr(cls, "__schema__", None):
            return cls.__get_graphql_model_with_schema__(name)

        return cls.__get_graphql_model_without_schema__(name)

    @classmethod
    def __get_graphql_model_with_schema__(cls, name: str) -> "GraphQLEnumModel":
        definition: EnumTypeDefinitionNode = cast(
            EnumTypeDefinitionNode,
            parse_definition(EnumTypeDefinitionNode, cls.__schema__),
        )

        members = getattr(cls, "__members__", [])
        members_values: dict[str, Any] = {}

        if isinstance(members, dict):
            members_values = dict(members.items())
        elif isclass(members) and issubclass(members, Enum):
            members_values = {member.name: member for member in members}
        else:
            members_values = {
                value.name.value: value.name.value
                for value in definition.values  # pylint: disable=no-member
            }

        members_descriptions = getattr(cls, "__members_descriptions__", {})

        return GraphQLEnumModel(
            name=name,
            members=members_values,
            ast_type=EnumTypeDefinitionNode,
            ast=EnumTypeDefinitionNode(
                name=NameNode(value=name),
                directives=definition.directives,
                description=definition.description
                or (get_description_node(getattr(cls, "__description__", None))),
                values=tuple(
                    EnumValueDefinitionNode(
                        name=value.name,
                        directives=value.directives,
                        description=value.description
                        or (
                            get_description_node(
                                members_descriptions.get(value.name.value),
                            )
                        ),
                    )
                    for value in definition.values  # pylint: disable=no-member
                ),
            ),
        )

    @classmethod
    def __get_graphql_model_without_schema__(cls, name: str) -> "GraphQLEnumModel":
        members = getattr(cls, "__members__", [])
        members_values = {}
        if isinstance(members, dict):
            members_values = dict(members.items())
        elif isclass(members) and issubclass(members, Enum):
            members_values = {i.name: i for i in members}
        elif isinstance(members, list):
            members_values = {kv: kv for kv in members}

        members_descriptions = getattr(cls, "__members_descriptions__", {})

        return GraphQLEnumModel(
            name=name,
            members=members_values,
            ast_type=EnumTypeDefinitionNode,
            ast=EnumTypeDefinitionNode(
                name=NameNode(value=name),
                description=get_description_node(
                    getattr(cls, "__description__", None),
                ),
                values=tuple(
                    EnumValueDefinitionNode(
                        name=NameNode(value=value_name),
                        description=get_description_node(
                            members_descriptions.get(value_name)
                        ),
                    )
                    for value_name in members_values
                ),
            ),
        )

    @classmethod
    def _validate(cls):
        if getattr(cls, "__schema__", None):
            cls._validate_enum_type_with_schema()
        else:
            cls._validate_enum_type()

    @classmethod
    def _validate_enum_type_with_schema(cls):
        definition = parse_definition(EnumTypeDefinitionNode, cls.__schema__)

        if not isinstance(definition, EnumTypeDefinitionNode):
            raise ValueError(
                f"Class '{cls.__name__}' defines '__schema__' attribute "
                f"with declaration for an invalid GraphQL type. "
                f"('{definition.__class__.__name__}' != "
                f"'{EnumTypeDefinitionNode.__name__}')"
            )

        validate_name(cls, definition)
        validate_description(cls, definition)

        members_names = {
            value.name.value for value in definition.values  # pylint: disable=no-member
        }
        if not members_names:
            raise ValueError(
                f"Class '{cls.__name__}' defines '__schema__' attribute "
                "that doesn't declare any enum members."
            )

        members_values = getattr(cls, "__members__", None)
        if members_values:
            cls.validate_members_values(members_values, members_names)

        members_descriptions = getattr(cls, "__members_descriptions__", {})
        cls.validate_enum_members_descriptions(members_names, members_descriptions)

        duplicate_descriptions = [
            ast_member.name.value
            for ast_member in definition.values  # pylint: disable=no-member
            if ast_member.description
            and ast_member.description.value
            and members_descriptions.get(ast_member.name.value)
        ]

        if duplicate_descriptions:
            raise ValueError(
                f"Class '{cls.__name__}' '__members_descriptions__' attribute defines "
                "descriptions for enum members that also "
                "have description in '__schema__' "
                f"attribute. (members: '{', '.join(duplicate_descriptions)}')"
            )

    @classmethod
    def validate_members_values(cls, members_values, members_names):
        if isinstance(members_values, list):
            raise ValueError(
                f"Class '{cls.__name__}' '__members__' attribute "
                "can't be a list when used together with '__schema__'."
            )

        missing_members = None
        if isinstance(members_values, dict):
            missing_members = members_names - set(members_values)
        elif isclass(members_values) and issubclass(members_values, Enum):
            missing_members = members_names - {value.name for value in members_values}

        if missing_members:
            raise ValueError(
                f"Class '{cls.__name__}' '__members__' is missing values "
                f"for enum members defined in '__schema__'. "
                f"(missing items: '{', '.join(missing_members)}')"
            )

    @classmethod
    def _validate_enum_type(cls):
        members_values = getattr(cls, "__members__", None)
        if not members_values:
            raise ValueError(
                f"Class '{cls.__name__}' '__members__' attribute is either missing or "
                "empty. Either define it or provide full SDL for this enum using "
                "the '__schema__' attribute."
            )

        if not any(
            [
                isinstance(members_values, (dict, list)),
                isclass(members_values) and issubclass(members_values, Enum),
            ]
        ):
            raise ValueError(
                f"Class '{cls.__name__}' '__members__' "
                "attribute is of unsupported type. "
                f"Expected 'Dict[str, Any]', 'Type[Enum]' or List[str]. "
                f"(found: '{type(members_values)}')"
            )

        members_names = cls.get_members_set(members_values)
        members_descriptions = getattr(cls, "__members_descriptions__", {})
        cls.validate_enum_members_descriptions(members_names, members_descriptions)

    @classmethod
    def validate_enum_members_descriptions(
        cls, members: set[str], members_descriptions: dict
    ):
        invalid_descriptions = set(members_descriptions) - members
        if invalid_descriptions:
            invalid_descriptions_str = "', '".join(invalid_descriptions)
            raise ValueError(
                f"Class '{cls.__name__}' '__members_descriptions__' attribute defines "
                f"descriptions for undefined enum members. "
                f"(undefined members: '{invalid_descriptions_str}')"
            )

    @staticmethod
    def get_members_set(
        members: Optional[Union[type[Enum], dict[str, Any], list[str]]],
    ) -> set[str]:
        if isinstance(members, dict):
            return set(members.keys())

        if isclass(members) and issubclass(members, Enum):
            return set(member.name for member in members)

        if isinstance(members, list):
            return set(members)

        raise TypeError(
            f"Expected members to be of type Dict[str, Any], List[str], or Enum."
            f"Got {type(members).__name__} instead."
        )
