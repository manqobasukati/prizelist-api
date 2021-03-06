from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from prize_list_app import views

router = DefaultRouter()
router.register(r'users',views.UserViewSet)
router.register(r'buyers',views.BuyerViewSet)
router.register(r'prize-list-item',views.PrizeListItemViewSet)



urlpatterns = [
    path('',include(router.urls)),
    path('shops/',views.ShopView.as_view()),
    path('shops/<int:pk>/branches',views.BranchView.as_view()),
    path('shops/<int:pk>/branches/<int:branch_id>',views.BranchDetailView.as_view()),
    path('shops/<int:shop_id>/branches/<int:branch_id>/prize-lists/', views.PrizeListView.as_view()),
    path('shops/<int:shop_id>/branches/<int:branch_id>/orders/', views.OrderView.as_view()),
    path('shops/<int:shop_id>/branches/<int:branch_id>/orders/<int:order_id>', views.OrderDetailView.as_view()),
    path('shops/<int:shop_id>/branches/<int:branch_id>/prize-lists/<int:prize_list_id>', views.PrizeListViewDetail.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]