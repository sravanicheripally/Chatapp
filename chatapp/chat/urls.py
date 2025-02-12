from django.urls import path
from .views import signup_view, login_view, chat_view,home,user_list_view,send_message,get_notifications,mark_notifications_read    
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chat', user_list_view, name='user_list_view'),
    path('users', chat_view, name='chat'),
    path('', home, name='home'),  
    path('chat/<str:receiver_username>/', chat_view, name='chat_with_user'),
    path("send_message/", send_message, name="send_message"),
    path("get_notifications/", get_notifications, name="get_notifications"),
    path("mark_notifications_read/", mark_notifications_read, name="mark_notifications_read"),
]
