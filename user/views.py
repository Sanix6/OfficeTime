from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from .services import send_sms
from rest_framework.views import APIView


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]
            first_name = serializer.data["first_name"]
            last_name = serializer.data["last_name"]
            password = serializer.data["password"]

            user = User(
                phone=phone, first_name=first_name, last_name=last_name
            )
            user.set_password(password)
            user.save()

            sms_sent = send_sms(phone, "Подтвердите номер телефона", user.code)

            if sms_sent:
                return Response(
                    {
                        "response": True,
                        "message": "Код подтверждения был отправлен на ваш номер.",
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"response": False, "message": "Something went wrong!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneView(GenericAPIView):
    serializer_class = VerifyPhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
            phone = serializer.data["phone"]

            try:
                user = User.objects.get(phone=phone)

                if user.activated:
                    return Response({"message": "Аккаунт уже подтвержден"})

                if user.code == code:
                    user.activated = True
                    user.save()

                    token, created = Token.objects.get_or_create(user=user)

                    return Response(
                        {
                            "response": True,
                            "message": "Пользователь успешно зарегистрирован.",
                            "token": token.key,
                        }
                    )
                return Response(
                    {"response": False, "message": "Введен неверный код"}
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": "Пользователь с таким телефоном не существует",
                    }
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendCodeView(GenericAPIView):
    serializer_class = SendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]

            try:
                user = User.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "reponse": False,
                        "message": "Пользователь с таким телефоном не существует",
                    },
                )
            if not user.is_active:
                user.save()

                sms = send_sms(phone, "Ваш новый код подтверждения", user.code)

                return Response({"response": True, "message": "Код отправлен"})

            return Response(
                {"response": False, "message": "Аккаунт уже подтвержден"}
            )
        return Response(serializer.errors)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            phone = request.data.get("phone")
            password = request.data.get("password")

            try:
                get_user = User.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": "Пользователь с указанными телефоном не существует",
                    }
                )

            user = authenticate(request, phone=f"{''.join(filter(str.isdigit, phone))}", password=password)

            if not user:
                return Response(
                    {
                        "response": False,
                        "message": "Неверный пароль",
                    }
                )

            if user.activated:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "response": True,
                        "message": "",
                        "token": token.key,
                    }
                )
            return Response(
                {
                    "response": False,
                    "message": "Подтвердите номер чтобы войти!",
                    "isactivated": False,
                }
            )

        return Response(serializer.errors)


class ChangePasswordView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data["old_password"]
            password = serializer.data["password"]
            confirm_password = serializer.data["confirm_password"]

            if password != confirm_password:
                return Response({"response": False, "message": "Пароли не совпадают"})

            if not user.check_password(old_password):
                return Response({"response": False, "message": "Вы ввели неправильный пароль"})

            if old_password == password:
                return Response({"response": False, "message": "Новый пароль не должен совпадать со старым."})

            user.set_password(password)
            user.save()

            return Response({"response": True, "message": "Пароль успешно обновлен"})
        return Response(serializer.errors)


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]
            try:
                user = User.objects.get(phone=f"{''.join(filter(lambda x: x.isdigit(), str(phone)))}")
                user.save()

                send_sms(phone, "Подтвердите номер для сброса пароля", user.code)
                return Response({"response": True, "message": "Код подверждение был отправлен на ваш номер"})
            except ObjectDoesNotExist:
                return Response({"response": False, "message": "Пользователь с таким номером не существует"})
        return Response(serializer.errors)
