from rest_framework import viewsets, status, generics, mixins
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError, NotFound
from account.api.serializers import *
from drf_spectacular.utils import extend_schema, extend_schema_view
from account.permissons import IsAdminUserRole
from rest_framework.permissions import IsAuthenticated









class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @extend_schema(
        summary="User Login",
        description="Authenticate user and return JWT tokens",
        tags=["Authentication"]
    )

    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        access_token = refresh.access_token

        access_token['name'] = user.name
        access_token['surname'] = user.surname
        access_token['email'] = user.email


        role = user.role

        if not role or role not in ['admin', 'staff', 'driver', 'rider']:
            return Response(
                {"detail": f"Invalid role: User must have a valid role (admin, staff, driver, or rider)."},
                status=400
            )

        access_token['role'] = role

        
        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
        })













class RegistrationViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    A ViewSet for handling user registration and CRUD operations.
    """
    permission_classes = [IsAuthenticated,IsAdminUserRole]
    queryset = User.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        """Return the appropriate serializer based on the action."""
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserUpdateSerializer

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
    )
    def create(self, request, role=None, *args, **kwargs):
        """Create a user with the specified role."""
        if role not in ['rider', 'driver']:
            raise ValidationError({"role": "Invalid role. Must be 'rider' or 'driver'."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(role=role)
        return Response(UserUpdateSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update user details with partial updates."""
        kwargs['partial'] = True  # Enable PATCH-like partial updates
        return super().update(request, *args, **kwargs)

    def get_user(self, pk):
        """Helper method to get a user by ID or raise 404."""
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail=f"User with ID {pk} not found.")

@extend_schema_view(
    create=extend_schema(
        summary="Register a Rider",
        description="Create a new rider user account.",
        tags=["Authentication"],
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
    )
)
class RiderRegistrationViewSet(RegistrationViewSet):
    """ViewSet for creating Rider accounts."""
    
    def get_queryset(self):
        """Filter the queryset to return only riders."""
        return User.objects.filter(role='rider')

    def create(self, request, *args, **kwargs):
        """Create a Rider."""
        return super().create(request, role='rider', *args, **kwargs)


@extend_schema_view(
    create=extend_schema(
        summary="Register a Driver",
        description="Create a new driver user account.",
        tags=["Authentication"],
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
    )
)
class DriverRegistrationViewSet(RegistrationViewSet):
    """ViewSet for creating Driver accounts."""
    def get_queryset(self):
        """Filter the queryset to return only drivers."""
        return User.objects.filter(role='driver')

    def create(self, request, *args, **kwargs):
        """Create a Driver."""
        return super().create(request, role='driver', *args, **kwargs)