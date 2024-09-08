import json
import os.path as osp


class MapperOption:
    def __init__(self,
                 path_white_list=None,
                 path_black_list=None,
                 name_white_list=None,
                 name_black_list=None,
                 services=None):
        self.options = {
            'path_white_list': path_white_list if path_white_list else [],
            'path_black_list': path_black_list if path_black_list else [],
            'name_white_list': name_white_list if name_white_list else [],
            'name_black_list': name_black_list if name_black_list else [],
            'services': services if services else {},
        }


class BaseEndpointMapper:
    @staticmethod
    def config() -> MapperOption:
        if osp.exists('emapcfg.json'):
            with open('emapcfg.json', 'r') as fp:
                obj = json.load(fp)
            return MapperOption(
                path_white_list=obj.get('path_white_list'),
                path_black_list=obj.get('path_black_list'),
                name_white_list=obj.get('name_white_list'),
                name_black_list=obj.get('name_black_list'),
                services=obj.get('services')
            )
        else:
            return MapperOption()
