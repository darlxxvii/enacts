from django.shortcuts import render
from .models import User
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def user_list(request):
    if request.method == "GET":
        users = User.objects.all()
        data = [
            {"id": u.id, "name": u.name, "email": u.email, "created_at": u.created_at.isoformat()}
            for u in users
        ]
        return JsonResponse(data, safe=False, status=200)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get("name")
            email = data.get("email")

            if not name or not email:
                return JsonResponse({"error": "Name and email are required"}, status=400)
            
            user = User.objects.create(name=name, email=email)

            return JsonResponse(
                {"id": user.id, "name": user.name, "email": user.email,"created_at": user.created_at.isoformat()},
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
    if request.method == 'GET':
        return JsonResponse(
            {"id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()},
            status=200
        )
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            user.name = data.get("name")
            user.email = data.get("email")
            user.save()
            return JsonResponse(
                {"id": user.id, "name": user.name, "email": user.email, "created_at": user.created_at.isoformat()},
                status=200
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "DELETE":
        user.delete()
        return JsonResponse({'message': "User deleted"}, status=204)
    
    return JsonResponse({"error": "method not allowed"}, status=405)