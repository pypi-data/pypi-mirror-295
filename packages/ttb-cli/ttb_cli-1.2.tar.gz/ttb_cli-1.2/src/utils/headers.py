def prepare_headers(headers):
    if 'Cookie' in headers:
        cookie_value = headers.pop('Cookie')
        cookies_header = f'Cookie: {cookie_value}'
        return cookies_header, headers

    return None, headers