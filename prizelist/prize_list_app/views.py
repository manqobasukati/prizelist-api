from django.shortcuts import render

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import viewsets, status, generics, mixins
from rest_framework.views import APIView

from prize_list_app.models import Shop, Branch, Buyer, PrizeList, PrizeListItem, Order, OrderItem
from prize_list_app.serializers import *

from pandas import pandas as pd

from prize_list_app.data_handler_funcs import get_items


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class BranchView(APIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer

    def get_shop(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Branch.DoesNotExist:
            raise Http404

    def get(self,request,pk):
       shop = self.get_shop(pk)
       branches = Branch.objects.filter(shop=shop)
       serializer = BranchSerializer(branches, many=True)
       return Response(serializer.data)

    def post(self,request,pk):
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrizeListView(APIView):
    parser_class = (FileUploadParser,)
    queryset = PrizeList.objects.all()
    serializer_class = PrizeListSerializer

    def get_object(self, pk):
        try:
            return PrizeList.objects.get(pk=pk)
        except PrizeList.DoesNotExist:
            raise Http404

    def get_branch(self,pk):
        try:
            return Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            raise Http404

    def get_shop(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):

        serializer = PrizeListSerializer(data=request.data)
        my_file =  request.FILES['prize_list']
        if serializer.is_valid():
            prize_list_data = get_items(file_name=my_file)
            serializer_object = serializer.save()
            prize_list = self.get_object(serializer_object.id)
            for i in prize_list_data:
                prize_list_item = PrizeListItem(category=i['category'],label=i['label'],
                                                prize=i['prize'],prize_list=prize_list,shop=self.get_shop(kwargs['shop_id']),
                                                branch=self.get_branch(kwargs['branch_id'])
                                                )
                prize_list_item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    def get(self, request,**kwargs):
        shop = self.get_shop(kwargs['shop_id'])
        branch = self.get_branch(kwargs['branch_id'])
        prize_list = PrizeList.objects.filter(branch=branch)
        serializer = PrizeListSerializer(prize_list, many=True)
        return Response(serializer.data)

class PrizeListViewDetail(APIView):
    parser_class = (FileUploadParser,)
    serializer_class = PrizeListSerializer

    def get_object(self, pk):
        try:
            return PrizeList.objects.get(pk=pk)
        except PrizeList.DoesNotExist:
            raise Http404

    def get_branch(self,pk):
        try:
            return Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            raise Http404

    def get_shop(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise Http404

    def get_prize_list(self,pk):
        try:
            return PrizeList.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise Http404

    def get(self,request,**kwargs):
        prize_list = self.get_prize_list(kwargs['prize_list_id'])
        serializer = PrizeListSerializer(prize_list)
        return Response(serializer.data)

class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

class PrizeListItemViewSet(viewsets.ModelViewSet):
    queryset = PrizeListItem.objects.all()
    serializer_class = PrizeListItemSerializer

class OrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self, pk):
        try:
            return PrizeList.objects.get(pk=pk)
        except PrizeList.DoesNotExist:
            raise Http404

    def get_branch(self,pk):
        try:
            return Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            raise Http404

    def get_shop(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise Http404

    def get_item(self, pk):
        try:
            return PrizeListItem.objects.get(pk=pk)
        except PrizeListItem.DoesNotExist:
            raise Http404

    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self,request,**kwargs):
        orders = Order.objects.filter(shop=self.get_shop(kwargs['shop_id']),
                                        branch=self.get_branch(kwargs['branch_id']))
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self,request, **kwargs):
       
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer_object = serializer.save()
            print(serializer_object)
            for i in request.data['order_items']:
                order_item = OrderItem(
                                item=self.get_item(i['id']),
                                order=self.get_order(serializer_object.id),
                                shop=self.get_shop(kwargs['shop_id']),
                                branch=self.get_branch(kwargs['branch_id']),
                                quantity=i['quantity']
                                )
                order_item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class OrderItemView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self, pk):
        try:
            return PrizeList.objects.get(pk=pk)
        except PrizeList.DoesNotExist:
            raise Http404

    def get_branch(self,pk):
        try:
            return Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            raise Http404

    def get_shop(self, pk):
        try:
            return Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            raise Http404

    def get(self, request,**kwargs):
        items = OrderItem.objects.filter(shop=self.get_shop(kwargs['shop_id']),
                                        branch=self.get_branch(kwargs['branch_id']),)
        serializer = OrderItemSerializer(items,many=True)
        return Response(serializer.data)
