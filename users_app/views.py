from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users_app.models import User

class UserAPI(APIView):

    def post(self, request):
        user = User(user_name=request.data["user_name"], password=request.data["password"])
        user.save()
        res = {"success": True, "user_id": user.id}
        return Response(res)

    def get(self, request):

        user_id = request.query_params.get("user_id")
        user_name = request.query_params.get("user_name")
        lst_users = []

        if user_id == None and user_name == None:
            users_from_db = User.objects.all()
            for u in users_from_db:
                lst_users.append({"id": u.id, "user_name": u.user_name})

        elif user_id != None:
            users_from_db = User.objects.filter(pk=user_id)
            for u in users_from_db:
                lst_users.append({"id": u.id, "user_name": u.user_name})

        elif user_name != None:
            users_from_db = User.objects.filter(user_name=user_name)
            for u in users_from_db:
                lst_users.append({"id": u.id, "user_name": u.user_name})

        else:
            return Response({"success": False, "message": "Invalid response"})

        return Response({"success": True, "users": lst_users})

    def delete(self, request):
        user_id = request.data["user_id"]

        if user_id == None:
            return Response({"success": False, "message": "No user_id in request"})

        try:
            user = User.objects.filter(id=user_id).get()
            user.delete()

        except:
            return Response({"success": False, "message": "User not found!"})

        return Response({"success": True, "message": "User is successfully deleted"})

    def put(self, request):
        user_id = request.data["user_id"]
        user_name = request.data["user_name"]
        user_password = request.data["user_password"]

        if user_id == None:
            return Response({"success": False, "message": "No user_id in request"})

        try:
            user = User.objects.filter(id=user_id).get()

            if user_name != None:
                user.user_name = user_name;

            if user_password != None:
                user.password = user_password

            user.save()

        except:
            return Response({"success": False, "message": "Something went wrong!"})

        return Response({"success": True, "message": "User information updated"})


class RoomAPI(APIView):

    def post(self, request):
        pass

    def get(self, request):
        pass

    def delete(self, request):
        pass

    def put(self, request):
        pass

class SuperUsersAPI(APIView):

    def post(self, request):
        pass

    def get(self, request):
        pass

    def delete(self, request):
        pass

    def put(self, request):
        pass