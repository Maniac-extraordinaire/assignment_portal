from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from .models import User, Assignment
from django.views import View
# Create your views here.

class RegisterView(View):
    def post(self, request):
        try:
            data = request.POST
            username = data.get('username')
            password = data.get('password')
            is_admin = data.get('is_admin', False).lower() == 'true'  # Setting the Defaults to False (User)

            # Validating input
            if not username or not password:
                return JsonResponse({'error': 'Username and Password are required'}, status=400)

            if len(password) < 6:
                return JsonResponse({'error': 'Password must be at least 6 characters long'}, status=400)

            if User.objects(username=username):
                return JsonResponse({'error': 'Username already exists'}, status=400)

            hashed_password = make_password(password)
            User(username=username, password=hashed_password, is_admin=is_admin).save()

            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            # Logging the error
            print(f"Error in RegisterView: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    
class LoginView(View):
    def post(self, request):
        try:
            data = request.POST
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'error': 'Username and Password are required'}, status=400)

            user = User.objects(username=username).first()
            if not user:
                return JsonResponse({'error': 'User not found'}, status=404)

            if not check_password(password, user.password):
                return JsonResponse({'error': 'Incorrect password'}, status=401)

            return JsonResponse({'message': f'Welcome {user.username}', 'is_admin': user.is_admin}, status=200)
        except Exception as e:
            # Logging the error
            print(f"Error in LoginView: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    
class UploadAssignmentView(View):
    def post(self, request):
        try:
            data = request.POST
            username = data.get('username')
            task = data.get('task')
            admin_name = data.get('admin')

            # Validating input
            if not username or not task or not admin_name:
                return JsonResponse({'error': 'Username, task, and admin are required'}, status=400)

            user = User.objects(username=username).first()
            admin = User.objects(username=admin_name, is_admin=True).first()

            if not user:
                return JsonResponse({'error': f'User {username} not found'}, status=404)
            if not admin:
                return JsonResponse({'error': f'Admin {admin_name} not found'}, status=404)

            Assignment(user=user, task=task, admin=admin).save()
            return JsonResponse({'message': 'Assignment uploaded successfully'}, status=201)
        except Exception as e:
            # Logging the error
            print(f"Error in UploadAssignmentView: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    
class AdminListView(View):
    def get(self, request):
        admins = User.objects(is_admin=True)
        admin_list = [{'username': admin.username} for admin in admins]
        return JsonResponse({'admins': admin_list})
    
class AdminAssignmentsView(View):
    def get(self, request):
        try:
            admin_name = request.GET.get('admin')
            if not admin_name:
                return JsonResponse({'error': 'Admin name is required'}, status=400)

            admin = User.objects(username=admin_name, is_admin=True).first()
            if not admin:
                return JsonResponse({'error': f'Admin {admin_name} not found'}, status=404)

            assignments = Assignment.objects(admin=admin)
            if not assignments:
                return JsonResponse({'message': 'No assignments found for this admin'}, status=200)

            assignment_list = [
                {
                    'id': str(assignment.id),
                    'user': assignment.user.username,
                    'task': assignment.task,
                    'status': assignment.status,
                    'timestamp': assignment.timestamp
                }
                for assignment in assignments
            ]

            return JsonResponse({'assignments': assignment_list}, status=200)
        except Exception as e:
            # Logging the error
            print(f"Error in AdminAssignmentsView: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    
class UpdateAssignmentStatusView(View):
    def post(self, request, id):
        try:
            status = request.POST.get('status')  # Expecting "Accepted" or "Rejected"
            if not status:
                return JsonResponse({'error': 'Status is required'}, status=400)

            if status not in ['Accepted', 'Rejected']:
                return JsonResponse({'error': 'Status must be either Accepted or Rejected'}, status=400)

            assignment = Assignment.objects(id=id).first()
            if not assignment:
                return JsonResponse({'error': 'Assignment not found'}, status=404)

            assignment.status = status
            assignment.save()
            return JsonResponse({'message': f'Assignment {status.lower()} successfully'}, status=200)
        except Exception as e:
            # Logging the error
            print(f"Error in UpdateAssignmentStatusView: {e}")
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
