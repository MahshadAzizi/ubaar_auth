from django.core.cache import cache


class ThrottleService:
    MAX_ATTEMPTS = 3
    BLOCK_DURATION = 60 * 60

    @classmethod
    def _key(cls, scope: str, target: str) -> str:
        """
        Generate a unique cache key based on scope and target (ip or phone).
        """
        return f'{scope}_fail:{target}'

    @classmethod
    def increment(cls, scope: str, ip: str = None, phone: str = None):
        """
        Increment failure count for given IP and/or phone number under a specific scope.
        """
        if ip:
            ip_key = cls._key(scope, f'ip:{ip}')
            cache.set(ip_key, cache.get(ip_key, 0) + 1, timeout=cls.BLOCK_DURATION)

        if phone:
            phone_key = cls._key(scope, f'phone:{phone}')
            cache.set(phone_key, cache.get(phone_key, 0) + 1, timeout=cls.BLOCK_DURATION)

    @classmethod
    def reset(cls, scope: str, ip: str = None, phone: str = None):
        """
        Reset failure count for given IP and/or phone number under a specific scope.
        """
        if ip:
            cache.delete(cls._key(scope, f'ip:{ip}'))
        if phone:
            cache.delete(cls._key(scope, f'phone:{phone}'))

    @classmethod
    def is_blocked(cls, scope: str, ip: str = None, phone: str = None) -> bool:
        """
        Check if given IP or phone number is blocked under a specific scope.
        """
        ip_attempts = cache.get(cls._key(scope, f'ip:{ip}')) if ip else 0
        phone_attempts = cache.get(cls._key(scope, f'phone:{phone}')) if phone else 0

        return (ip_attempts or 0) >= cls.MAX_ATTEMPTS or (phone_attempts or 0) >= cls.MAX_ATTEMPTS
