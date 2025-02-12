import os
import django

# Set Django settings module before anything else
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatapp.settings")

# Initialize Django
django.setup()  # Ensure Django is set up before importing other modules

# Now import Django-related modules
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Regular HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
