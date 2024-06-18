from django.urls import path,include
from . import views
from rest_framework_nested import routers


router=routers.DefaultRouter()

# -----------here is the parent routers--------------------
# we user basename 
router.register('products',viewset=views.Productviewset,basename='products')
router.register('customers',viewset=views.CustomerViewSet,basename='customers')
router.register('orders',viewset=views.OrdersViewset,basename='orders')

router.register('carts',viewset=views.Cartviewset,basename='carts')
# -------------
# look up so we will have parametter  called product_pk in our route
# base name using as prefix for generating url patterns product-list or product details
cartitems=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cartitems.register('items',viewset=views.Itemsviewset,basename='iteffms')
# ------------------------,vi--
reviewrouter=routers.NestedDefaultRouter(router,'products',lookup='review')
reviewrouter.register('reviews',viewset=views.Reviewviewset,basename="ali-salhab")

urlpatterns=router.urls+reviewrouter.urls+cartitems.urls
# URLConf
# urlpatterns = [
#     path("",include(router.urls)),
#         path("",include(reviewrouter.urls))
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:id>', views.ProductDetails.as_view()),
#     #   path('collections/', views.CollectionList.as_view()),
#     #     path('collections/<int:pk>', views.collection_details,name="collection-details"),

  
# ]