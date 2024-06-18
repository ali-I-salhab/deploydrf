from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny,DjangoModelPermissions
from rest_framework.views import APIView
from .models import Product,OrderItem,User
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .serilizer import ProductSerializer,CartSerializer, UpdateCartItemSerializer
from django.db.models import Count,Sum
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,ListModelMixin
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serilizer import CollectionSerializer,ReviewSerializer,CustomerSerializer,AddCartItemSerializer,CartItemSerializer
from .models import Collection,Review,Cart,CartItem,Customer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.conf import settings
from .permissions import IsAdminUserOrReadOnly
from .permissions import ViewCustomerHistoryPermissions
from .models import Order
from .serilizer import OrderSerializer
# -------------------function based views
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method=="GET":
#         products=Product.objects.select_related('collection').all()
#         serelizer=ProductSerializer(products,many=True)
#         return Response(serelizer.data)
#     if request.method=="POST":
      
#         serelizer=ProductSerializer(data=request.data)
#         serelizer.is_valid(raise_exception=True)
#         return Response(serelizer.data)
      
# class based view 
# class ProductList(APIView):
#     def get(self,request):
#          products=Product.objects.select_related('collection')
#          serelizer=ProductSerializer(products,many=True)
#          return Response(serelizer.data)
#     def post(self,request):
#         serelizer=ProductSerializer(data=request.data)
#         serelizer.is_valid(raise_exception=True)
#         return Response(serelizer.data)
# ----------------Getneric view
# ------here is ModelViewSet : in this method we combain two view 
class Reviewviewset(ModelViewSet):
    
    def get_queryset(self):
        # print("Review view set get query set --------=")
        # print(self.request.query_params['r'])
        
        
        return Review.objects.filter(product=self.kwargs['review_pk'])
   
    serializer_class=ReviewSerializer
  
    def get_serializer_context(self):
        print("------------------------------------context passed from Reviewviewse to Review serializer")

     
        return {"product_id":self.kwargs['review_pk']}
class Itemsviewset(ModelViewSet):
    http_method_names=['post','get','delete','patch']
    def get_serializer_context(self):
        print("cart_id_is-------------------->")
        print(self.request.user.email)
        # print(self.kwargs['cart_pk'])
        return {'cart_id':self.kwargs['cart_pk']}
        
    def get_serializer_class(self):
        print("---------------------------")
        print(self.request.method=='POST')
        print("---------------------------")
        if self.request.method=='POST':
            return AddCartItemSerializer
        if self.request.method=='PATCH':
            return UpdateCartItemSerializer
        
        
        return CartItemSerializer
    
    
    def get_queryset(self):
        print("------------------=")
        print(self.kwargs)
        queryset =CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])
        queryset = queryset 
        return queryset
    

        
    

class Cartviewset(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin,GenericViewSet):
    queryset=Cart.objects.prefetch_related('items__product').all()
    serializer_class=CartSerializer

    
class Productviewset(ModelViewSet):
    queryset=Product.objects.all()
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields=['collection_id']
    
    search_fields=['title','description']
    ordering_fields=['title',"id"]
    
    # def get_queryset(self):

    #     products=Product.objects.all()
    #     print(self.request.query_params)
    #     if self.request.query_params.get('collection_id') is not None:
    #         print("[[[[[[[[[[filter apllied]]]]]]]]]]")
    #         return products.filter(collection_id=self.request.query_params.get('collection_id',None))
     
    #     else :
    #         return products
     
        # return products
    serializer_class=ProductSerializer
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product=kwargs['pk']).count()>0:
            return Response("{'error':'cnat be deleted'}")
        print("------------------------------------------------")
        print(kwargs)
        return super().destroy(request, *args, **kwargs)
    # def delete(self,request,id):
    #     product=get_object_or_404(Product,pk=id)
    #     if product.order_item.count()>0 :
    #         return Response({"error": "Cant be deleted "})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):
#     queryset=Product.objects.select_related("collection")
#     serializer_class=ProductSerializer

    # if we have some logic we use rhis two methods 

    # def get_queryset(self):
    #     return Product.objects.select_related("collection")
    # def get_serializer(self, *args, **kwargs):
    #     return ProductSerializer

# class ProductDetails(RetrieveUpdateDestroyAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer   
#     lookup_field="id"   
    # def delete(self,request,id):
    #     product=get_object_or_404(Product,pk=id)
    #     if product.order_item.count()>0 :
    #         return Response({"error": "Cant be deleted "})
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
# class ProductDetails(APIView):

#     def delete(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     def get(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         serilizer=ProductSerializer(product)
#         return Response(serilizer.data)
#     def put(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         serilaizer=ProductSerializer(product,data=request.data)
#         serilaizer.is_valid(raise_exception=True)
#         serilaizer.save()
#         return Response(serilaizer.data)

# @api_view(['GET',"PUT","PATCH","DELETE"])
# def product_details(request,id):
#     product=get_object_or_404(Product,pk=id)
#     if request.method=="DELETE":
  
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     if request.method=="GET":
            
       
#         serelizer=ProductSerializer(product)
#         return Response(serelizer.data)
#     if request.method=="PUT":
            
#         serelizer=ProductSerializer(product,data=request.data,)
#         serelizer.is_valid(raise_exception=True) 
#         serelizer.save()
#         return Response(serelizer.data)   
#     if request.method=="PATCH":
            
#         serelizer=ProductSerializer(product,data=request.data,)
#         serelizer.is_valid(raise_exception=True) 
#         serelizer.save()
#         return Response(serelizer.data)  
    
#     return Response(serelizer.validated_data)


class CollectionList(ListCreateAPIView):
    queryset=Collection.objects.annotate(count_products=Count('products__id')).all()
    serializer_class=CollectionSerializer
    @api_view()
    def collection_details(request,pk):
        return Response("ok")



class CustomerViewSet(RetrieveModelMixin,ListModelMixin,CreateModelMixin,GenericViewSet):
    permission_classes=[DjangoModelPermissions]
    serializer_class=CustomerSerializer
    # queryset=Customer.objects.all()
    # def get_permissions(self):
    #     if self.request.method=='GET':
    #         return [AllowAny(),] 
    #     return[]   
    def get_queryset(self):
         print("----------------------------------")
         print(self.request.user)
         
         return Customer.objects.all()
    @action(methods=['get'],detail=True,permission_classes=[ViewCustomerHistoryPermissions])
    def history(self,request,pk):
        return Response('history')
    @action(methods=['get','PUT'],detail=False)
    def mee(self,request):
        
        (customer,created)=Customer.objects.get_or_create(user_id=request.user.id)
        if request.method=='GET':
            
            print("-----------------------------------------")
            print(request.user)
          
            print(created)
            
            serilaizer=CustomerSerializer(customer)
            return Response(serilaizer.data)
        elif request.method=='PUT':
            serilaizer=CustomerSerializer(customer,request.data)
            serilaizer.is_valid(raise_exception=True)
            serilaizer.save()
            return Response(serilaizer.data,status=status.HTTP_200_OK)    

     

class OrdersViewset(ModelViewSet):

    serializer_class=OrderSerializer   
    permission_classes=[IsAuthenticated]    
    def get_queryset(self):
        print(self.request.user)
        if self.request.user.is_staff:
            return Order.objects.all() 
        else :
            # print(self.request.user.id)
            customer_id=Customer.objects.only('user_id').get(user=self.request.user.id)
            print(f'${customer_id }+ userid')
          
            return Order.objects.filter(customer=customer_id)
