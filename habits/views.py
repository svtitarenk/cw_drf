from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.response import Response

from habits.models import Habit
from habits.permissions import IsOwnerOrPublicReadOnly
from habits.serializers import HabitSerializer
from rest_framework.permissions import IsAuthenticated
from habits import paginators


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrPublicReadOnly]
    pagination_class = paginators.CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ('frequency', 'action',)

    # search_fields = ('action',)
    # ordering_fields = ('frequency',)

    def list_public(self, request):
        public_habits = Habit.objects.filter(is_public=True)
        serializer = self.get_serializer(public_habits, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """ Возвращаем привычки, доступные только пользователю или публичные """

        user = self.request.user
        return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Автоматическое назначение создателя
