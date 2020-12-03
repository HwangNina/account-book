import json
import bcrypt
import jwt_utils
import my_settings
import jwt_utils

from django.http     import JsonResponse
from django.views    import View

from employee.models import Employee

# Create your views here.
class SignUpView(View):

    def post(self, request):
         try:
            data  = json.loads(request.body)

            if Employee.objects.filter(account=data['account']).exists():
                return JsonResponse({"message": "ACCOUNT_EXISTS"}, status=400)

            # password encryption
            password       = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            # insert record
            Employee(
                name = data['name'],
                account = data['account'],
                password = password_crypt,
                is_admin = 0
            ).save()
           
            return JsonResponse({"message": "SIGNUP_SUCCESS"}, status=201)

        except KeyError as e :
            return JsonResponse({'message': f'KEY_ERROR:{e}'}, status=400)

        except ValueError as e:
            return JsonResponse({"message": f"VALUE_ERROR:{e}"}, status=400)


class SignInView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            employee = Employee.objects.get(account = data['account'])

            if bcrypt.checkpw(data['password'].encode('UTF-8'), employee.password.encode('UTF-8')):
                key       = my_settings.SECRET.get('SECRET_KEY')
                algorithm = my_settings.SECRET.get('JWT_ALGORITHM')
                token     = jwt.encode({'employee' : employee.id},key, algorithm = algorithm).decode('UTF-8')
                return JsonResponse({"token": token, "message": "SIGNIN_SUCCESS", "name" : employee.name}, status=200)

            else:
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=401)

        except KeyError as e :
            return JsonResponse({'message': f'KEY_ERROR:{e}'}, status=400)

        except ValueError as e:
            return JsonResponse({"message": f"VALUE_ERROR:{e}"}, status=400)

        except Employee.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=401)