from django.db.models import fields
import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Wineproducer,Stockist,Agent,Product



class ProductType(DjangoObjectType):
    class Meta:
        model=Product        
        fields=('id','name','color','palate','nose','price')

class WineproducerType(DjangoObjectType):
    class Meta:
        model = Wineproducer  
        fields =('__all__')      

class StockistType(DjangoObjectType):
    class Meta:
        model=Stockist
        fields=("__all__")        

class AgentType(DjangoObjectType):
    class Meta:
        model=Agent
        fields=("__all__")        




 

class ProductInput(graphene.InputObjectType):
    id=graphene.ID()
    name= graphene.String()
    description =graphene.String()
    price =graphene.Float()
    created = graphene.DateTime()








class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required =True)
    ok = graphene.Boolean()
    product =graphene.Field(ProductType)


    @staticmethod
    def mutate(root,info,input=None):
        ok =True
        product_instance=Product(name=input.name)
        product_instance.save()
        return CreateProduct(ok=ok, product=product_instance)            







class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required =True)
        input=ProductInput(required = True)

    ok = graphene.Boolean()
    product= graphene.Field(ProductType)

    @staticmethod
    def mutate(root,info,id,input=None):
        ok=False
        product_instance=Product.objects.get(pk=id)
        if product_instance:
            ok=True
            product_instance.name=input.name
            product_instance.save()
            return UpdateProduct(ok=ok,product=product_instance)
        return UpdateProduct(ok=ok,product=None)        




class Query(ObjectType):
    
    product =graphene.Field(ProductType, id=graphene.Int())
    product=graphene.List(ProductType)
    wineproducer = graphene.List(WineproducerType)
    stockist=graphene.List(StockistType)
    agent=graphene.List(AgentType)
    



    def resolve_stockist(self,info,**kwargs):
        return Stockist.objects.all()


    def resolve_agent(self,info,**kwargs):
        return Agent.objects.all()    

    def resolve_wineproducer(sel,info,**kwargs):
        return Wineproducer.objects.all()
    


    def resolve_product(root,info,**kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Product.objects.get(pk=id)

        return None

        
    def resolve_product(self,info,**kwargs):
        return Product.objects.all()        




class Mutation(graphene.ObjectType):    
    create_product= CreateProduct.Field()
    update_product= UpdateProduct.Field()