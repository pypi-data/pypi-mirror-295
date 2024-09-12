import os
from lced_utils.str_utils import convert_to_upper_snake_case
from lced_variables.dict_var import (
    RouterSingletonDict,
    ConfigSingletonDict,
    ConnectSingletonDict,
)


def set_config_info(config_info):
    project_name = os.path.basename(config_info["PROJECT_ROOT_PATH"])
    upper_project_name = convert_to_upper_snake_case(project_name)
    ConfigSingletonDict().update(config_info)
    if upper_project_name in ConfigSingletonDict():
        ConfigSingletonDict()["PROJECT"] = ConfigSingletonDict().pop(upper_project_name)


def get_project_bind():
    return ConfigSingletonDict().get("PROJECT", {}).get("BIND", {})


def get_project_logging():
    return ConfigSingletonDict().get("PROJECT", {}).get("LOGGING", {})


def get_project_connect():
    return ConfigSingletonDict().get("PROJECT", {}).get("CONNECT", {})


def get_project_service():
    return ConfigSingletonDict().get("PROJECT", {}).get("SERVICE", {})


def get_project_root_path():
    return ConfigSingletonDict().get("PROJECT_ROOT_PATH")


def get_project_env():
    return ConfigSingletonDict().get("PROJECT_ENV")


def get_edge_device_id():
    return ConfigSingletonDict().get("EDGE_DEVICE", {}).get("ID")


def get_battery_device_id():
    return ConfigSingletonDict().get("BATTERY_DEVICE", {}).get("ID")


def get_battery_device_metadata():
    return ConfigSingletonDict().get("BATTERY_DEVICE", {}).get("METADATA", {})


def iter_set_connect_info(connect_name, info):
    ConnectSingletonDict().setdefault(connect_name, {}).update(info)


def get_connect_info():
    return ConnectSingletonDict()


def iter_set_register_route_info(info):
    RouterSingletonDict().setdefault("register_route", []).append(info)


def iter_set_dynamic_methods_info(info):
    RouterSingletonDict().setdefault("dynamic_methods", []).append(info)


def iter_set_handler_mapping_info(info):
    RouterSingletonDict().setdefault("handler_mapping", []).append(info)


def get_register_route_info():
    return RouterSingletonDict().get("register_route", [])


def get_dynamic_methods_info():
    return RouterSingletonDict().get("dynamic_methods", [])


def get_handler_mapping_info():
    return RouterSingletonDict().get("handler_mapping", [])
