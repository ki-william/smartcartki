from itertools import count
from lib2to3.pgen2 import token
from rest_framework import status
from .models import *
from django.http import JsonResponse
from django.shortcuts import render
from .models import Cart, Order, OrderItem, Product
from .serializers import ProductSerializer , OrderSerializer,UserProfileSerializer,RateSerializer,recommendationsserialiser
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from random import randint
from collections import OrderedDict

import requests 
from django import http
# @csrf_exempt
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username,password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({"message":"logged successfully"+" "+str(username)})
#         else :
#             return JsonResponse({"message":"wrong password"})

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = self.serializer_class(data=data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email
        })



@csrf_exempt
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
            'message': 'Succseccfully Registerd'}, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)
      
        # username = request.data.get('username')
        # password = request.data.get('password')
        # confirm_password = request.data.get('confirm_password')
        # if password == confirm_password: 
        #     User.objects.create_user(username = username,  password = password) 
        #     return JsonResponse({"message":"created successfully"+" "+str(username) })
        # else :
        #     return JsonResponse({"message":"wrong password"})


@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_profile(request):
    user_profile  = UserProfile.objects.get(username=request.user.username)
    serializer = UserProfileSerializer(user_profile)
    return JsonResponse(serializer.data, safe=False)



@csrf_exempt
@api_view(['GET'])
def products_list(request):   
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)


   
@csrf_exempt
@api_view(['GET'])
def orders_list(request):   
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data, safe=False)



@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_order_details(request,id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)



@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_orders(request,):   
    if request.method == 'GET':
        id=request.user.id
        user_orders = Order.objects.filter(customer=id)
        serializer = OrderSerializer(user_orders, many=True)
        return JsonResponse(serializer.data, safe=False)


def calculate_amount_of_order(self):
    return

@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_order_details(request,id):
    try:
        order = Order.objects.get(id=id)
        
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = OrderSerializer(order)
    return Response(serializer.data)






@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_order(request):
    if request.method == 'POST':
        try : 
            cart = Cart.objects.get(id = request.data.get("cart"))
        except Cart.DoesNotExist:
            return Response ( {"Error":" Cart dosn't exist "}) 
        if cart.occupied :
           return JsonResponse({"message":"cart not availabe"})
        else:
            order = Order.objects.create(customer=request.user,cart=cart)
            serializer = OrderSerializer(order)
            return JsonResponse({"order":serializer.data})



@csrf_exempt
@permission_classes([IsAuthenticated])
@api_view(['POST','GET'])
def adding_orderItem(request):
  
    if request.method == 'POST':
        barcode=request.data.get("barcode")
        try:
            product = Product.objects.get(barcode=barcode)
            price_of_product=product.price
            print("=============================")
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order=request.user.order_set.last()
        checker=0
        for i in order.orderItems.all():
            if product == i.product:
                checker=1
                break

        if checker == 1 :
            f =order.orderItems.get(product=product)
            setattr(f,"quantity",f.quantity+1)
            setattr(f,"price",(f.quantity*price_of_product))
            setattr(product,"Quantity", product.Quantity-1)
            product.save()
            f.save()        
        else:
            order.orderItems.create(product=product,quantity=1,price=price_of_product) 
            setattr(product,"Quantity", product.Quantity-1)
            product.save()
    
        total_price = 0
        order_serializer = OrderSerializer(order)        
        for i in range(len(order_serializer.data['orderItems'])):
            total_price=total_price+order_serializer.data['orderItems'][i]['price']
         
        
        setattr(order,"total_price",total_price)
        print("=============================")

        print(request.user.balance)
        setattr(request.user,"balance", request.user.balance-total_price)
        order.save()    
        request.user.save()    
        order_serializer = OrderSerializer(order)
        return JsonResponse(order_serializer.data)

    elif request.method == 'GET':
        order=request.user.order_set.last()
        order_serializer = OrderSerializer(order)
        return JsonResponse(order_serializer.data)

x=4 

@csrf_exempt
@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serialzer = UserProfileSerializer(users,many=True)
        # data = JSONParser().parse(users)
        return JsonResponse(serialzer.data,safe=False)


@csrf_exempt
@api_view(['GET'])
def get_all_rates(request):
    if request.method == 'GET':
        rates = Rate.objects.all()
        serialzer = RateSerializer(rates,many=True)
        return JsonResponse(serialzer.data,safe=False)

    
temp=[]   
@api_view(['POST','GET'])
def send_and_receive(request):     
    if request.method == 'POST':  
        token = JSONParser().parse(request)
        if len(temp) < 3 :
            temp.append(token)
            return JsonResponse(token,safe=False)
        else :
            return JsonResponse(token,safe=False)
    elif request.method == 'GET':
        if len(temp)== 0:
            return JsonResponse("0",safe=False)
        else :
            response = temp[0]
            temp.clear()
            return JsonResponse(response,safe=False)
            
         


