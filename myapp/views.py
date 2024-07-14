from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt , ensure_csrf_cookie
import json
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

# data_store = [
#     {
#         "name": "John Doe",
#         "email": "johndoe@example.com",
#         "message": "Hello, this is a test message to check the form submission."
#     },
#     {
#         "name": "Jane Smith",
#         "email": "janesmith@example.com",
#         "message": "Hi, I am interested in learning more about your services."
#     },
#     {
#         "name": "Alice Johnson",
#         "email": "alicejohnson@example.com",
#         "message": "Good day, I would like to inquire about your pricing."
#     },
    
# ]

@csrf_exempt
def store_data(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            name=data.get('name')
            email=data.get('email')
            message=data.get('message')
            if name and email and message:
                redis_client.rpush('data_store', json.dumps({
                    "name": name,
                    "email": email,
                    "message": message
                }))
                return JsonResponse({"status": "success", "message":"data stored successfully"})
            else:
                return JsonResponse({"status":"fail", "message":"some fields are missing"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status":"error", "message":"Invalid Json"}, status=400)  
    return JsonResponse({"status":"error", "message":"Invalid request method"}, status=405)  


@ensure_csrf_cookie
def fetch_data(request):
    if request.method == 'GET':
        data_store = redis_client.lrange('data_store', 0, -1)
        data_store = [json.loads(item) for item in data_store]
        return JsonResponse({'status': 'success', 'data': data_store})
    return JsonResponse({"status":"error", "message":"Invalid request method"}, status=405)  
        