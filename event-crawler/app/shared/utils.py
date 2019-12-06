import requests
from json import dumps as json_dumps
from app.shared.logger import Logger
from config import settings


def site_data(url, method='GET', expected_status=200, output='text', **kwargs):
    """
        Get site data, process and logger the result.
    """
    if output not in ['text', 'json']:
        raise ValueError('Output expect `text` or `json` values')

    if method not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        raise ValueError(f'Method `{method}` is invalid')
    
    if kwargs.get('data', None):
        kwargs['data'] = json_dumps(kwargs['data'])

    headers = kwargs.get('headers', {})
    headers['auth'] = 'true'
    headers['userId'] = settings.USER_ID
    kwargs['headers'] = headers

    method = method.lower()
    try:
        method = getattr(requests, method)
        response = method(url, **kwargs)
        
        status = response.status_code == expected_status
        data = response.text if output == 'text' else response.json

        if not status:
            Logger.error(f'Error URL: `{url}` response status: '+
                         f'{response.status_code} | output: {output} | '+
                         f'data: {data}')

        Logger.info(f'Response ok')
        return status, data
    
    except Exception as err:
        Logger.error(f'Error URL: `{url}` | {err}')
        return False, None
