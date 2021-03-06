from django.contrib.auth import get_user_model
from django.views import View
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from .serializers import *
from .models import *
from django.db.models import Q


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    token = Token.objects.create(user=serializer.instance)
    token_data = {"token": token.key}
    user_profile = UserProfile()
    user_profile.save()
    return Response(
        {**serializer.data, **token_data},
        status=status.HTTP_201_CREATED,
        headers=headers
    )


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserDetails(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserFriends(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self, *args, **kwargs):
        user_profile = UserProfile.objects.filter(pk=self.kwargs['pk'])
        friends_profiles = user_profile[0].friends.all()
        return friends_profiles


class MonetaryList(generics.ListCreateAPIView):
    queryset = DebtMonetary.objects.all()
    serializer_class = DebtMonetarySerializer


class MonetaryDetails(generics.RetrieveUpdateAPIView):
    serializer_class = DebtMonetarySerializer
    queryset = DebtMonetary.objects.all()


class ItemList(generics.ListCreateAPIView):
    serializer_class = DebtItemSerializer
    queryset = DebtItem.objects.all()


class ItemDetails(generics.RetrieveUpdateAPIView):
    serializer_class = DebtItemSerializer
    queryset = DebtItem.objects.all()


class CurrentUser(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        curUser = self.request.user
        user_profile = UserProfile.objects.filter(user=curUser)
        return user_profile


class UserMonetary(generics.ListCreateAPIView):
    serializer_class = DebtMonetarySerializer

    def get_queryset(self, *args, **kwargs):
        return DebtMonetary.objects.filter(Q(debtor=self.kwargs['pk']) | Q(creditor=self.kwargs['pk']))


class UserMonetaryWith(generics.ListCreateAPIView):
    serializer_class = DebtMonetarySerializer

    def get_queryset(self, *args, **kwargs):
        return DebtMonetary.objects.filter((Q(debtor=self.kwargs['pk1']) & Q(creditor=self.kwargs['pk2'])) | (Q(creditor=self.kwargs['pk1']) & Q(debtor=self.kwargs['pk2'])))


class UserDebtMonetary(generics.ListCreateAPIView):
    serializer_class = DebtMonetarySerializer

    def get_queryset(self, *args, **kwargs):
        return DebtMonetary.objects.filter(debtor=self.kwargs['pk'])


class UserDebtMonetaryWith(generics.ListAPIView):
    serializer_class = DebtMonetarySerializer

    def get_queryset(self):
        return DebtMonetary.objects.filter(debtor=self.kwargs['pk1'], creditor=self.kwargs['pk2'])


class UserCreditMonetary(generics.ListCreateAPIView):
    serializer_class = DebtMonetarySerializer

    def get_queryset(self, *args, **kwargs):
        return DebtMonetary.objects.filter(creditor=self.kwargs['pk'])


class UserCreditMonetaryWith(generics.ListAPIView):
    serializer_class = DebtMonetarySerializer

    def get_queryset(self):
        return DebtMonetary.objects.filter(creditor=self.kwargs['pk1'], debtor=self.kwargs['pk2'])


class UserItem(generics.ListCreateAPIView):
    serializer_class = DebtItemSerializer

    def get_queryset(self, *args, **kwargs):
        return DebtItem.objects.filter(Q(debtor=self.kwargs['pk']) | Q(creditor=self.kwargs['pk']))


class UserItemWith(generics.ListCreateAPIView):
    serializer_class = DebtItemSerializer

    def get_queryset(self, *args, **kwargs):
        return DebtItem.objects.filter((Q(debtor=self.kwargs['pk1']) & Q(creditor=self.kwargs['pk2'])) | (Q(creditor=self.kwargs['pk1']) & Q(debtor=self.kwargs['pk2'])))


class UserDebtItem(generics.ListCreateAPIView):
    serializer_class = DebtItemSerializer

    def get_queryset(self, *args, **kwargs):
        return DebtItem.objects.filter(debtor=self.kwargs['pk'])


class UserDebtItemWith(generics.ListAPIView):
    serializer_class = DebtItemSerializer

    def get_queryset(self):
        return DebtItem.objects.filter(debtor=self.kwargs['pk1'], creditor=self.kwargs['pk2'])


class UserCreditItem(generics.ListCreateAPIView):
    serializer_class = DebtItemSerializer

    def get_queryset(self, *args, **kwargs):
        return DebtItem.objects.filter(creditor=self.kwargs['pk'])


class UserCreditItemWith(generics.ListAPIView):
    serializer_class = DebtItemSerializer

    def get_queryset(self):
        return DebtItem.objects.filter(creditor=self.kwargs['pk1'], debtor=self.kwargs['pk2'])

class SearchUserList(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):

        username = self.kwargs['username']
        return UserProfile.objects.filter(username=username)

class PropositionList(generics.ListCreateAPIView):
    serializer_class = PropositionSerializer
    queryset = Proposition.objects.all()


class PropositionDetails(generics.RetrieveUpdateAPIView):
    serializer_class = PropositionSerializer
    queryset = Proposition.objects.all()

class UserPropositionSender(generics.ListCreateAPIView):
    serializer_class = PropositionSerializer

    def get_queryset(self, *args, **kwargs):
        return Proposition.objects.filter(sender=self.kwargs['pk'])

class UserPropositionReceiver(generics.ListCreateAPIView):
    serializer_class = PropositionSerializer

    def get_queryset(self, *args, **kwargs):
        return Proposition.objects.filter(receiver=self.kwargs['pk'])

@api_view(['GET'])
def DebtsMonetarySum(request, *args, **kwargs):
    mySum = DebtMonetary.objects.filter(debtor=kwargs['pk'], isActive=True).aggregate(Sum('amount'))["amount__sum"] or 0
    return Response({'sum': mySum})



@api_view(['GET'])
def CreditsMonetarySum(request, *args, **kwargs):
    mySum = DebtMonetary.objects.filter(creditor=kwargs['pk'], isActive=True).aggregate(Sum('amount'))["amount__sum"] or 0
    return Response({'sum': mySum})


@api_view(['GET'])
def MonetarySum(request, *args, **kwargs):
    credits_sum = DebtMonetary.objects.filter(creditor=kwargs['pk'], isActive=True).aggregate(Sum('amount'))["amount__sum"] or 0
    debts_sum = DebtMonetary.objects.filter(debtor=kwargs['pk'], isActive=True).aggregate(Sum('amount'))["amount__sum"] or 0
    mySum = credits_sum - debts_sum
    return Response({'sum': mySum})

@api_view(['GET'])
def MonetarySumWith(request, *args, **kwargs):
    credits_sum = DebtMonetary.objects.filter(creditor=kwargs['pk1'], debtor=kwargs['pk2'], isActive=True).aggregate(Sum('amount'))["amount__sum"] or 0
    debts_sum = DebtMonetary.objects.filter(creditor=kwargs['pk2'], debtor=kwargs['pk1'], isActive=True).aggregate(Sum('amount'))["amount__sum"] or 0
    mySum = credits_sum - debts_sum
    return Response({'sum': mySum})


@api_view(['GET'])
def DebtsItemCount(request, *args, **kwargs):
    myCount = DebtItem.objects.filter(debtor=kwargs['pk'], isActive=True).count()
    return Response({'count': myCount})


@api_view(['GET'])
def CreditsItemCount(request, *args, **kwargs):
    myCount = DebtItem.objects.filter(creditor=kwargs['pk'], isActive=True).count()
    return Response({'count': myCount})
