from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth.mutations import Register
import graphene
import graphql_jwt

from .models import Customer, Mechanic

#Types
class GroupType(DjangoObjectType):
    class Meta:
        model = Group

class PermissionType(DjangoObjectType):
    class Meta:
        model = Permission

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

# Nodes
class MechanicNode(DjangoObjectType):
    class Meta:
        model = Mechanic
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)



# Queries
class Query(UserQuery, MeQuery, graphene.ObjectType):
    mechanic = graphene.relay.Node.Field(MechanicNode)
    all_mechanics = DjangoFilterConnectionField(MechanicNode)

    customer = graphene.relay.Node.Field(CustomerNode)
    all_customers = graphene.relay.Node.Field(CustomerNode)

    group = graphene.Field(GroupType)
    all_groups = graphene.List(GroupType)

    permission = graphene.Field(PermissionType)
    all_permissions = graphene.List(PermissionType)

    def resolve_group(self, info,id, **kwargs):
        return Group.objects.get(pk=id)

    def resolve_all_groups(self, info, **kwargs):
        return Group.objects.all()

    def resolve_permission(self, info, id, **kwargs):
        return Permission.objects.get(pk=id)
    
    def resolve_all_permissions(self, info, **kwargs):
        return Permission.objects.all()

# Mutations
# class AuthMutation(graphene.ObjectType):
#     register = Register.Field()
class PermissionInput(graphene.InputObjectType):
    name = graphene.String()
    id = graphene.ID()

class UserInput(graphene.InputObjectType):
    email = graphene.String()

class GroupInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    permissions = graphene.List(PermissionInput)

class SetGroupInput(graphene.InputObjectType):
    user = UserInput()
    group = GroupInput()


class SetUserGroup(graphene.Mutation):
    class Arguments:
        input = SetGroupInput(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input):
        user = get_user_model().objects.get(email=input.user.email)
        if user is None:
            return SetUserGroup(ok=False)
        group = Group.objects.get(pk=input.group.id)
        if group is None:
            return SetUserGroup(ok=False)
        
        user.groups.add(group)
        return SetUserGroup(ok=True)


class CreateGroup(graphene.Mutation):
    class Arguments:
        input = GroupInput(required=True)
    
    ok = graphene.Boolean()
    group = graphene.Field(GroupType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        permissions = []

        for permission_input in input.permissions:
            permission = Permission.objects.get(pk=permission_input.id)
            if permission is None:
                return CreateGroup(ok=False, post=None)
            permissions.append(permission)

        
            

        group_instance = Group(
            name= input.name,
        )
        group_instance.save()
        group_instance.permissions.set(permissions)
        return(CreateGroup(ok=ok, group=group_instance))




class Mutation(graphene.ObjectType):
    create_group = CreateGroup.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    set_user_group = SetUserGroup.Field()