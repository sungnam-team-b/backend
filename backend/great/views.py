from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
import jwt
from .models import Great

def greatview(request):
    return JsonResponse({"id" : "test"})
# Create your views here.

# CRUD 
# https://woolbro.tistory.com/98

def list(request):
    greats = Great.objects.all()
    return JsonResponse({"greats" : "greats"})
    #return JsonResponse({"greats" : greats}) error 발생
    #return render(request, )

###################### 2022-09-13 #########################
#/api/v1/greats/greatslist
#/api/v1/greats/task_status
class greatslistAPI():
    def greatList(self,request):
        greats = Great.objects.filter(

        )
        return 
        

# class TrashImageListAPI(APIView):
#     def get(self, request, user_id, page_number):
#         payload = user_token_to_data(
#             request.headers.get('Authorization', None))
#         if (payload.get('id') == user_id):
#             trashs = trash_image.objects.filter(
#                 user_id=user_id, active=1).order_by('-created_at')
#             paginator = Paginator(trashs, 10)
#             page = page_number
#             try:
#                 contacts = paginator.page(page)
#             except PageNotAnInteger:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             except EmptyPage:
#                 return Response(status=status.HTTP_204_NO_CONTENT)
#             serializer = TrashImageSerializer(contacts, many=True)
#             return Response(serializer.data)
#         else:
#             return JsonResponse({"message": "Invalid_Token"}, status=401)
