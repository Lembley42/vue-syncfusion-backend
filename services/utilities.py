from flask import request


def Get_Data(request, expected_keys):
    data = request.get_json()

    if not all(key in data for key in expected_keys):
        return False

    return tuple(data[key] for key in expected_keys)