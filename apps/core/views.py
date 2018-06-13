from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from apps.core.serializers import SendContactUsEmailSerializer
from apps.core.utils import return_http_error


class SendContactUsEmailAPIView(APIView):
    serializer_class = SendContactUsEmailSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        """
        ---
        request_serializer: ForgotPasswordSerializer
        """

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.send_mail(serializer.data)
            return JsonResponse(
                {
                    'result': 'success',
                },
                status=status.HTTP_200_OK,
            )

        return return_http_error(serializer.errors, status.HTTP_400_BAD_REQUEST)
