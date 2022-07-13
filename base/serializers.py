from itertools import product
from rest_framework import serializers
from .models import Cart, OrderItem, Product, Order, UserProfile,Rate
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, )

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'email', 'balance','password','image')

    def create(self, validated_data):
        user = super(UserProfileSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer2(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('username')


#
# class UserProfileSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = UserProfile
#         fields = ('id','user','image')
#

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'Quantity', 'image','weight','barcode']


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True)
    customer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'cart', 'date_ordered', 'complete','orderItems','transaction_id']

class RateSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)
   
    class Meta:
        model = Rate
        fields = "__all__"



###############
class productPictureSerialiser(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Product
        fields = ('image')

    def get_image_url(self, obj):
        return obj.image.url



class Cartserialiser(serializers.ModelSerializer):
    #currentuser = UserProfileSerializer2(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['cartnumber', 'barcode', 'currentuser','isreserved']
