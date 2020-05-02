from django.db import models
from datetime import date, datetime

class Shop(models.Model):
    name = models.CharField(max_length=50)

class Branch(models.Model):
    name = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)

class Buyer(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
    location = models.CharField(max_length=100)

class PrizeList(models.Model):
    shop = models.ForeignKey(Shop,related_name='shop',on_delete=models.CASCADE)
    prize_list_file = models.FileField(blank=False,default=False)
    branch = models.ForeignKey(Branch,related_name='branch',on_delete=models.CASCADE)
    date_submitted = models.DateField(date.today)
    date_valid_to = models.DateField(default=date.today)




class PrizeListItem(models.Model):
    category = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    prize = models.FloatField(max_length=100)
    shop = models.ForeignKey(Shop,related_name='shop_name',on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    prize_list = models.ForeignKey(PrizeList,related_name='prize_list_item',on_delete=models.CASCADE)

class Order(models.Model):
    order_time = models.DateTimeField(default=datetime.now)
    shop = models.ForeignKey(Shop ,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)

class OrderItem(models.Model):
    item = models.ForeignKey(PrizeListItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='order_items',on_delete=models.CASCADE)
    shop =  models.ForeignKey(Shop,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    quantity = models.IntegerField()








