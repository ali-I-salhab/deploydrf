from rest_framework import serializers
from .models import Product,Collection,Review,Cart,CartItem,Customer,Order,OrderItem
class SimpleProductSerializer(serializers.ModelSerializer):
   class Meta:
      model=Product
      fields=['id','title']
class CustomerSerializer(serializers.ModelSerializer):
   class Meta:
      model=Customer
      fields='__all__'
class OrderItemsSerializer(serializers.ModelSerializer):
   product=SimpleProductSerializer()
   class Meta:
      model=OrderItem
      fields=['id','product','quantity','unit_price']      



class OrderSerializer(serializers.ModelSerializer):
   customer=CustomerSerializer(read_only=True)
   items=OrderItemsSerializer(many=True)

   
   class Meta:
      model=Order
      fields=['id','placed_at','payment_status','customer','items']


class ReviewSerializer(serializers.ModelSerializer):
    product=serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())
    class Meta:
        model=Review
        fields=['id','name','description','date','product']
    
    def create(self, validated_data):
        print("--------------------")
        print(self.context)
        product_id=self.context['product_id']
        c=Review.objects.create(product_id=product_id,**validated_data)
        return c
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','unit_price']    

class UpdateCartItemSerializer(serializers.ModelSerializer):
   class Meta:
      model=CartItem
      fields=['quantity']        
class AddCartItemSerializer(serializers.ModelSerializer):
  def validate_product(self,value):
      
      print("from validation methods _--------------------------_____")
      print(value)
      if not Product.objects.filter(pk=value).exists():
        raise serializers.ValidationError("Prduct Not Found Ya hummar")
      else:
        return value
      
      
          
  def save(self, **kwargs):
    print("------------------SAVE METhod-------------------------")

    quantity=self.validated_data['quantity']
    prosuct_id=self.validated_data['product'].id
    cart_id=self.context['cart_id']

    try :
        print("------------------ppid")
        print(prosuct_id)
        cartitem=CartItem.objects.get(cart_id=cart_id,product_id=prosuct_id)
        cartitem.quantity+=quantity
        cartitem.save()
        self.instance=cartitem

    except CartItem.DoesNotExist:
         self.instance=CartItem.objects.create(cart_id=cart_id,**self.validated_data)
    return self.instance

 
 
  class Meta:
    model=CartItem
    fields=['product','quantity']              
class CartItemSerializer(serializers.ModelSerializer):
  product=SimpleProductSerializer()
  total_price=serializers.SerializerMethodField()
  
  def get_total_price(self,cartitem:CartItem):
      return cartitem.quantity*cartitem.product.unit_price
  class Meta:
    model=CartItem
    fields=['id','cart','product','quantity','total_price']            
         
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model=Cart
        fields=['id','created_at','items','total_price']
    

class CollectionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title =serializers.CharField()
    count_products=serializers.IntegerField()
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id',"title",'description','collection','inventory']

    # id=serializers.IntegerField()
    # title=serializers.CharField(max_length=255)
    # description=serializers.CharField(max_length=255)
    # collection=serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(),view_name='collection-details')

class CustomerSerializer(serializers.ModelSerializer):
   user_id=serializers.IntegerField(read_only=True)
   class Meta:
        model=Customer
        fields=['id','user_id','phone','birth_date','membership']