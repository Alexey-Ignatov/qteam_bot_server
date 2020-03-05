from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import datetime
from rest_framework import authentication, permissions
from rest_framework import routers, serializers, viewsets

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer, CardSerializer, BotUserSerializer
from .models import Card, CardLike, CardDislike,BotUser,BotUserToCardCategory, CardCategory,BookEveningEvent
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
import requests

dayno_2_dayname = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"

}

dates_on_btns_num = 7


def upd_resp_path(bot_user, resp_path):
    bot_user.main_resp_path = resp_path
    bot_user.save()


def get_date_btns(card_id, bot_user):
    btns_list = []
    #for cat in cats:
    #    btns_list.append([{'text': cat.title, "callback_data": json.dumps({'cat_id': cat.id, 'action': 'on'})}])

    for i in range(dates_on_btns_num):
        i_datetime = timezone.now() + datetime.timedelta(days=i)
        text = dayno_2_dayname[i_datetime.weekday()] + ', ' + str(i_datetime.date().strftime("%d.%m"))
        text = 'Сегодня'+ ', ' + str(i_datetime.date().strftime("%d.%m")) if i == 0 else text
        text = 'Завтра' + ', ' + str(i_datetime.date().strftime("%d.%m")) if i == 1 else text
        if i in [0, 1] or i_datetime.weekday() in [4, 5, 6]:
            #TODO тут сохраняется время по таймзоне на сервере
            btns_list.append([{'text': text, "callback_data": json.dumps({'card_id': card_id, 'date': str(i_datetime.date())})}])
    return btns_list

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
        resp_path = request.data['resp_path']
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)


        upd_resp_path(bot_user, resp_path)

        try:
            cat = CardCategory.objects.get(pk=real_data['cat_id'])
        except CardCategory.DoesNotExist:
            raise Http404

        try:
            user_cats = BotUserToCardCategory.objects.get(bot_user=bot_user, card_category=cat)
            if real_data['action'] == 'off':
                user_cats.delete()
        except BotUserToCardCategory.DoesNotExist:
            if real_data['action'] == 'on':
                BotUserToCardCategory.objects.create(bot_user=bot_user, card_category=cat)

        return Response({})

class ResetPrefsApi(APIView):

    @staticmethod
    def get(request, bot_user_id):
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        resp_path = request.GET['resp_path']
        upd_resp_path(bot_user, resp_path)

        BotUserToCardCategory.objects.filter(bot_user = bot_user).delete()

        return Response({})


class LikeApi(APIView):

    @staticmethod
    def post(request, bot_user_id):
        print('real_data', request.data)
        real_data = json.loads(request.data['str_to_parse'])
        resp_path = request.data['resp_path']
        print('real_data', real_data)
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)


        upd_resp_path(bot_user, resp_path)

        try:
            card = Card.objects.get(pk=real_data['card_id'])
        except Card.DoesNotExist:
            raise Http404

        if real_data['type'] == 'like':
            CardLike.objects.create(bot_user=bot_user, date=timezone.now(), card = card )

        if real_data['type'] == 'dislike':
            CardDislike.objects.create(bot_user=bot_user, date=timezone.now(), card = card )

        btns_list = get_date_btns(real_data['card_id'], bot_user)
        return Response({"btns_json": json.dumps(btns_list)})
        #return Response({"time":})


class BookEveningApi(APIView):
    @staticmethod
    def post(request, bot_user_id):
        real_data = json.loads(request.data['str_to_parse'])
        resp_path = request.data['resp_path']

        date = datetime.datetime.strptime(real_data['date'], "%Y-%m-%d").date()
        print('date', 'date')
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        upd_resp_path(bot_user, resp_path)

        try:
            card = Card.objects.get(pk=real_data['card_id'])
        except Card.DoesNotExist:
            raise Http404


        try:
            BookEveningEvent.objects.get(bot_user=bot_user, card=card, planed_date=date)
        except BookEveningEvent.DoesNotExist:
            BookEveningEvent.objects.create(bot_user=bot_user, card=card, planed_date=date)


        return Response({})
        #return Response({"time":})



class GetCardsApi(APIView):

    @staticmethod
    def get(request, bot_user_id):
        meta = request.META
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        resp_path = request.GET['resp_path']
        print('resp_path', resp_path)
        upd_resp_path(bot_user, resp_path)

        #user_cats = BotUserToCardCategory.objects.filter(bot_user = bot_user)

        #if len(user_cats) < 3:
        #    return Response({'answer': 'less 3 cats'})

        serializer = CardSerializer(Card.objects.all(), many=True)
        return Response(serializer.data)



