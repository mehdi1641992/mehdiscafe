from .utils import get_system_matrix_data
from django.conf import settings

def system_matrix(request):
    """
    Makes the weather, date, and TMDB key available 
    to every template on the site.
    """
    return {
        'matrix': get_system_matrix_data(),
        'tmdb_key': getattr(settings, 'TMDB_API_KEY', '')
    }