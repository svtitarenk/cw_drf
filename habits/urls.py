from django.urls import path
from rest_framework.routers import SimpleRouter
from habits.apps import HabitsConfig
from habits.views import HabitViewSet

# проводим стандартные настройки. Указываем приложение, импортируем из dogs.apps.DogsConfig
app_name = HabitsConfig.name

# присваиваем экземпляр класса
router = SimpleRouter()
# прописывем путь, по которому будет в пустом пути '', показываться DogsViewSet
router.register('', HabitViewSet)


urlpatterns = [
    path('public/', HabitViewSet.as_view({'get': 'list_public'}), name='public-habits'),
    # path('api-auth/', include('rest_framework.urls')),  # для авторизации через API
]
# к urlpatterns добавляем наши urls
urlpatterns += router.urls