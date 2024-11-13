from django.urls import get_resolver


def available_urls(request):
    return {'urls': [name for name in get_resolver().reverse_dict]}
