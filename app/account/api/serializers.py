from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password




User = get_user_model()



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        user = authenticate(**data)

        if user is None:
            raise serializers.ValidationError({'error': 'Invalid credentials'})

        if not user.is_active:
            raise serializers.ValidationError({'error': 'Account not activated', 'activation_required': True})
        

        return user
    




class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("id", "name", "phone_number", "surname", "email", "password", "password2", "role")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use!")

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords did not match!")

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user
    



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "surname"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance