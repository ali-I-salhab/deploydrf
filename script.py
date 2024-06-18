from django.contrib.contenttypes.models import ContentType

from store.models import Customer, Product
# the class Contenttype has method called model_class() 
# not found in other Calsses such like Product or cusomers or any other class 
# what dose this metod(model_class()) work ??
# ----> here the answer 
# retrun the model class represented by this instance method 

def run():
    print("A")
    # =======VERY IMPORTANT CONTENT --A
    # content_type=ContentType.objects.get(app_label="Store",model="Product")
    # print(content_type.model)
    # products =content_type.model_class()
    # print(products.objects.all())
    # product=content_type.get_object_for_this_type(id='1')
    # print(product)
    # p= ContentType.objects.get_for_model(Product)
    # print(p.id)

    

    # a=content_type.get_for_model(first_name='ali')
    # print(content_type.get_object_for_this_type(id="1").description)

run()    