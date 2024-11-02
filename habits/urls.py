from django.urls import path
from rest_framework.routers import SimpleRouter
from habits.apps import HabitsConfig
from habits.views import HabitViewSet

# проводим стандартные настройки. Указываем приложение, импортируем из habits.apps.HabitsConfig
app_name = HabitsConfig.name

# присваиваем экземпляр класса
router = SimpleRouter()

# прописывем путь, по которому будет в пустом пути '', показываться ViewSet
router.register('', HabitViewSet)

urlpatterns = [
    path('public/', HabitViewSet.as_view({'get': 'list_public'}), name='public-habits'),
]
# к urlpatterns добавляем наши urls
urlpatterns += router.urls
