from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return JsonResponse({"message": "Your account has been deleted successfully."})
