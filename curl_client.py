import json
import pycurl
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class CurlClient:
    def __init__(self, endpoint, body=None):
        self.url = "http://0.0.0.0:8000/"
        self.header = ['Accept: application/json', 'Content-Type: application/json']
        self.endpoint = endpoint
        self.body = body
        self.verbose = False

    def curl_post(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url + self.endpoint)
        curl.setopt(pycurl.HTTPHEADER, self.header)
        curl.setopt(pycurl.POST, 1)

        if self.verbose:
            # depending on whether you want to print details on stdout, uncomment either
            curl.setopt(pycurl.VERBOSE, 1)  # to print entire request flow
        else:
            # or
            curl.setopt(pycurl.WRITEFUNCTION, lambda x: None)  # to keep stdout clean

        # preparing body the way pycurl.READDATA wants it
        body_as_dict = self.body
        body_as_json_string = json.dumps(body_as_dict)  # dict to json
        body_as_file_object = StringIO(body_as_json_string)

        # prepare and send. See also: pycurl.READFUNCTION to pass function instead
        curl.setopt(pycurl.READDATA, body_as_file_object)
        curl.setopt(pycurl.POSTFIELDSIZE, len(body_as_json_string))
        curl.perform()

        # you may want to check HTTP response code, e.g.
        status_code = curl.getinfo(pycurl.RESPONSE_CODE)
        if status_code != 200:
            print(f"Server returned HTTP status code {status_code}")

        # don't forget to release connection when finished
        curl.close()

    def curl_get(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url + self.endpoint)
        curl.setopt(pycurl.HTTPHEADER, self.header)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)

        if self.verbose:
            # depending on whether you want to print details on stdout, uncomment either
            curl.setopt(pycurl.VERBOSE, 1)  # to print entire request flow
        else:
            # or
            curl.setopt(pycurl.WRITEFUNCTION, lambda x: None)  # to keep stdout clean

        curl.perform()

        # you may want to check HTTP response code, e.g.
        status_code = curl.getinfo(pycurl.RESPONSE_CODE)
        if status_code != 200:
            print(f"Server returned HTTP status code {status_code}")

        # don't forget to release connection when finished
        curl.close()

    def curl_patch(self):
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url + self.endpoint)
        curl.setopt(pycurl.HTTPHEADER, self.header)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.CUSTOMREQUEST, 'PATCH')

        if self.verbose:
            # depending on whether you want to print details on stdout, uncomment either
            curl.setopt(pycurl.VERBOSE, 1)  # to print entire request flow
        else:
            # or
            curl.setopt(pycurl.WRITEFUNCTION, lambda x: None)  # to keep stdout clean

        curl.perform()

        # you may want to check HTTP response code, e.g.
        status_code = curl.getinfo(pycurl.RESPONSE_CODE)
        if status_code != 200:
            print(f"Server returned HTTP status code {status_code}")

        # don't forget to release connection when finished
        curl.close()
