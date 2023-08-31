class HostHeaderCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем значение Host из заголовка
        request_host = request.META.get('HTTP_HOST', '')

        # Получаем ожидаемое значение Host из настроек
        expected_host = 'riseua.online'  # Замените на ваше ожидаемое значение

        # Проверяем, соответствует ли Host ожидаемому значению
        if request_host != expected_host:
            print(f"""
                  -- Strange host header! --
                  Expected: {expected_host},
                  Got: {request_host}
                  IP: {request.META.get('REMOTE_ADDR')},
                  User-Agent: {request.META.get('HTTP_USER_AGENT')}
                  """)
        
        response = self.get_response(request)
        return response