class RegisterUser(APIView):
    @staticmethod
    def post(request, bot_user_id):
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        resp_path = request.data['resp_path']
        print('resp_path', resp_path)
        upd_resp_path(bot_user, resp_path)

        data_to_validate = request.data

        print(request.data)
        #data_to_validate['cashbox'] = device_id
        return Response({})


class GetMyStrCategories(APIView):
    @staticmethod
    def get(request, bot_user_id):
        meta = request.META
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        resp_path = request.GET['resp_path']
        print('resp_path', resp_path)
        upd_resp_path(bot_user, resp_path)

        user_cats = BotUserToCardCategory.objects.filter(bot_user = bot_user)

        res_list = [user_2_cat.card_category.title for user_2_cat in user_cats]

        print(request.data)
        res_str = ', '.join(res_list) if res_list else "Ни одной категории не выбрано"

        return Response({"user_cats":res_str})


class GetCatButtonsList(APIView):
    @staticmethod
    def get(request, bot_user_id):
        meta = request.META
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        resp_path = request.GET['resp_path']
        print('resp_path', resp_path)
        upd_resp_path(bot_user, resp_path)


        btns_list = []
        cats = CardCategory.objects.all()
        for cat in cats:
            btns_list.append([{'text':cat.title, "callback_data":json.dumps({'cat_id':cat.id, 'action':'on'})}])

        btns_list+=[[{"text":"Посмотреть мои категории", "callback_data":"{\"show_cats\":true}"}],
                    [{"text":"❌ Сбросить категории ❌","callback_data":"reset cats"}]]

        return Response({"btns_json": json.dumps(btns_list)})










class SendFreeEveningReminderApi(APIView):

    @staticmethod
    def get(request):
        url = "https://flowxo.com/hooks/a/d678bypz"
        curr_date = timezone.now().date()
        today_book_events = BookEveningEvent.objects.filter(planed_date=curr_date)
        for event in today_book_events:
            curr_bot_user = event.bot_user
            curr_card = event.card

            send_data = {'text':"Дорогой друг! Освободи вечер, у тебя сегодня: "+ curr_card.title ,
                         "resp_path": curr_bot_user.main_resp_path,
                         'card':CardSerializer(curr_card).data}

            response = requests.post(url, json=send_data)

        return Response({})
        #return Response({"time":})



class SendAddActivityApi(APIView):

    @staticmethod
    def get(request):
        url = "https://flowxo.com/hooks/a/2m8bd4q9"
        curr_date = timezone.now().date()
        today_book_events = list(BookEveningEvent.objects.filter(planed_date__gte=curr_date))

        users = list(set([event.bot_user for event in today_book_events]))
        resppath_2_card_list ={bot_user.bot_user_id:[event.card for event in today_book_events if bot_user==event.bot_user]
                for bot_user in users}

        print('resppath_2_card_list', resppath_2_card_list)


        for bot_user_id, future_card_list in resppath_2_card_list.items():
            # todo
            if len(future_card_list) < 200:
                cards_liks = CardLike.objects.filter(bot_user__bot_user_id=bot_user_id).order_by('?')
                cards = list(set([cl.card for cl in cards_liks])- set(future_card_list))
                bot_user = BotUser.objects.get(bot_user_id=bot_user_id)

                send_data = {"resp_path": bot_user.main_resp_path,
                             'cards':CardSerializer(cards[:3], many=True).data}

                print('send_data', send_data)

                response = requests.post(url, json=send_data)

        return Response({})
        #return Response({"time":})


class GetWeekPlansApi(APIView):

    @staticmethod
    def get(request, bot_user_id):
        meta = request.META
        try:
            bot_user = BotUser.objects.get(bot_user_id=bot_user_id)
        except BotUser.DoesNotExist:
            bot_user = BotUser.objects.create(bot_user_id=bot_user_id)

        resp_path = request.GET['resp_path']
        upd_resp_path(bot_user, resp_path)

        curr_date = timezone.now().date()
        today_book_events = list(BookEveningEvent.objects.filter(planed_date__gte=curr_date, bot_user = bot_user))

        print('today_book_events', today_book_events)

        resp_list = []
        for book_event in today_book_events:
            text_date = dayno_2_dayname[book_event.planed_date.weekday()] + ', ' + str(book_event.planed_date.strftime("%d.%m"))
            if book_event.planed_date == timezone.now() + datetime.timedelta(days=1):
                text_date = "Завтра"

            if book_event.planed_date == timezone.now():
                text_date = "Сегодня"

            resp_list.append({
                'card': CardSerializer(book_event.card).data,
                'date':text_date
            })


        return Response({'resp_data':resp_list})
        #return Response({"time":})
