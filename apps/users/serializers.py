from rest_framework import serializers

from apps.core.utils import generate_unique_key, send_email_job_registration
from apps.users.models import User
from apps.users.validators import check_valid_password


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    password = serializers.CharField(required=False)
    last_name = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = User
        exclude_password = ('password', 'repeat_password',)
        exclude_other_fields = ('is_superuser', 'is_staff', 'groups', 'user_permissions',)
        exclude = exclude_other_fields
        read_only_fields = ('token', 'last_login', 'created', 'modified', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def create(self, validated_data):
        validated_data.pop('repeat_password', None)
        validated_data['password'] = 'temporary_password'
        validated_data['token'] = generate_unique_key(validated_data['email'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.validate(validated_data)
        validated_data.pop('repeat_password', None)
        updated_object = super().update(instance, validated_data)
        if 'password' in validated_data:
            updated_object.set_password(validated_data['password'])
            updated_object.save()

        return updated_object

    def validate(self, data):
        email = data.get('email')
        if email and 'email' in data:
            data['email'] = email.lower()
            data['username'] = data['email']
        if 'email' in data:
            self.check_valid_email(data['email'], self.context['request'].user.pk)
        check_valid_password(data, user=self.context['request'].user)

        return data

    @staticmethod
    def check_valid_email(value, pk):
        old_user = User.objects.get(pk=pk)
        if User.objects.filter(email=value).exists() and old_user.email != value:
            raise serializers.ValidationError({'email': ['This email address has already exist.']})

        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    @staticmethod
    def send_mail(validated_data):
        user = User.objects.get(email=validated_data['email'])
        user.reset_key = generate_unique_key(user.email)

        send_email_job_registration(
            'Car.am',
            user.email,
            'reset_password',
            {
                'reset_key': user.reset_key,
                'name': user.username
            },
            'Reset your password',
        )
        user.save()

    def validate(self, data):
        self.check_email(data['email'])
        return data

    @staticmethod
    def check_email(value):
        user = User.objects.filter(email=value)

        if not user.exists():
            raise serializers.ValidationError('This email address does not exist.')

        if not user.filter(is_active=True).exists():
            raise serializers.ValidationError('Your account is inactive.')

        return value


class ConfirmAccountSerializer(serializers.Serializer):
    token = serializers.CharField()

    @staticmethod
    def confirm(validated_data):
        user = User.objects.get(email_confirmation_token=validated_data['token'])
        user.is_active = True
        user.email_confirmation_token = None
        user.save()

    def validate(self, data):
        if not User.objects.filter(email_confirmation_token=data['token']).exists():
            raise serializers.ValidationError('Invalid token.')

        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def change_password(self, validated_data):
        self.validate(validated_data)
        user = User.objects.get(pk=self.context['id'])
        user.set_password(validated_data['password'])
        user.save()

    def validate(self, data):
        error = check_valid_password(data)
        if error:
            raise serializers.ValidationError({'password': error})
        return data
