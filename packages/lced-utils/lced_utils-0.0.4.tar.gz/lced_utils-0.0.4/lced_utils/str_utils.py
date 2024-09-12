def to_camel_case(snake_str, is_pascal=False):
    components = snake_str.split("_")
    if is_pascal:
        return "".join(x.capitalize() for x in components)
    else:
        return components[0] + "".join(x.capitalize() for x in components[1:])


def convert_to_upper_snake_case(input_str):
    cleaned_str = input_str.replace("-", "_")
    upper_snake_case = cleaned_str.upper()
    return upper_snake_case
