#!/usr/bin/env python3

import base64
import json

import requests


class Netboot:
    def __init__(self, url, ca=None, cert=None, key=None):
        self.url = url
        self.kwargs = {}
        if ca:
            self.kwargs.update(dict(verify=ca))
        if cert and key:
            self.kwargs.update(dict(cert=(cert, key)))

    def encode_to_base64(self, input_string):
        input_bytes = input_string.encode("utf-8")
        base64_bytes = base64.b64encode(input_bytes)
        base64_string = base64_bytes.decode("utf-8")
        return base64_string

    def parse_response(self, response):
        try:
            out = response.json()
        except json.JSONDecodeError:
            out = response.text.strip()
        return dict(status=response.status_code, result=out)

    def upload_package(self, package_file):
        with open(package_file, "rb") as fp:
            files = dict(uploadFile=(package_file.name, fp, "application/gzip"))
            response = requests.post(self.url + "/tarball/", files=files, **self.kwargs)
        return self.parse_response(response)

    def add(self, mac, os, response_file, package_file=None):
        if package_file:
            upload_result = self.upload_package(package_file)
        else:
            upload_result = None
        config = dict(address=mac, os=os, version="", config=self.encode_to_base64(response_file.read_text()))
        response = requests.put(self.url + "/host/", json=config, **self.kwargs)
        result = self.parse_response(response)
        result["package_upload"] = upload_result
        return result

    def ls(self):
        response = requests.get(self.url + "/hosts/", **self.kwargs)
        return self.parse_response(response)

    def delete_all(self):
        list_result = self.ls()
        macs = list_result["result"]["addresses"]
        results = []
        for mac in macs:
            result = self.delete(mac)
            results.append(result)
        return results

    def delete(self, mac):
        response = requests.delete(self.url + "/host/", json=dict(address=mac), **self.kwargs)
        return self.parse_response(response)
