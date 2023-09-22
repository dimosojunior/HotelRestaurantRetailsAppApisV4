
from django.urls import path
from . import views

# # MWANZO IN ORDER TO USE MODEL VIEW SET
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('PostMyUser', views.MyUserViewSet)



router.register('PostHotelInventory', views.HotelInventoryViewSet)
router.register('PostHotelFoodCategories', views.HotelFoodCategoriesViewSet)
router.register('PostHotelDrinksCategories', views.HotelDrinksCategoriesViewSet)
router.register('PostRoomsClasses', views.RoomsClassesViewSet)
router.register('PostHotelCustomers', views.HotelCustomersViewSet)




# HOTEL FOOD PRODUCT
router.register('PostHotelOtherFoodProducts', views.HotelOtherFoodProductsViewSet)
router.register('PostHotelPizzaProducts', views.HotelPizzaProductsViewSet)


# HOTEL DRINKS PRODUCT
router.register('PostHotelSoftDrinksProducts', views.HotelSoftDrinksProductsViewSet)
router.register('PostHotelBeersProducts', views.HotelBeersProductsViewSet)



#--------------UNORDERED HOTEL ROOMS-----------------
router.register('PostHotelRoomsClassA', views.HotelRoomsClassAViewSet)
router.register('PostHotelRoomsClassB', views.HotelRoomsClassBViewSet)
router.register('PostHotelRoomsClassC', views.HotelRoomsClassCViewSet)
router.register('PostHotelRoomsClassD', views.HotelRoomsClassDViewSet)
router.register('PostHotelRoomsClassE', views.HotelRoomsClassEViewSet)



#--------------BOOKED HOTEL ROOMS-----------------
router.register('PostHotelBookedRoomsClassA', views.HotelBookedRoomsClassAViewSet)
router.register('PostHotelBookedRoomsClassB', views.HotelBookedRoomsClassBViewSet)
router.register('PostHotelBookedRoomsClassC', views.HotelBookedRoomsClassCViewSet)
router.register('PostHotelBookedRoomsClassD', views.HotelBookedRoomsClassDViewSet)
router.register('PostHotelBookedRoomsClassE', views.HotelBookedRoomsClassEViewSet)











#-----------------------RESTAURANT----------------------


router.register('RestaurantInventory', views.RestaurantInventoryViewSet)
router.register('RestaurantFoodCategories', views.RestaurantFoodCategoriesViewSet)
router.register('RestaurantDrinksCategories', views.RestaurantDrinksCategoriesViewSet)

router.register('RestaurantCustomers', views.RestaurantCustomersViewSet)






# HOTEL FOOD PRODUCT
router.register('RestaurantOtherFoodProducts', views.RestaurantOtherFoodProductsViewSet)
router.register('RestaurantPizzaProducts', views.RestaurantPizzaProductsViewSet)


# Restaurant DRINKS PRODUCT
router.register('RestaurantSoftDrinksProducts', views.RestaurantSoftDrinksProductsViewSet)
router.register('RestaurantBeersProducts', views.RestaurantBeersProductsViewSet)












#-----------------------RETAILS-------------------------




router.register('RetailsInventory', views.RetailsInventoryViewSet)
router.register('RetailsFoodCategories', views.RetailsFoodCategoriesViewSet)
router.register('RetailsDrinksCategories', views.RetailsDrinksCategoriesViewSet)

router.register('RetailsCustomers', views.RetailsCustomersViewSet)












# HOTEL FOOD PRODUCT
router.register('RetailsOtherFoodProducts', views.RetailsOtherFoodProductsViewSet)
router.register('RetailsPizzaProducts', views.RetailsPizzaProductsViewSet)


# Retails DRINKS PRODUCT
router.register('RetailsSoftDrinksProducts', views.RetailsSoftDrinksProductsViewSet)
router.register('RetailsBeersProducts', views.RetailsBeersProductsViewSet)




urlpatterns = router.urls