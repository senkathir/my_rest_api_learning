from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets#another way of dealing with api operations
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
#from rest_framework.permissions import IsAuthenticatedOrReadOnly #non authenticated users i.e read only users can also view the content
from rest_framework.permissions import IsAuthenticated#only authenticated users can view the content

from profiles_api import models
from profiles_api import permissions
from profiles_api import serializers
# Create your views here.

class HelloApiView(APIView):
    """Test api view for practise"""

    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):#req takes all the data that is being passed to this api while firing it
        """Get http request method"""
        an_apiview = [
        'Is similar to Django view',
        'Is mapped manually to URLs',
        'get,post,patch,put,delete',
        ]

        return Response({'message':'First API','an_apiview':an_apiview})

    def post(self,request):
        """post method for api"""

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST#by default, reponse wil be 200 OK, thats y we are changing it to 400
            )

    def put(self, request, pk=None):
        """put request where pk is id with which only we are gonna update i.e replace existing data with input data"""
        return Response({'method':'PUT'})

    def patch(self, request, pk=None):
        """patch request where pk is id with which only we are gonna update only the field that is given as input"""
        return Response({'method':'Patch'})

    def delete(self, request, pk=None):
        """Delete request where pk is id with which only we are gonna delete"""
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """test the actions in viewset"""

    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """List viewset which is like GET"""
        list_viewset = [
            'list,update,create,Retreive,partial_update are the actions',
            'used for basic api operations with db'
        ]

        return Response({'message':'Hello','list_viewset':list_viewset})

    def create(self,request):
        """create viewset"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST#by default, reponse wil be 200 OK, thats y we are changing it to 400
            )

    def retreive(self,request,pk=None):
        """handles getting an object by its id"""
        return Response({'method':'GET'})

    def partial_update(self,request,pk=None):
        """updates only a part of object"""
        return Response({'http_method':'PATCH'})

    def update(self,request,pk=None):
        """updates an object"""
        return Response({'http_method':'PUT'})

    def destroy(self,request,pk=None):
        """removes the object"""
        return Response({'http_method':'DELETE'})

class UserLoginApiView(ObtainAuthToken):
    """handle creating user authentication tokens i.e creates tokens which can be used in all api for authentication"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES#to make this api available in admin for testing.by default, obtainauthtoken will not be available for testing. now this app_settings will be used to override and make it available for testing



class UserProfileViewSet(viewsets.ModelViewSet):#we can pass the query set to model viewset so it knows which objects in db is gonna be managed through this viewset
    """create and update profiles with modelsand connected to model serializer class"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)#comma to make it as a tuple
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)#for searching a profile with specific fields
    search_fields = ('name','email',)



class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Creating, reading and updating profilefeed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
#        IsAuthenticatedOrReadOnly
    )

    def perform_create(self,serializer):
        """sets the userprofile to logged-in user"""
        """Whenever http req is made to viewset for creating user, models will call serializer
        and it will use its default create function. perform_create will override this
        functionality. this serializer will now use its serializer in model but with
        user_profile will be user in incoming http request.since we have tokenauth,
        request will have user details. only user who is authenticated will be able
        add feeditems, otherwise, feeditems will be anonymous"""

        serializer.save(user_profile=self.request.user)
