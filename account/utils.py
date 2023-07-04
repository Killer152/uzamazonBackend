import logging
import random
import string
import datetime
from rest_framework.generics import get_object_or_404
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView, jwt_response_payload_handler

from vendors.models import VendorModel

logger = logging.getLogger(__file__)


def get_sms_json_template(phone, text, sms_id):
    d = "[{'phone':'" + phone + "', 'text':'" + text + "'}]"
    data = {
        'login': settings.SMS_LOGIN,
        'password': settings.SMS_PASS,
        'data': d
    }
    return data


def send_sms(data):
    # text = settings.SMS_LOGIN + ':' + settings.SMS_PASS
    # text = text.encode('utf-8')
    # encoded = base64.b64encode(text)
    # encoded = encoded.decode('utf-8')
    #
    # headers = {
    #     'Content-Type': "application/json",
    #     'Authorization': "Basic " + encoded,
    #     'cache-control': "no-cache",
    #     'Postman-Token': "effa6d6c-01b4-475c-8094-78b1f49c8282"
    # }
    r = requests.post(settings.SMS_URL, data=data)
    logger.error(str(datetime.datetime.now()) + '\n' + r.text)


def send_sms_code(phone, text, user_id):
    # data = get_sms_json_template(phone, text, user_id)
    d = '[{"phone":"' + phone + '", "text":"' + text + '"}]'
    data = {
        'login': 'KOINOT',
        'password': '84uiiZ27a90al7dB0cjL',
        'data': d
    }

    print(d)

    # response = requests.post('http://185.8.212.184/smsgateway/', data=data) нада
    # logger.error(str(datetime.datetime.now()) + '\n' + response.text)

    # send_sms(data)


def generate_token(length):
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(length))


def generate_code():
    return random.randint(10000, 99999)


def send_code(phone, code):
    text = 'UzAmazon'


class NewJSONWebTokenAPIView(APIView):
    """
    Base API View that various JWT interactions inherit from.
    """
    permission_classes = ()
    authentication_classes = ()

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'view': self,
        }

    def get_serializer_class(self):
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__)
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            if VendorModel.objects.filter(user=user).exists():
                response_data["sent_request"] = VendorModel.objects.get(user__username=user.username).sent_request
                response_data["verified"] = VendorModel.objects.get(user__username=user.username).verified
            else:
                response_data["sent_request"] = False
                response_data["verified"] = False
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewObtainJSONWebToken(NewJSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer
