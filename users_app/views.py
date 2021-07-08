from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from users_app.models import User, Room

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
        room = Room(name=request.data["room_name"], private=request.data["private"])
        room.save()
        res = {"success": True, "room_id": room.id}
        return Response(res)


    def get(self, request):

        room_id = request.query_params.get("room_id")
        room_name = request.query_params.get("room_name")
        lst_rooms = []

        if room_id == None and room_name == None:
            rooms_from_db = Room.objects.all()
            for r in rooms_from_db:
                lst_rooms.append({"id": r.id, "room_name": r.name, "private": r.private})

        elif room_id != None:
            rooms_from_db = Room.objects.filter(pk=room_id)
            for r in rooms_from_db:
                lst_rooms.append({"id": r.id, "room_name": r.name, "private": r.private})

        elif room_name != None:
            rooms_from_db = Room.objects.filter(name=room_name)
            for r in rooms_from_db:
                lst_rooms.append({"id": r.id, "room_name": r.name, "private": r.private})

        else:
            return Response({"success": False, "message": "Bad request"})

        return Response({"success": True, "rooms": lst_rooms})



    def delete(self, request):
        room_id = request.data["room_id"]

        if room_id == None:
            return Response({"success": False, "message": "No room_id in request"})

        try:
            room = Room.objects.filter(id=room_id).get()
            room.delete()

        except:
            return Response({"success": False, "message": "Room not found!"})

        return Response({"success": True, "message": "Room is successfully deleted"})


    def put(self, request):
        room_id = request.data["room_id"]
        room_name = request.data["room_name"]
        private = request.data["private"]

        if room_id == None:
            return Response({"success": False, "message": "No room_id in request"})

        try:
            room = Room.objects.filter(id=room_id).get()

            if room_name != None:
                room.name = room_name;

            if private != None:
                room.private = private

            room.save()

        except:
            return Response({"success": False, "message": "Something went wrong!"})

        return Response({"success": True, "message": "Room information updated"})


class AddUsersToRoomAPI(APIView):

    def post(self, request):
        user_id = request.data["user_id"]
        room_id = request.data["room_id"]

        if user_id == None or room_id == None:
            return Response({"success": False, "message": "Invalid request!"})

        try:
            user = User.objects.filter(id = user_id).get()
        except:
            return Response({"success": False, "message": "User doesn't exist!"})

        try:
            room = Room.objects.filter(id = room_id).get()
        except:
            return Response({"success": False, "message": "Room doesn't exist!"})

        try:
            existing_user = room.users.all().filter(id=user_id).get()
        except:
            existing_user = None

        if existing_user != None:
            return Response({"success": True, "message": "User is already added to room!"})

        room.users.add(user)

        return Response({"success": True, "message": "User added to room"})


    def get(self, request):
        user_id = request.query_params.get("user_id")
        room_id = request.query_params.get("room_id")
        user = None
        room = None

        if user_id == None and room_id == None:
            return Response({"success": False, "message": "Invalid request!"})

        if user_id != None:
            try:
                user = User.objects.filter(id = user_id).get()
            except:
                return Response({"success": False, "message": "User doesn't exist!"})

        if room_id != None:
            try:
                room = Room.objects.filter(id = room_id).get()
            except:
                return Response({"success": False, "message": "Room doesn't exist!"})


        if user_id != None and room_id == None:
            ls_rooms = []
            rooms = User.objects.filter(id = user_id).get().room_set.all()
            for r in rooms:
                ls_rooms.append({"room_id": r.id, "room_name": r.name, "private": r.private})

            return Response({"success": True, "rooms": ls_rooms})

        if room_id != None and user_id == None:
            ls_users = []
            users = Room.objects.filter(id = room_id).get().users.all()

            print(type(users))

            for u in users:
                ls_users.append({"user_id": u.id, "user_name": u.user_name})

            return Response({"success": True, "users": ls_users})

        is_member = Room.objects.filter(id = room_id).get().users.filter(id = user_id).exists()

        return Response({"success": True, "is_member": is_member})


    def delete(self, request):
        user_id = request.data["user_id"]
        room_id = request.data["room_id"]
        user = None
        room = None

        if user_id == None or room_id == None:
            return Response({"success": False, "message": "Invalid request!"})

        try:
            user = User.objects.filter(id=user_id).get()
        except:
            return Response({"success": False, "message": "User doesn't exist!"})

        try:
            room = Room.objects.filter(id=room_id).get()
        except:
            return Response({"success": False, "message": "Room doesn't exist!"})

        try:
            if not Room.objects.filter(id = room_id).get().users.filter(id = user_id).exists():
                return Response({"success": True, "message": "User already not in room"})
            user = User.objects.filter(id=user_id).get()
            room = Room.objects.filter(id=room_id).get()
            room.users.remove(user)
        except:
            return Response({"success": False, "message": "Unable to remove user from room!"})

        return Response({"success": True, "message": "User removed from room"})