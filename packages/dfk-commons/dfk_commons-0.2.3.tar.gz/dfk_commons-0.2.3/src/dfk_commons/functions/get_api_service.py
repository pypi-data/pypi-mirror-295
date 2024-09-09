from dfk_commons.classes.APIService import APIService


def get_api_service(url, chain):
    return APIService(url, chain)