from rest_framework import generics
from django.contrib.auth.models import User
from devhouse.models import Shop, Schedule, Shift
from .serializers import ShopSerializer, UserSerializer, ScheduleSerializer, ShiftSerializer
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
import json


class ShopCreate(generics.CreateAPIView):
    serializer_class = ShopSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


@permission_classes((permissions.AllowAny, ))
class ShopDetail(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            return

    def get(self, request, shop_id):
        shop = self.get_object(shop_id)
        if not shop:
            return Response(status=404)
        serializer = ShopSerializer(shop)
        return Response({
            'result': serializer.data,
            'message': 'success'
        })


@permission_classes((permissions.AllowAny, ))
class ShopSchedule(ShopDetail):
    queryset = Schedule.objects.all()

    def get(self, request, shop_id):
        schedules = Schedule.objects.filter(shop_id=shop_id)
        if not schedules.count():
            return Response(data=schedules, status=404)
        serializer = ScheduleSerializer(schedules, many=True)

        return Response(json.dumps(serializer.data))


class ShopClose(generics.UpdateAPIView):
    serializer_class = ShiftSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, data):
        qs = Shift.objects.filter(shop_id=data.get("shop"), closed=None)
        if qs.count() != 1:
            return
        return qs[0]

    def update(self, request, *args, **kwargs):
        instance = self.get_object(request.data)

        if not instance:
            return Response(status=404)
        instance.closed = datetime.now()
        instance.now_working = False

        instance.save()

        serializer = ShiftSerializer(instance, data=instance.as_dict())
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UpdateSchedule(generics.UpdateAPIView):
    serializer_class = ScheduleSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self, data):
        qs = Schedule.objects.filter(shop_id=data.get("shop"), daytype=data.get("daytype"),
                                     periodtype=data.get("periodtype"), deleted=False)
        if qs.count() != 1:
            return
        return qs[0]

    def update(self, request, *args, **kwargs):
        instance = self.get_object(request.data)
        if not instance:
            return Response(status=404)
        instance.period_start = request.data.get("period_start")
        instance.period_end = request.data.get("period_end")
        instance.save()
        serializer = ScheduleSerializer(instance, data=instance.as_dict())
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((permissions.AllowAny, ))
class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = ()
    permission_classes = ()


@permission_classes((permissions.AllowAny, ))
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, user_id):
        user = self.get_object(user_id)
        if not user:
            return Response(None)
        serializer = UserSerializer(user)
        return Response({
            'result': serializer.data,
            'message': 'success'
        })