temp1=[]   
@api_view(['POST','GET'])
def send_and_receive_1(request):     
    if request.method == 'POST':  
        token = JSONParser().parse(request)
        if len(temp1) < 3 :
            temp1.append(token)
            return JsonResponse(token,safe=False)
        else :
            return JsonResponse(token,safe=False)
    elif request.method == 'GET':
        if len(temp1)== 0:
            return JsonResponse("0",safe=False)
        else :
            response = temp1[0]
            temp1.clear()
            return JsonResponse(response,safe=False)
            
temp2=[]   
@api_view(['POST','GET'])
def send_and_receive_2(request):     
    if request.method == 'POST':  
        token = JSONParser().parse(request)
        if len(temp2) < 3 :
            temp2.append(token)
            return JsonResponse(token,safe=False)
        else :
            return JsonResponse(token,safe=False)
    elif request.method == 'GET':
        if len(temp2)== 0:
            return JsonResponse("0",safe=False)
        else :
            response = temp2[0]
            temp2.clear()
            return JsonResponse(response,safe=False)



temp3=[]   
@api_view(['POST','GET'])
def send_and_receive_3(request):     
    if request.method == 'POST':  
        token = JSONParser().parse(request)
        if len(temp3) < 3 :
            temp3.append(token)
            return JsonResponse(token,safe=False)
        else :
            return JsonResponse(token,safe=False)
    elif request.method == 'GET':
        if len(temp3)== 0:
            return JsonResponse("0",safe=False)
        else :
            response = temp3[0]
            temp3.clear()
            return JsonResponse(response,safe=False)




temp4=[]   
@api_view(['POST','GET'])
def send_and_receive_4(request):     
    if request.method == 'POST':  
        token = JSONParser().parse(request)
        if len(temp4) < 3 :
            temp4.append(token)
            return JsonResponse(token,safe=False)
        else :
            return JsonResponse(token,safe=False)
    elif request.method == 'GET':
        if len(temp4)== 0:
            return JsonResponse("0",safe=False)
        else :
            response = temp4[0]
            temp4.clear()
            return JsonResponse(response,safe=False)


        
        
        
 #added new serializer(recommendationsserialiser) and two imports in views(random,orderdictionary) and added the url to urls.py
@csrf_exempt
@api_view(['GET'])
def recommendations(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serialzer = recommendationsserialiser(products,many=True)
        p1 = randint(0, len(serialzer.data)-1)
        p2 = randint(0, len(serialzer.data)-1)
        p3 = randint(0, len(serialzer.data)-1)
        print(serialzer.data)
        sz = OrderedDict()
        sz[p1] = serialzer.data[p1]
        sz[p2] = serialzer.data[p2]
        sz[p3] = serialzer.data[p3]
        return JsonResponse(sz,safe=False)



## imported in view requests and http , added a table in models.py(usedtransactions), 
@csrf_exempt
@api_view(['GET'])
def recharge(request):
    if request.method == 'GET':
        url = 'https://accept.paymob.com/api/auth/tokens'  # replace with other python app url or ip
        request_data = {'api_key': 'ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRVeE5EWXlMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuNGZMbXo5dzF0U05MdmhyMThtN0NRZ2dDalNZd0tHWHpjcjlXSV9jVG5DNUdzdzBGdjZPTWJKZFotLS1EazNRdHpBYmVVa3BKYXFfYUoxazRDVHQtX3c='}  # replace with data to be sent to other app
        response_post = requests.post(url, json=request_data)
        response_post_data = response_post.json()  # data returned by other app
        token = response_post_data['token']
        
        
        headers = {'authorization' : token}
        get_data = request.GET
        #transctionid = '47836548'
        if ('username' not in get_data or 'transctionid'  not in get_data) :
            return http.JsonResponse({"Error":"Username or transaction id is missing"})
        else :
            transctionid = get_data['transctionid']
            usernam = get_data['username']
            print(transctionid)
            url2 = "https://accept.paymob.com/api/acceptance/transactions/%s"%transctionid
            #urlspare = "https://accept.paymob.com/api/acceptance/transactions"
            get_paramters = {'transaction_id':transctionid}
            response_get = requests.get(url2, json=get_paramters, headers=headers)
            response_get_data = response_get.json()
            
            if ('id' in response_get_data and 'success' in response_get_data) :
                    usedtransaction = Usedtransactions.objects.filter(transactionid = transctionid).exists()
                    print(usedtransaction)
                    if not usedtransaction :
                        ##add it to used transactions 
                        Usedtransactions.objects.create(transactionid=transctionid,username =usernam )
                        current_balance = UserProfile.objects.filter(username=usernam).values_list('balance')
                        #print("----------",current_balance[0][0],type(current_balance[0][0]))
                        newcredit = response_get_data ['amount_cents']/100.0
                        new_balance  = float(current_balance[0][0]) + newcredit
                        UserProfile.objects.filter(username=usernam).update(balance= new_balance)
                        print(response_get_data)
                        return http.JsonResponse({"message":"Recharged sucessfully"},safe=False)
                    else : 
                        #update the DB
                        return http.JsonResponse({"Error":"Transaction ID is used before, Please try to recharge"},safe=False)
            else :     
                    return http.JsonResponse({"Error":"Username or transaction id is wrong","Paymentresponse":"%s"%response_get_data},safe=False)

