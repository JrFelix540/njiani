import graphene

import njiani.users.schema as userSchema
import njiani.services.schema as serviceSchema

class Query(userSchema.Query,
    serviceSchema.Query,
    graphene.ObjectType):
    pass

class Mutation(userSchema.Mutation,
    graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)