from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Shop, Schedule, Shift
from devhouse.default_data import default_schedules
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data.pop("username"))
        user.set_password(validated_data.pop("password"))
        user.save()
        return user


class ShopSerializer(serializers.ModelSerializer):
    is_working = serializers.SerializerMethodField(method_name='check_is_working')

    class Meta:
        model = Shop
        fields = ('id', 'name', 'is_working')

    @staticmethod
    def check_is_working(instance):
        return Shift.objects.filter(shop_id=instance.id, closed=None, now_working=True).count() > 0

    def create(self, validated_data):
        shop = Shop(
            name=validated_data.pop("name"),
            owner_id=self.context['request'].user.id
        )
        if 'schedules' not in validated_data:
            validated_data['schedules'] = default_schedules
        shop.save()
        for i in validated_data['schedules']:
            i['shop'] = shop.id

        schedule_serializer = ScheduleSerializer(data=validated_data['schedules'], many=True)
        if schedule_serializer.is_valid():
            schedule_serializer.save()

        shift_serializer = ShiftSerializer(data={'shop': shop.id, 'now_working': True})
        if shift_serializer.is_valid():
            shift_serializer.save()
        return shop

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.email)
        instance.owner = validated_data.get('owner', instance.content)
        instance.save()
        return instance


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('shop', 'daytype', 'periodtype', 'period_start', 'period_end', 'is_working')

    def create(self, validated_data):
        schedule = Schedule(
            shop=validated_data.pop("shop"),
            daytype=validated_data.pop("daytype"),
            periodtype=validated_data.pop("periodtype"),
            period_start=validated_data.pop("period_start"),
            period_end=validated_data.pop("period_end"),
            is_working=validated_data.pop("is_working"),
            deleted=False
        )
        schedule.save()
        return schedule


class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ('shop', 'now_working')

    def create(self, validated_data):
        shift = Shift(
            shop=validated_data.pop("shop"),
            opened=datetime.now()
        )
        shift.save()
        return shift
