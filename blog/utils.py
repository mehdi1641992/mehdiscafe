from .models import SystemStatus

def get_system_matrix_data():
    # We only need to fetch the Mood from the Admin panel
    config = SystemStatus.objects.first()
    return {
        'sys_mood': config.active_mood if config else "clear"
    }