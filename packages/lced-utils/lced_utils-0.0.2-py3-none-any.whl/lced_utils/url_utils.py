def format_base_url(conn_info):
    return f"{conn_info['host']}:{conn_info['port']}{conn_info['route_prefix']}"
