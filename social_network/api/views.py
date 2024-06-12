from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from rest_framework import permissions
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination



# User signup
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User login
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email__iexact=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    

# Setting pagination 
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
  
  
# Searching user  
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        return User.objects.filter(Q(email__iexact=search_query) | Q(username__icontains=search_query))


# Sending friend request
class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        to_user = User.objects.get(id=self.request.data['to_user'])
        if self.request.user == to_user:
            raise ValidationError("You cannot send a friend request to yourself.")
        
        if FriendRequest.objects.filter(from_user=self.request.user, to_user=to_user, status='pending').exists():
            raise ValidationError("Friend request already sent.")
        
        serializer.save(from_user=self.request.user, to_user=to_user)
        

# Responding the request
class RespondFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')

    def perform_update(self, serializer):
        status = self.request.data.get('status')
        if status not in ['accepted', 'rejected']:
            raise ValidationError("Invalid status")
        serializer.save(status=status)
        

# Listing friends
class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = FriendRequest.objects.filter(
            Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
        ).values_list('from_user_id', 'to_user_id')
        
        # Extract the friend IDs and exclude the current user
        friends_ids = set()
        for from_user_id, to_user_id in friends:
            if from_user_id != user.id:
                friends_ids.add(from_user_id)
            if to_user_id != user.id:
                friends_ids.add(to_user_id)

        return User.objects.filter(id__in=friends_ids)


# Listing pending requests
class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')
    
