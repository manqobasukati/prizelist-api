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
    shop_user = UserSerializer()
    class Meta:
        model = Shop
        fields = "__all__"

    def create(self,validated_data):
        user_data = validated_data.get('shop_user')
        user_serialize = UserSerializer(data=user_data)
        if user_serialize.is_valid():
             user_object = user_serialize.save()
             shop = Shop.objects.create(shop_user=user_object, name=validated_data.get('name'))
             return shop
  



class BranchSerializer(serializers.ModelSerializer):
     shop = ShopSerializer(read_only=True)
     class Meta:
        model = Branch
        fields = "__all__"

     
#      def create(self,validated_data):
#         print(validated_data)
#         branch_data = validated_data.pop('shop')
#         shop = Shop.objects.get(**validated_data)
#         return Branch(shop=shop,**branch_data)
     
     



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
        fields = ['date_submitted','shop', 'date_valid_to','prize_list_item','id','branch','active']



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
     order_items = OrderItemSerializer(many=True,read_only=True)
     class Meta:
        model = Order
        fields = ['shop','order_items','branch','order_time']
