from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.users.models import *
from apps.users.api.serializers import (
    UserSerializer, UserListSerializer, UpdateUserSerializer, 
    PasswordSerializer, GroupSerializer, UserGroupserializer,UserAux, UserGroupAuxserializer, GroupAux
)


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    model = AuthGroup
    serializer_class = GroupSerializer
    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects
        else:
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):
        organismo_serializer = self.get_serializer(
            self.get_queryset(), many=True)
        return Response(organismo_serializer.data, status=status.HTTP_200_OK)


class UserGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    # serializer_class = UserGroupserializer
    serializer_class = UserGroupserializer
    

    def get_queryset(self, pk=None):
        # self.serializer_class = UserGroupAuxserializer
        if pk is None:
            # self.serializer_class = UserGroupserializer
            return self.get_serializer().Meta.model.objects
        else:
            # self.serializer_class = UserGroupAuxserializer
            return self.get_serializer().Meta.model.objects.filter(id=pk).first()

    def list(self, request):       
        
        user_group_serializer = self.get_serializer(
            self.get_queryset(), many=True)
        return Response(user_group_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Relación de usuario y rol creada correctamente!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, pk=None):
        self.serializer_class = UserGroupAuxserializer
        if self.get_queryset(pk):
            user_group_serializer = self.serializer_class(
                self.get_queryset(pk), data=request.data)
            if user_group_serializer.is_valid():
                user_group_serializer.save()
                return Response({'message': 'Relación de usuario y rol actualizada correctamente!'},  status=status.HTTP_200_OK)
            return Response(user_group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No existe la Relación de usuario y rol'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        user_group = self.get_queryset().filter(id=pk).first()
        if user_group:
            user_group.delete()            
            return Response({'message': 'Relación de usuario y rol eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'message': 'No existe la Relación de usuario y rol'}, status=status.HTTP_400_BAD_REQUEST)
    
    


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAdminUser,)
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    user_group_serializer_class = UserGroupserializer
    user_group_aux_serializer_class = UserGroupAuxserializer
    list_aux = UserAux
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects\
                .filter(is_active=True)\
                .values('id', 'username', 'email', 'name','last_name')
        return self.queryset
        

    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            })
        return Response({
            'message': 'Hay errores en la información enviada',
            'errors': password_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
 
    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        user_serializer = self.list_aux(data=request.data)
        # print(user_serializer)
        if user_serializer.is_valid():
            print(user_serializer['username'].value)
            user = {'username': user_serializer['username'].value, 'name': user_serializer['name'].value, 'last_name': user_serializer['last_name'].value,
                    'email': user_serializer['email'].value, 'password': user_serializer['password'].value}
           
            usera_serializer = self.serializer_class(data=user)
            if(usera_serializer.is_valid()):
                usera_serializer.save()
                user_group={
                    'user': usera_serializer['id'].value,
                    'group': user_serializer['group'].value
                }
                user_group_serializer = self.user_group_serializer_class(
                    data=user_group)
                if(user_group_serializer.is_valid()):
                    user_group_serializer.save();
                # id_user = usera_serializer['id'].value
                # id_group = user_serializer['group'].value

            # user_serializer.save()
            # print(user_serializer['id'].value)
            return Response({
                'message': 'Usuario registrado correctamente.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Hay errores en el registro',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UpdateUserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Hay errores en la actualización',
            'errors': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

        # user_serializer = self.list_aux(data=request.data)
        # # print(user_serializer)
        # if user_serializer.is_valid():
        #     # print(user_serializer['username'].value)
        #     user = {'username': user_serializer['username'].value, 'name': user_serializer['name'].value, 'last_name': user_serializer['last_name'].value,
        #             'email': user_serializer['email'].value, 'password': user_serializer['password'].value}
        #     usera_serializer = UpdateUserSerializer(user2, data=user)
        #     if(usera_serializer.is_valid()):
        #         usera_serializer.save()

        #         # print(usera_serializer)
        #         # user_group = UsersUserGroups.objects.filter(user=user2).first()
        #         user_group_serializer = self.user_group_aux_serializer_class(
        #         ).Meta.model.objects.filter(user=user2).first()
        #         # print(user_group.user.id)
        #         # user_group_serializer = self.user_group_aux_serializer_class(
        #         #     data=user_group)
        #         print(user_group_serializer)
        #         if user_group_serializer:
        #             # print(user_group.group)
        #             # print(user_serializer['group'].value)
        #             user_group_serializer.group = user_serializer['group'].value
        #             user_group_serializer.save()
                    
        #             return Response({
        #                 'message': 'Usuario actualizado correctamente.'
        #             }, status=status.HTTP_201_CREATED)
        #         # user_group = {
        #         #     'user': user2,
        #         #     'group': user_serializer['group'].value
        #         # }
        #         # user_group_serializer = self.user_group_serializer_class(
        #         #     data=user_group)
        #         # if(user_group_serializer.is_valid()):
        #         #     user_group_serializer.save()
        #         # id_user = usera_serializer['id'].value
        #         # id_group = user_serializer['group'].value

        #     # user_serializer.save()
        #     # print(user_serializer['id'].value)
            
        # return Response({
        #     'message': 'Hay errores en el registro',
        #     'errors': user_serializer.errors
        # }, status=status.HTTP_400_BAD_REQUEST)

        

       

    def destroy(self, request, pk=None):
        user_destroy = self.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'Usuario eliminado correctamente'
            })
        return Response({
            'message': 'No existe el usuario que desea eliminar'
        }, status=status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['post'])
    def get_grupo(self, request):
        self.serializer_class = UserGroupserializer
        auxiliar = GroupAux(data=request.data)
        if auxiliar.is_valid():
            #    print(auxiliar)
            pk = auxiliar.validated_data['user_id']
            credencial = UsersUserGroups.objects.filter(
                user=pk).first()
            # print(credencial)
            credencial_serializer = self.serializer_class(
                credencial)
            if credencial_serializer:
                # print(credencial)
                return Response(credencial_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def get_user(self, request):
        self.serializer_class = UserSerializer
        auxiliar = UserAux(data=request.data)
        if auxiliar.is_valid():
            #    print(auxiliar)
            pk = auxiliar.validated_data['user']
            credencial = User.objects.filter(
                username=pk).first()
            # print(credencial)
            credencial_serializer = self.serializer_class(
                credencial)
            if credencial_serializer:
                # print(credencial)
                return Response(credencial_serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
