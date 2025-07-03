from django.urls import path, include

from toy_store.api.routers import router

app_name = 'toy_store'

urlpatterns = [
    path('', include(router.urls)),
]
