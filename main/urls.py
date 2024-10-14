from django.urls import path
from .views import *

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='check'),
    path('api/check-out/', CheckOutView.as_view(), name='check-out'),
    path('active/users', ActivityListView.as_view(), name='active-users'),
    path('attendance/', AttendanceView.as_view(), name='attendance'),
    path('history/salary', HistorySalaryView.as_view(), name='history-salary'),
    path('profile', ProfileDetailView.as_view(), name='profile')

]