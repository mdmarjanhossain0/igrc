from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from django.utils import timezone
import requests

from mysite.constants.status_constants import(
	SUCCSS,
	ERROR
)
from account.api.utils import (
	mobile_check,
	generate_otp
)
from account.models import (
	Account,
)

from account.api.serializers import (
	AccountSerializer,
	RegisterSerializer,
	LoginSerializer
)

from drf_yasg.utils import swagger_auto_schema

class Login(APIView):
	permission_classes = [AllowAny]
	@swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: AccountSerializer}
    )
	def post(self, request):
		email = request.data.get("email")
		password = request.data.get("password")

		user = authenticate(email=email, password=password)
		if user is not None:
			refresh = RefreshToken.for_user(user)
			serializer = AccountSerializer(user)
			data = serializer.data
			data.update({
				"response": SUCCSS,
				"msg": "Successfully login.",
				"refresh": str(refresh),
				"access": str(refresh.access_token),
			})
			return Response(data, status=200)
		else:
			return Response({
				"response": ERROR,
				"msg": "Invalid credentials."}, status=200)


@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def send_otp_view(request, mobile):
	random_number = generate_otp()
	message = f"Your AAP OTP is {random_number}"
	url = f"http://bulksmsbd.net/api/smsapi?api_key=QXVFUSuVAarLD9DgTw2X&type=text&number={mobile}&senderid=8809617619967&message={message}"
	payload  = {}
	headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	response = requests.get(url)
	return Response(
			data={
				"response": SUCCSS,
				"msg": "We have sent a 4 Digits otp to your registered number. Please check your phone sms and enter the Code below",
				"otp": random_number
			}
		)



@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={200: AccountSerializer, 401: 'Invalid credentials'},
)
@api_view(["POST"])
@permission_classes([])
@authentication_classes([])
def register_view(request):
	data = {}
	mobile = request.data.get("mobile", None)
	if mobile_check(mobile):
		return Response(
			data={
				"response": ERROR,
				"msg": "Number already exist.",
			}
		)
	serializer = RegisterSerializer(data=request.data)
	if serializer.is_valid():
		obj = serializer.save()
		# obj.otp = generate_otp()
		# obj.otp_send_time = timezone.now()
		# obj.save()
		data = AccountSerializer(obj).data
		refresh = RefreshToken.for_user(obj)
		data = data
		data.update({
				"response": SUCCSS,
				"msg": "Successfully register.",
				"refresh": str(refresh),
				"access": str(refresh.access_token),
			})
		return Response(data=data)
	else:
		return Response(serializer.errors, status=400)

@api_view(
	[
		"POST",
	]
)
@permission_classes([])
@authentication_classes([])
def send_forget_password_otp_view(request):
	data = {}
	mobile = request.data["mobile"]
	try:
		account = Account.objects.get(moible=mobile)
		random_number = generate_otp()
		account.otp = random_number
		account.otp_send_time = timezone.now()
		message = f"Your AAP OTP is {random_number}"
		url = f"http://bulksmsbd.net/api/smsapi?api_key=QXVFUSuVAarLD9DgTw2X&type=text&number={contact_no}&senderid=8809617619967&message={message}"
		payload  = {}
		headers = {
		'Content-Type': 'application/x-www-form-urlencoded'
		}
		response = requests.get(url)
		account.save()
		return Response(
			data={
				"response": SUCCSS,
				"msg": "We have sent a 4 Digits otp to your registered number. Please check your phone sms and enter the Code below"
			}
		)
	except:
		return Response(
			data={
				"response": ERROR,
				"msg": "Not found"
			}
		)



@api_view(
	[
		"POST",
	]
)
@permission_classes([])
@authentication_classes([])
def forget_password_view(request):
	data = {}
	mobile = request.data["mobile"]
	otp = request.data["otp"]
	try:
		account = Account.objects.get(mobile=mobile)
		if account.otp == otp:
			refresh = RefreshToken.for_user(account)
			data = {
				"response": SUCCSS,
				"msg": None,
				"refresh": str(refresh),
				"access": str(refresh.access_token),
			}
			return Response(data=data)
		else:
			return Response(
                data={
                    "response": ERROR,
                    "msg": "Invalid OTP"
                }
            )
	except:
		return Response(
			data={
				"response": "error",
				"msg": "Not found"
			}
		)



class AccountListApiView(ListAPIView):
	queryset = Account.objects.all()
	serializer_class = AccountSerializer

class TenantAccountListApiView(ListAPIView):
	serializer_class = AccountSerializer


	def get_queryset(self):
		tenant_id = self.kwargs.get('tenant_id')
		print(tenant_id)
		return Account.objects.filter(tenant_id=tenant_id)
	