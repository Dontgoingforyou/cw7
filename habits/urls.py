from django.urls import path, include
from rest_framework.routers import DefaultRouter
from habits.apps import HabitsConfig
from habits.views import HabitViewSet

router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

app_name = HabitsConfig.name

urlpatterns = [
    path('', include(router.urls)),
]