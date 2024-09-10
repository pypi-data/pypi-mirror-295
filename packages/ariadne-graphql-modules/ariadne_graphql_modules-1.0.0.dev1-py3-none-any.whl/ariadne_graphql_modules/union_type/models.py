from dataclasses import dataclass

from ariadne import UnionType
from graphql import GraphQLSchema, GraphQLTypeResolver

from ariadne_graphql_modules.base_graphql_model import GraphQLModel


@dataclass(frozen=True)
class GraphQLUnionModel(GraphQLModel):
    resolve_type: GraphQLTypeResolver

    def bind_to_schema(self, schema: GraphQLSchema):
        bindable = UnionType(self.name, self.resolve_type)
        bindable.bind_to_schema(schema)
