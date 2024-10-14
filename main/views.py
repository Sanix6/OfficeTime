from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import Visit
from datetime import datetime, date
from .functions import check_employee_in_office
from .serializers import *
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated  



class CheckInView(generics.CreateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]  

    def create(self, request, *args, **kwargs):
        lat_employee = request.data.get('lat_a')
        lon_employee = request.data.get('lon_a')

        if not request.user.is_authenticated: 
            return Response({'status': 'failure', 'message': 'Вы не автаризованы.'}, status=401)

        if check_employee_in_office(lat_employee, lon_employee):
            visit = Visit.objects.create(
                user=request.user, 
                data=timezone.now().date(),
                time=timezone.now().time(),
                status='В офисе',
                lat_a=lat_employee,
                lon_a=lon_employee,
                is_active=True  
            )
            serializer = self.get_serializer(visit)
            return Response({'status': 'success', 'message': 'Вы в офисе!', 'visit': serializer.data})
        else:
            return Response({'status': 'failure', 'message': 'Вы не находитесь рядом с офисом.'}, status=400)



class CheckOutView(generics.UpdateAPIView):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    def update(self, request, *args, **kwargs):
        visit = self.get_object()
        
        if visit.is_active:
            visit.is_active = False
            visit.status = 'Вне офиса' 
            visit.save()
            serializer = self.get_serializer(visit)
            return Response({'status': 'success', 'message': 'Вы покинули офис.', 'visit': serializer.data})
        else:
            return Response({'status': 'failure', 'message': 'Вы уже покинули офис.'}, status=400)
        

class ActivityListView(generics.GenericAPIView):
    queryset = Visit.objects.filter(is_active=True)
    serializer_class = ActivityListSerializer

    def get(self, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AttendanceView(generics.GenericAPIView):
    queryset = Visit.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class HistorySalaryView(generics.GenericAPIView):
    queryset = Salary.objects.all()
    serializer_class = HistorySalarySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all() 
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user