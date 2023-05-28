def get_description(var, code):
    if var.get(code):
        return var.get(code)
    else:
        return None


def get_key_from_value(d, val):
    return [k for k, v in d.items() if v == val][0]


def get_by_name(var, name):
    return get_key_from_value(var, name)


def replace_options(options_dict, replacement_dict):
    result = {}
    result['options'] = list(map(replacement_dict.get, options_dict['options']))
    return result


