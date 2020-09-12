from rest_framework import serializers

from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """serializes a basic field for testing"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """serializes a user profile object(model)"""

    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password')
        extra_kwargs = {
            'password':{
                'write_only': True,#pwd field will not be retreived/displayed for http methods other than create
                'style':{'input_type':'password'}#passwd will not be visible instead it will be dots
            }
        }

    def create(self, validated_data):#this is the default method for creating user and it will pass cleartxt pwd in fields as mentioned above. we ll override it by calling create_user from models
        """create and return user to override create_user in models"""#this is done for replacing clear text pwd with hashed pwd
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes profile feed items"""

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')#id ll be created by django(pk) and created_on is set to automatic time. only user_profile and status_text will be writable fields
        extra_kwargs = {'user_profile':{'read_only':True}}
