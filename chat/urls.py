# from django.urls import path
# from . import views
# urlpatterns = [
#     # URL form : "/api/messages/1/2"
#     path('messages/<int:sender>/<int:receiver>', views.message_list, name='message-detail'),  # For GET request.
#     # URL form : "/api/messages/"
#     path('messages/', views.message_list, name='message-list'),   # For POST
#     # URL form "/api/users/1"
#     path('users/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
#     path('users/', views.user_list, name='user-list'),    # POST for new user and GET for all users list
# ]


from django.urls import path, re_path
from .views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView,
    MyThreads
)

app_name = 'chat'

urlpatterns = [
    path('', ChatListView.as_view()),
    path('create/', ChatCreateView.as_view()),
    path('<pk>', ChatDetailView.as_view()),
    path("mythreads/", MyThreads.as_view(), name="my_threads"),
    path('<pk>/update/', ChatUpdateView.as_view()),
    path('<pk>/delete/', ChatDeleteView.as_view())
]
