from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(["POST"])
def send_message(request):
    print(request)
    data = {"message": "Hi"}
    return Response(data, status=status.HTTP_200_OK)
