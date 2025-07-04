from django.urls import path
from users.views import MyTokenObtainPairView


urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
