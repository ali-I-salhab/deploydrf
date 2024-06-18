from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as BaseUserSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['username','email','password','first_name','last_name']

class CurrentUserSerializer(BaseUserSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields=['username','email','password','first_name','last_name']