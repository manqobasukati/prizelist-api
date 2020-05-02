from django.contrib.auth.models import User
from rest_framework import serializers
from prize_list_app.models import Shop, Branch, Buyer, PrizeList, PrizeListItem, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(
                username=validated_data['username'],
                password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = "__all__"

class BranchSerializer(serializers.ModelSerializer):
   
     class Meta:
        model = Branch
        fields = "__all__"
     
     



class BuyerSerializer(serializers.ModelSerializer):

     class Meta:
        model = Buyer
        fields = "__all__"

class PrizeListItemSerializer(serializers.ModelSerializer):
     class Meta:
        model = PrizeListItem
        fields = ['category','label','prize','id']

class PrizeListSerializer(serializers.ModelSerializer):
     prize_list_item = PrizeListItemSerializer(many=True,read_only=True)
     class Meta:
        model = PrizeList
        fields = ['date_submitted','shop', 'date_valid_to','prize_list_item','id','branch']



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
     order_items = OrderItemSerializer(many=True,read_only=True)
     class Meta:
        model = Order
        fields = ['shop','order_items','branch','order_time']
