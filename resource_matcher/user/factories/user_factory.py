from user.serializers.user_serializers import UserSerializer

class UserFactory:
    @staticmethod
    def create_from_request(request_data):
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            return serializer, None
        return None, serializer.errors

    @staticmethod
    def get_serializer(user, many=False):
        return UserSerializer(user, many=many)
