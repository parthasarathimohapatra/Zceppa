from django.shortcuts import render
from .models import *
from .auth import *
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
#from rest_framework.authtoken import Token
from rest_framework.permissions import AllowAny

# Create your views here.

class CustomerRegistration(APIView):
    permission_classes=(AllowAny,)
    def post(self, request):
        try:
            customer_exists = UserProfile.objects.filter(phone=request.data.get("phone"))
            if customer_exists:
                return Response({"status": False, "detail": "The phone No is already registerd"})
            else:
                customer_email_exists = UserProfile.objects.filter(email=request.data.get("email"))
                if customer_email_exists:
                    return Response({"status": False, "detail": "The Email is already registerd"})
                else:
                    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    if(re.fullmatch(regex, request.data.get("email").lower())):
                        if request.data.get("phone").isnumeric():
                            if len(request.data.get("phone")) == 10:
                                customer_save = UserProfile(name=request.data.get("name"),
                                                        dob=request.data.get("dob"),
                                                        phone=request.data.get("phone"),
                                                        email=request.data.get("email").lower(),
                                                        password=request.data.get("password"),
                                                        gender=request.data.get('gender'),
                                                        )
                                customer_save.save()
                                return Response({"status": True,"detail": "You are Successfully registerd","customer_details": "1"})
                            else:
                                return Response({"status": False,"detail": "Please Enter Only 10 Digit Phone Number"})
                        else:
                            return Response({"status": False,"detail": "Please Enter Correct Phone Number"})
                    else:
                        return Response({"status": False,"detail": "Please Enter Correct Email Format"})
        except:
            return Response({
                'status': False,
                'detail': "something went wrong"
            })
            
class CustomerLogin(APIView):
    permission_classes=(AllowAny,)
    def post(self, request):
        #try:
            print("success")
           # email=request.data.get("email")
            if UserProfile.objects.filter(email=request.data.get("email")):
                customer_email=UserProfile.objects.get(email=request.data.get("email"))
               
                if customer_email :
                    if ((customer_email.password) == (request.data.get("password"))):
                        #token = Token.objects.get_or_create(customer_email)
                        token = jwt.encode(
                            {"user": customer_email.customer_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3000)},
                              'secret', algorithm='HS256')
                        return Response({"status": True,"customer":customer_email.customer_id, "token":token})
                    else:
                        return Response({"status": False,"detail": "Please Enter Correct Password"})
                else:
                    return Response({"status": False, "detail": "Please Enter Valid Details"})
            else:
                return Response({"status": False, "detail": "Please Enter correct Email"})

        # except:
        #     return Response({
        #         'status': False,
        #         'detail': "something went wrong"
        #     })

class UserProfileView(APIView):
    permission_classes=(AllowAny,)
    # permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(customer_id=request.data.get("id"))
            #status_code = status.HTTP_200_OK
            response = {
                #'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'name': user_profile.name,
                    'dob': user_profile.dob,
                    'phone': user_profile.phone,
                    'email': user_profile.email,
                    'gender': user_profile.gender,
                    }]
            }
            return Response({"status": True,"Customer": response })
        except:
            return Response({
                'status': False,
                'detail': "something went wrong"
            })