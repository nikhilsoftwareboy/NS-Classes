from django.conf import settings
from announcements.models import Announcement
from courses.models import Course

def site_context(request):
    """Global context available in all templates."""
    unread_announcements_count = 0
    recent_announcements = []
    
    # Safely query if DB tables exist
    try:
        recent_announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')[:5]
        cbse_courses_nav = Course.objects.filter(board='CBSE', is_active=True)[:6]
        bihar_courses_nav = Course.objects.filter(board='BIHAR', is_active=True)[:6]
    except Exception:
        recent_announcements = []
        cbse_courses_nav = []
        bihar_courses_nav = []

    user_role = None
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_role = 'admin'
        else:
            try:
                user_role = request.user.profile.role
            except Exception:
                user_role = 'student'

    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'NS Classes'),
        'SITE_DIRECTOR': getattr(settings, 'SITE_DIRECTOR', 'Nikhil Kumar Singh & Saurabh Raj'),
        'SITE_PHONE': getattr(settings, 'SITE_PHONE', '987654321'),
        'SITE_TAGLINE': getattr(settings, 'SITE_TAGLINE', 'Your Success Begins Here'),
        'recent_announcements_global': recent_announcements,
        'cbse_courses_nav': cbse_courses_nav,
        'bihar_courses_nav': bihar_courses_nav,
        'current_user_role': user_role,
    }
