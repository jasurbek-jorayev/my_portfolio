from .models import Profile


def site_settings(request):
    """Make the singleton Profile available to every template as `profile`."""
    return {"profile": Profile.objects.first()}
