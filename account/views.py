import re

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveUpdateAPIView, GenericAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from account.models import UserModel, TokenModel, ProfileModel
from account.serializers import RegistrationTokenSerializer, PasswordSetSerializer, \
    ChangePasswordSerializer, \
    PasswordForgetCodeSerializer, ProfileSerializer, RegistrationSerializer, ProfileAvatarSerializer
from account.utils import send_sms_code, generate_code
from vendors.models import VendorModel


class RegistrationView(GenericAPIView):
    """Registration of new User
    POST:
    {
        username: string,
        password1: string,
        password2 string,
    }
    If passwords aren`t same returns: Passwords should be the same
    If user is already created returns: User with this phone has been already created
    If user account is not activated: User account is disabled
    If success: 'User was created successfully'
    If phone format incorrect: Incorrect phone number format
    """
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        data = serializer.validated_data
        username = data['username']
        errors = {}
        exists = User.objects.filter(username=username)
        if exists.exists():
            if exists.get().is_active:
                return Response({'message': 'User with this phone has been already created'},
                                status=status.HTTP_302_FOUND)
            else:
                return Response({'message': 'User account is disabled.'},
                                status=status.HTTP_308_PERMANENT_REDIRECT)
        if data['password1'] != data['password2']:
            errors['password2'] = {'Passwords should be the same'}
        matched = re.match(r'^998\d{9}$', username)
        if matched:
            code = generate_code()
            user = UserModel.objects.create(username=username, first_name=data['first_name'],
                                            last_name=data['last_name'], is_active=False)
            user.set_password(data['password1'])
            user.save()
            token = TokenModel.objects.create(user=user, code=code)
            text = 'Code: {}'.format(code)
            send_sms_code(username, text, token.id)
            ProfileModel.objects.create(user=user, dob=data['dob'], gender=data['gender'])
            return Response({'message': 'User was created successfully', 'status': True})
        else:
            return Response({'message': 'Incorrect phone number format'},
                            status=status.HTTP_418_IM_A_TEAPOT)


class RegistrationTokenView(GenericAPIView):
    """Endpoint for validating token sent to the user Returns:
        if code is valid:
        {
            "token": "some token"
        }
        if not:
        {
            "message": "Code is incorrect",
            "status": false
        }
    """
    serializer_class = RegistrationTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        code = data['code']
        username = data['username']
        token = TokenModel.objects.filter(code=code, user__username=username)
        if not token.exists():
            return Response({'message': 'Code is incorrect', 'status': False}, status=status.HTTP_200_OK)
        user = token.get().user
        user.is_active = True
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        TokenModel.objects.filter(user=user).delete()
        data = {'token': token}
        return Response(data, status=status.HTTP_201_CREATED)


class PasswordSetView(GenericAPIView):
    """Endpoint for setting password Returns:
        If passwords are the same:
        {
            "message": "Password was updated",
            "status": true
        }
        Otherwise:
        {
            "message": "Passwords should be the same",
            "status": false
        }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordSetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            password1 = serializer.data.get('password1')
            password2 = serializer.data.get('password2')
            if password1 != password2:
                return Response({'message': 'Passwords should be the same', 'status': False}, status=status.HTTP_200_OK)
            user = self.request.user
            user.set_password(password1)
            user.save()
            return Response({'message': 'Password was updated', 'status': True})

        return Response(serializer.errors, status=status.HTTP_200_OK)


class ChangePasswordView(UpdateAPIView):
    """Updates existing password
        Method PUT Returns:
        If old password is wrong:
        {
            "message": "Wrong password",
            "status": false
        }
        If passwords are not the same:
        {
            "message": "Passwords should be the same",
            "status": false
        }
        If success:
        {
            "message": "Success",
            "status": true
        }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    # param_config = openapi.Responses(responses={
    #     Union['dsf']: Response({'message': 'Wrong password', 'status': False}, status=status.HTTP_200_OK)})

    def get_object(self, queryset=None):
        return self.request.user

    # @swagger_auto_schema(responses='OK')
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password1 = serializer.data.get('new_password1')
            new_password2 = serializer.data.get('new_password2')
            if not self.object.check_password(old_password):
                return Response({'message': 'Wrong password', 'status': False}, status=status.HTTP_200_OK)
            if new_password1 != new_password2:
                return Response({'message': 'Passwords should be the same', 'status': False}, status=status.HTTP_200_OK)
            self.object.set_password(serializer.data.get('new_password1'))
            self.object.save()
            return Response({'message': 'Success', 'status': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_200_OK)


class PasswordForgetCodeView(GenericAPIView):
    """Forget password
    Args:
        username
    Returns:
        username
    """
    serializer_class = PasswordForgetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data.get('username')
            matched = re.match(r'^998\d{9}$', username)
            if matched:
                user = UserModel.objects.filter(username=username)
                if user.exists():
                    code = generate_code()
                    if_exists = TokenModel.objects.filter(user=user.get())
                    if if_exists.exists():
                        if_exists.delete()
                    token = TokenModel.objects.create(user=user.get(), code=code)
                    text = 'Code: {}'.format(code)
                    send_sms_code(user.get().username, text, token.id)
                    return Response({'message': 'Token was created successfully', 'status': True})
                return Response({'message': 'This phone number doesn\'t exist', 'status': False})
            return Response({'message': 'Incorrect phone number format', 'status': False})
        return Response(serializer.errors, status=status.HTTP_200_OK)


class ResetTokenView(GenericAPIView):
    """Endpoint that comes after forget password. Generates new token
    Args and Returns are the same as in /account/register/token
    """
    serializer_class = RegistrationTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        data = serializer.validated_data
        code = data['code']
        token = TokenModel.objects.filter(code=code, user__username=username)
        if not token.exists():
            return Response({'message': 'Code is incorrect', 'status': False}, status=status.HTTP_200_OK)
        user = token.get().user
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        TokenModel.objects.filter(user=user).delete()
        data = {'token': token}
        return Response(data, status=status.HTTP_200_OK)


class ProfileView(RetrieveUpdateAPIView):
    """Returns or updates profile
    Method GET for return
    Method PUT for update
    Args for PUT request:
        All args are optional but one of them should be compulsory
        profile: {"dob": "2003-02-02", "gender": "man"} // for gender send man/woman, dob in a form YYYY-mm-dd
        email
        last_name
        first_name Returns:
        {
            "id": 5,
            "username": "998999999999",
            "first_name": "rrr",
            "last_name": "rrr",
            "email": "mail202@gmail.com",
            "profile": {
                "dob": "2002-02-02",
                "gender": "woman"
            }
        }
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        return Response(data)

    def get_object(self):
        return self.request.user


class ProfileAvatarView(UpdateAPIView):
    serializer_class = ProfileAvatarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserDeleteView(DestroyAPIView):
    """User deletes himself account
    If successfully deleted returns: Successfully deleted
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response("Successfully deleted", status=status.HTTP_204_NO_CONTENT)


class UserStatus(APIView):
    def get(self, request):
        data = {
            "sent_request": False,
            "verified": False
        }
        if not self.request.user.is_anonymous and VendorModel.objects.filter(user=self.request.user).exists():
            data["sent_request"] = VendorModel.objects.get(user__username=self.request.user.username).sent_request
            data["verified"] = VendorModel.objects.get(user__username=self.request.user.username).verified
        return Response(data, status=status.HTTP_200_OK)

