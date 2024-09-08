import requests


class BaseEndpointHandler:
    def __init__(self, **kwargs):
        self.result = {}
        self.path_white_list = kwargs.get('path_white_list', [])
        self.path_black_list = kwargs.get('path_black_list', [])
        self.name_white_list = kwargs.get('name_white_list', [])
        self.name_black_list = kwargs.get('name_black_list', [])
        self.services = kwargs.get('services', {})

        if any(w_point in self.path_black_list for w_point in self.path_white_list):
            raise Exception('Black and white path lists cannot have the same values')
        if any(w_point in self.name_black_list for w_point in self.name_white_list):
            raise Exception('Black and white name lists cannot have the same values')

        self.start()

    def start(self):
        pass


class DjangoEndpointHandler(BaseEndpointHandler):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self):
        from django.urls import get_resolver

        urlpattern = get_resolver().url_patterns

        for i, item in enumerate(urlpattern):
            urls_list = self.get_urls(item)
            if not urls_list:
                continue

            for key, value in urls_list.items():
                self.result[key] = value

    def get_urls(self, item, parent_url=''):
        result = {}

        endpoint = str(item.pattern)

        if hasattr(item, 'url_patterns'):
            for pattern in item.url_patterns:
                urls_list = self.get_urls(pattern, parent_url + endpoint)
                if not urls_list:
                    continue

                for key, value in urls_list.items():
                    if value is None:
                        del result[key]
                    else:
                        result[key] = value
        else:
            while True:
                name = parent_url + endpoint

                if not item.name:
                    print(f'No url patterns found for {name}')
                    break

                if item.name in self.services.keys():
                    response = requests.get(f'{self.services[item.name]}/api/endpoints/')
                    if response.status_code == 401:
                        result[item.name] = None
                        break

                    result[item.name] = response.content
                    break

                if len(self.name_white_list) > 0 and not any(point in item.name for point in self.name_white_list):
                    break
                elif len(self.name_black_list) > 0 and any(point in item.name for point in self.name_black_list):
                    break
                elif len(self.path_white_list) > 0 and not any(name.startswith(point) for point in self.path_white_list):
                    break
                elif len(self.path_black_list) > 0 and any(name.startswith(point) for point in self.path_black_list):
                    break

                result[item.name] = name
                break

        return result


class FastAPIEndpointHandler(BaseEndpointHandler):
    def __init__(self, fastapi_app,  **kwargs):
        super(FastAPIEndpointHandler, self).__init__(**kwargs)
        self.get_urls(fastapi_app.routes)

    def get_urls(self, routes):
        for route in routes:
            name = getattr(route, 'name')
            if not name:
                continue
            self.result[name] = getattr(route, 'path')
