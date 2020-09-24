import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Cuisine,Wineproducer,Stockist,Agent,Product



class CuisineType(DjangoObjectType):
    class Meta:
        model=Cuisine

class ProductType(DjangoObjectType):
    class Meta:
        model=Product        
        fields=('id','name','color','palate','nose','price')




class CuisineInput(graphene.InputObjectType):
    id = graphene.ID()
    name =graphene.String()  

class ProductInput(graphene.InputObjectType):
    id=graphene.ID()
    name= graphene.String()
    description =graphene.String()
    price =graphene.Float()
    created = graphene.DateTime()






class CreateCuisine(graphene.Mutation):
    class Arguments:
        input =CuisineInput(required = True)
    ok =graphene.Boolean()
    cuisine =graphene.Field(CuisineType)

    @staticmethod
    def mutate(root,info,input =None):
        ok =True
        cuisine_instance=Cuisine(name =input.name)
        cuisine_instance.save()
        return CreateCuisine(ok =ok,cuisine = cuisine_instance) 

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





class UpdateCuisine(graphene.Mutation):
    class Arguments:
        id =graphene.Int(required = True)
        input =CuisineInput(required = True)

    ok = graphene.Boolean()
    cuisine =graphene.Field(CuisineType)

    @staticmethod
    def mutate(root,info,id,input=None):
        ok =False
        cuisine_instance =Cuisine.objects.get(pk =id)
        if cuisine_instance:
            ok =True
            cuisine_instance.name=input.name
            cuisine_instance.save()
            return UpdateCuisine(ok=ok,cuisine =cuisine_instance)

        return UpdateCuisine(ok =ok,cuisine=None)  

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
    cuisine =graphene.Field(CuisineType, id=graphene.Int())
    cuisine = graphene.List(CuisineType)
    product=graphene.List(ProductType)
    


    def resolve_product(root,info,**kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Product.objects.get(pk=id)

        return None

        
    def resolve_product(self,info,**kwargs):
        return Product.objects.all()        



    


    def resolve_cuisine(root,info,**kwargs):
        id =kwargs.get('id')

        if id is not None:
            return Cuisine.objects.get(pk =id)

        return None


    def resolve_cuisine(self,info,**kwargs):
        return Cuisine.objects.all()  


class Mutation(graphene.ObjectType):
    create_cuisine=CreateCuisine.Field()
    update_cuisine =UpdateCuisine.Field()    
    create_product= CreateProduct.Field()
    update_product= UpdateProduct.Field()