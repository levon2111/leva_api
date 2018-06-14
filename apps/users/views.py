from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.core.utils import return_http_error, send_email_job_registration, generate_unique_key
from apps.users.models import User, Syndicate, InvitedToSyndicate
from apps.users.serializers import ForgotPasswordSerializer, ConfirmAccountSerializer, UserSerializer, \
    ChangePasswordSerializer, SyndicateCreateSerializer, SyndicateGetSerializer, EmailSerializer


class Login(ObtainAuthToken):
    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        if not serializer.is_valid():
            return return_http_error(serializer.errors, status.HTTP_412_PRECONDITION_FAILED)
        user = serializer.validated_data['user']

        if user.is_active is False:
            return return_http_error({'error': 'please enter a valid data'}, status.HTTP_412_PRECONDITION_FAILED)
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'token': token.key,
        })


class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.send_mail(serializer.data)
            return JsonResponse(
                {
                    'result': 'success',
                },
                status=status.HTTP_200_OK,
            )
        if serializer.errors and "non_field_errors" in serializer.errors:
            return return_http_error({"email": serializer.errors['non_field_errors'][0]}, status.HTTP_400_BAD_REQUEST)
        return return_http_error(serializer.errors, status.HTTP_400_BAD_REQUEST)


class ConfirmAccountAPIView(APIView):
    serializer_class = ConfirmAccountSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        """
        ---
        request_serializer: ConfirmAccountSerializer
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.confirm(serializer.data)
            return JsonResponse(
                {
                    'result': 'success',
                },
                status=status.HTTP_200_OK,
            )

        return return_http_error(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-updated_at')
    serializer_class = UserSerializer
    http_method_names = ['get', 'delete', 'put', 'patch', ]
    permission_classes = [IsAuthenticated]
    search_fields = ('first_name', 'last_name', 'email', 'id',)
    renderer_classes = tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    exclude_report_fields = ('password', 'last_login',)

    def get_object(self, queryset=None):
        return self.request.user

    @action(methods=['patch'], detail=True, serializer_class=ChangePasswordSerializer)
    def password(self, request, pk=None):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {
                        'code': status.HTTP_400_BAD_REQUEST,
                        'detail': 'Wrong password.',
                        'developer_message': 'old_password Wrong password.',
                        'errors': 'ERROR',
                        'status': 'BAD_REQUEST',
                        'timestamp': timezone.now(),
                        'title': 'Error for Patch password',
                    }
                )
            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)

        return Response(
            {
                'code': status.HTTP_404_NOT_FOUND,
                'detail': 'Wrong password.',
                'developer_message': 'user not found',
                'errors': 'ERROR',
                'status': 'NOT_FOUND',
                'timestamp': timezone.now(),
                'title': 'Error for Patch password',
            }
        )


class SyndicateViewSet(ModelViewSet):
    def get_queryset(self):
        return Syndicate.objects.all()

    queryset = Syndicate.objects.all()
    serializer_class = SyndicateCreateSerializer
    http_method_names = ('post',)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated],
            serializer_class=SyndicateCreateSerializer)
    def create_syndicate(self, request):
        members_to_invite = request.data['members_to_invite']
        request.data.pop('members_to_invite')
        syndicate_data = SyndicateCreateSerializer(data=request.data)

        if syndicate_data.is_valid():
            syndicate_data = syndicate_data.save()
            print(syndicate_data)
            for member in members_to_invite:
                valid_email = EmailSerializer(data=member)
                if valid_email.is_valid():
                    token = generate_unique_key(member['email'])
                    inv = InvitedToSyndicate(token=token, syndicate=syndicate_data)
                    inv.save()
                    send_email_job_registration(
                        'Leva.com',
                        member['email'],
                        'invite_member',
                        {
                            'token': token
                        },
                        'Member invite',
                    )
                else:
                    return return_http_error(valid_email.errors, status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED, data=SyndicateGetSerializer(syndicate_data).data)
        else:
            return return_http_error(syndicate_data.errors, status.HTTP_400_BAD_REQUEST)
