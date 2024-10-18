import threading

from rr_cfi.settings import BUILD_NUMBER, VERSION

_thread_locals = threading.local()

def getCurrentUser():
    return getattr(_thread_locals, 'user', None)

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.user = request.user
        response = self.get_response(request)
        return response
    
class AddVersionToHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response['X-Version'] = VERSION
        response['X-Build-Number'] = BUILD_NUMBER

        return response