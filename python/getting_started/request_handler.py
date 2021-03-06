import json
import requests
import urllib.parse


class RequestHandler(object):
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def __to_canonical_querystring(self, params):
        canonical_querystring = ""
        # parameters have to be sorted alphabetically for the signing part
        for param_key, param_value in sorted(params.items()):
            if canonical_querystring != "":
                canonical_querystring += "&"
            canonical_querystring += param_key + "=" + urllib.parse.quote(param_value)
        return canonical_querystring

    def request(self, path, method="GET", data=None, params={}, api_token=None):
        canonical_querystring = self.__to_canonical_querystring(params)
        data = json.dumps(data) if data else None
        headers = {}

        headers["Accept"] = "application/json"
        headers["Content-type"] = "application/json"
        headers["x-api-key"] = self.api_key

        # All endpoints require the API token, except the API token endpoint.
        if api_token:
            headers["x-dnbapi-jwt"] = api_token

        request_url = self.endpoint + path + "?" + canonical_querystring

        if method == "GET":
            return requests.get(request_url, headers=headers)
        if method == "POST":
            return requests.post(request_url, headers=headers, data=data)
        if method == "PUT":
            return requests.put(request_url, headers=headers, data=data)
        if method == "DELETE":
            return requests.delete(request_url, headers=headers, data=data)
        raise RuntimeError("Unknown method: " + method)
