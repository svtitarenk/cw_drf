from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User
from datetime import timedelta


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@user.ru', password='12345')
        self.habit = Habit.objects.create(
            user=self.user,
            place='По парку',
            time='12:00',
            action='Пробежка',
            frequency=1,
            estimated_time=timedelta(minutes=10)
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.user, self.user)
        self.assertEqual(self.habit.place, 'По парку')
        self.assertEqual(self.habit.action, 'Пробежка')


class HabitSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@user.ru', password='12345')
        self.habit_data = {
            'place': 'По парку',
            'time': '12:00',
            'action': 'Пробежка',
            'frequency': 1,
            'estimated_time': '1:59',
            'user': self.user
        }
        self.client.force_authenticate(user=self.user)

    def test_serializer_with_valid_data(self):
        """ Проверка обработки данных через сериализатор """
        serializer = HabitSerializer(data=self.habit_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['place'], 'По парку')

    def test_create_habit_with_valid_frequency(self):
        """ Проверка валидатора на периодичность (1-7)"""
        response = self.client.post('/habits/', self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['place'], 'По парку')
        self.assertEqual(response.data['frequency'], self.habit_data['frequency'])

    def test_create_habit_with_invalid_frequency_below_range(self):
        """ Проверка валидатора на периодичность (frequency < 1)"""
        invalid_data = self.habit_data.copy()
        # Frequency ниже допустимого
        invalid_data['frequency'] = 0
        response = self.client.post('/habits/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0],
                         "Привычка должна выполняться как минимум раз в неделю (частота от 1 до 7 дней).")

    def test_create_habit_with_invalid_frequency_above_range(self):
        """ Проверка валидатора на периодичность (frequency > 7)"""
        invalid_data = self.habit_data.copy()
        # Frequency больше допустимого
        invalid_data['frequency'] = 8
        response = self.client.post('/habits/', invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0],
                         "Привычка должна выполняться как минимум раз в неделю (частота от 1 до 7 дней).")


class HabitViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@user.ru', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        response = self.client.post(
            '/habits/',
            {
                'place': 'По парку',
                'time': '12:00',
                'action': 'Пробежка',
                'frequency': 1,
                'estimated_time': '1:59',
                'user': self.user
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['place'], 'По парку')
