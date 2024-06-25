from rest_framework.throttling import SimpleRateThrottle


class IPThrottle(SimpleRateThrottle):   # ip 제한 횟수는 setting 에 있음.
    scope = 'ip'

    def get_cache_key(self, request, view):
        return self.get_ident(request)
