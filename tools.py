import json
import requests


def do_request(url, token, **kwargs):
    """Perform a request to SITE and return response."""

    headers = {"Authorization": "Bearer %s" % token}
    response = requests.get(url, headers=headers, params=kwargs)

    # Raise exception and abort if requests is not successful
    response.raise_for_status()

    try:
        # Try to convert result to JSON
        # abort if not possible
        return response.json()
    except ValueError:
        raise Exception('not a JSON object: {}'.format(response.text))


def send_to_jbrowse(data):
    """Display `data` in the format required by JBrowse.

    """
    return json.dumps(data)


def send_list(data):
    """Display `data` in the format required by Adama.

    :type data: list

    """

    for elt in data:
        print json.dumps(elt)
        print '---'


def send(data):
    """Display `data` in the format required by Adama.

    """
    print json.dumps(data)
    print '---'
