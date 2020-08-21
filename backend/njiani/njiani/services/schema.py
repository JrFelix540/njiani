import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from .models import Service

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service


class ServiceNode(DjangoObjectType):
    class Meta:
        model = Service
        filter_fields = ['name']
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    service = graphene.relay.Node.Field(ServiceNode)
    all_services = DjangoFilterConnectionField(ServiceNode)

