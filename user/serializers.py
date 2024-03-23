from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов."},
    )

    class Meta:
        model = User
        fields = [
            "phone",
            'user',
            "first_name",
            "last_name",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        validate_password(password)

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают!")

        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        phone = self.validated_data["phone"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        password = self.validated_data["password"]

        user = User(
            user=user,
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user


class VerifyPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
    )
    code = serializers.IntegerField(
        required=True
    )

    class Meta:
        fields = ["phone", "code"]

    def validate(self, attrs):
        attrs["phone"] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"
        return super().validate(attrs)


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    class Meta:
        fields = ["phone"]

    def validate(self, attrs):
        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
        # min_length=8,
        required=True,
        # error_messages={"min_length": "Не менее 8 символов."},
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs['phone'] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        error_messages={"required": "Это поле обязательно."}
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов.", "required": "Это поле обязательно."}
    )
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов.", "required": "Это поле обязательно."}
    )


class ForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.IntegerField(
        required=True,
        error_messages={"required": "Введите номер телефона."}
    )

    class Meta:
        fields = ["phone"]
