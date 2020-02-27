from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rest_framework import authentication, permissions
from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CardSerializer, BotUserSerializer
from .models import Card, CardLike, CardDislike,BotUser
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
import json



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

class UpdPrefsApi(APIView):

    @staticmethod
    def put(request, bot_user_id):
        print(request.data)
        real_data = json.loads(request.data['str_to_parse'])
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            BotUser.objects.create(bot_user_id=bot_user_id)

        bot_user = BotUser.objects.filter(bot_user_id=bot_user_id)
        bot_user.update(**real_data)


        return Response(BotUserSerializer(BotUser.objects.get(bot_user_id=bot_user_id)).data)

        #serializer = OrderSerializer(data=data_to_validate)

        #if serializer.is_valid():
        #   with transaction.atomic():
        #        serializer.save()
        #        return Response(serializer.data)

        #print(serializer.errors)
        #raise ValidationError(serializer.errors)


class LikeApi(APIView):

    @staticmethod
    def post(request, bot_user_id):
        print(request.data)
        meta = request.META

        real_data = json.loads(request.data['str_to_parse'])
        print('real_data', real_data)
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        try:
            card = Card.objects.get(pk=real_data['card_id'])
        except Card.DoesNotExist:
            raise Http404

        if real_data['type'] == 'like':
            CardLike.objects.create(bot_user=bot_user, date=timezone.now(), card = card )

        if real_data['type'] == 'dislike':
            CardDislike.objects.create(bot_user=bot_user, date=timezone.now(), card = card )

        return Response({})




class GetCardsApi(APIView):

    @staticmethod
    def get(request, bot_user_id):
        meta = request.META

        data_to_validate = request.data

        print(request.data)

        serializer = CardSerializer(Card.objects.all(), many=True)
        return Response(serializer.data)
        #data_to_validate['cashbox'] = device_id
        return Response({})


class RegisterUser(APIView):
    @staticmethod
    def post(request, bot_user_id):
        meta = request.META

        data_to_validate = request.data

        print(request.data)
        #data_to_validate['cashbox'] = device_id
        return Response({})