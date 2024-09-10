from dataclasses import dataclass
from typing import cast

from ariadne import ObjectType as ObjectTypeBindable
from ariadne.types import Resolver
from graphql import GraphQLField, GraphQLObjectType, GraphQLSchema

from ariadne_graphql_modules.base_graphql_model import GraphQLModel


@dataclass(frozen=True)
class GraphQLObjectModel(GraphQLModel):
    resolvers: dict[str, Resolver]
    aliases: dict[str, str]
    out_names: dict[str, dict[str, str]]

    def bind_to_schema(self, schema: GraphQLSchema):
        bindable = ObjectTypeBindable(self.name)

        for field, resolver in self.resolvers.items():
            bindable.set_field(field, resolver)
        for alias, target in self.aliases.items():
            bindable.set_alias(alias, target)

        bindable.bind_to_schema(schema)

        graphql_type = cast(GraphQLObjectType, schema.get_type(self.name))
        for field_name, field_out_names in self.out_names.items():
            graphql_field = cast(GraphQLField, graphql_type.fields[field_name])
            for arg_name, out_name in field_out_names.items():
                graphql_field.args[arg_name].out_name = out_name
