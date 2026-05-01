from rest_framework.decorators import api_view
from rest_framework. views import APIView
from rest_framework.response import Response
from myapp.services.rate_limiter import is_allowed
from worker.tasks import send_email_task
from rest_framework import status
from .. serializers import *
from ..  models import *


@api_view(['GET'])
def limited_view(request):
    user = request.META.get('REMOTE_ADDR')

    if not is_allowed(user):
        return Response(
            {"error": "Rate limit exceeded"},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    return Response({
        "status": True,
        "message": "Success"})


class SendMail(APIView):
 def post(self, request):
    serializer = UserSerializer(data=request.data)
    

    if not serializer.is_valid():
        return Response(
            {
                "status": False,
                "errors": serializer.errors  
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    data = serializer.validated_data

    try:
        email_ids = []
        
        for email in data['email']:
            email_obj = User.objects.create(
                email=email,
                subject=data['subject'],
                body=data['body'],
            )

            send_email_task.delay(
                email_obj.id,
                email,
                data['subject'],
                data['body'],
                data['sender_name']   

            )

            email_ids.append(email_obj.id)

        return Response(
            {
                "status": True,
                "message": "Emails stored & queued successfully",
                "email_ids": email_ids
            },
            
            status=status.HTTP_200_OK
        )
    
            
    except Exception as e:
        return Response(
            {
                "status": False,
                "message": "Failed to queue email",
                "error": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
  
  
  
  
  
  
  
  
  
  
  
  
  
  
            
# class SendMail(APIView):
#     permission_classes = []

#     def post(self, request):
#         emails = request.data.get("email")
#         subject = request.data.get("subject")
#         body = request.data.get("body")

#         if not emails or not subject or not body:
#             return Response(
#                 {
#                     "status": False,
#                     "message": "email, subject, and body are required"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )



#         for e in emails:
#             send_email_task.delay(e, subject, body)

#         return Response({
#             "status": True,
#             "message": "Emails queued successfully",
#             "total": len(emails)
#         })

