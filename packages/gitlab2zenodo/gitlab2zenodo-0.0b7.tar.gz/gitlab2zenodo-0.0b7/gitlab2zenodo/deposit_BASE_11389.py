#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import re
from pathlib import Path

import requests

from gitlab2zenodo.settings import Settings


class ZenodoDeposit(object):
    def __init__(self, token=None, sandbox=True):
        self.params = {}
        if token is not None:
            self.params['access_token'] = token
        sandbox_api = "https://sandbox.zenodo.org/api/deposit/depositions"
        normal_api = "https://zenodo.org/api/deposit/depositions"
        self.zenodo_url = sandbox_api if sandbox else normal_api
        self.deposit = None
        self.deposition_id = None
        self.headers = {"Content-Type": "application/json"}
        self.links = {}

    def _latest_id(self):
        if not self.links:
            return self.deposit["id"]
        if "latest_draft" in self.links:
            # grab the last unpublished version
            link = self.links["latest_draft"]
        else:
            link = self.links["latest"]
        return Path(link).name

    def _request(self, method, path, full_path=False, **kwargs):
        """Interface to `requests.request()` which consistently returns a dict

        Args:
            method : str
                The HTTP method. Can be one of 'GET', 'PUT', 'POST', and 'DELETE'
            path : str
                The path to the API object or action, like record, file or new version
            full_path : bool, optional
                Is the given path the full path to the object, by default False

                If false, the path is corrected based on the base URL stored in the deposit object.
            kwargs
                Additional arguments passed to `requests.request()`

        Returns:
            dict
                The API response

        Raises:
           requests.HTTPError
                If the response from the server is outside the 200-range
        """
        if not full_path:
            path = self.zenodo_url + path

        r = requests.request(method, path,
                             params=self.params,
                             **kwargs)

        infos = {}
        try:
            infos = r.json()
        except:
            try:
                r.raise_for_status()
            except Exception as e:
                errors = infos.get("errors", [])
                extra_message = "".join([err["field"] + ": " + err["message"] for err in errors])
                extra_message += "\n\tThis error occured while sending metadata:\n\t" + str(kwargs)
                raise requests.RequestException(extra_message) from e
        if not r.ok:
            details = f"\n\nOccured while sending {method} to {path}"
            raise requests.RequestException(", ".join([f"{k}: {v}" for k, v in r.json().items()])+details)

        return infos

    def get_deposit(self, id):
        logging.info("get deposit")
        r = self._request("GET", "/" + id)
        self.deposition_id = str(r['id'])
        self.links = r["links"]
        self.deposit = r
        return r

    def new_deposit(self):
        logging.info("new deposit")
        r = self._request("POST", "", json={})  # , headers=self.headers)
        self.deposit = r
        self.deposition_id = str(r['id'])
        self.links = r["links"]
        return r

    def upload(self, path):
        logging.info("upload file")
        with path.open("rb") as fp:
            r = self._request(
                "PUT", self.links["bucket"] + "/" + path.name, full_path=True, data=fp)
        return r

    def upload_metadata(self, metadata):
        logging.info("upload metadata")
        r = self._request("PUT", "/" + self._latest_id(),
                          data=json.dumps(metadata), headers=self.headers)
        if "links" in r:
            self.links = r["links"]
        return r

    def remove_existing_files(self):
        logging.info("clean")
        # grab the representation for the very last deposit
        r = self._request("GET", "/" + self._latest_id())
        for file in r.get("files", []):
            file_id = file["id"]
            file_url = f"/{self._latest_id()}/files/{file_id}"
            r = self._request("DELETE", file_url)
        return r

    def new_version(self):
        logging.info("new version")

        error_msg = f"The deposit {self.deposition_id} has an unpublished version, " \
                    + "I can not add a new one. " \
                    + "Please remove or publish the existing version, " \
                    + "then run again." + "\n" + str(self.deposit)

        if "latest_draft" in self.links:
            draft = self._request("GET", self.links["latest_draft"], full_path=True)
            if draft['submitted'] == False:
                raise ValueError(error_msg)
        elif self.deposit['submitted'] == False:
            raise ValueError(error_msg)

        req_url = f"/{self.deposition_id}/actions/newversion"
        r = self._request("POST", req_url)
        if "links" in r:
            self.links = r["links"]
            self.deposit = r
        return r

    def publish_latest_draft(self):
        id = self._latest_id()
        logging.info(f"publish {id}")
        req_url = f"/{id}/actions/publish"
        return self._request("POST", req_url)


def get_metadata(settings: Settings) -> dict:
    """Get metadata from zenodo

    Args:
        settings : Settings
            The Settings object - the result of calling `Settings()`

    Returns:
        dict
            The full API response object

    Raises:
        NameError
            If no token can be found in the settings
        NameError
            If no record ID can be found in the settings
    """
    sandbox = settings.get("sandbox")
    token = settings.get("zenodo_token")
    record = settings.get("zenodo_record")

    if token is None:
        raise NameError(
            "You need to set the zenodo_token environment variable, "
            "or pass the token as argument")
    if record is None:
        raise NameError(
            "You need to set the zenodo_record environment variable, "
            "or pass the record ID as argument")

    deposit = ZenodoDeposit(token=token, sandbox=sandbox)
    return deposit.get_deposit(record)


def send(settings: Settings):
    """Create a new Zenodo record and upload archive together with metadata

    Args:
        settings : Settings
            The Settings object - the result of calling `Settings()`

    Raises:
        NameError
            If no token can be found in the settings
    """
    sandbox = settings.get("sandbox")
    token = settings.get("zenodo_token")
    record = settings.get("zenodo_record")
    metadata_path = settings.get("metadata")
    archive_path = settings.get("archive")
    publish = settings.get("publish")

    if token is None:
        raise NameError(
            "You need to set the zenodo_token environment variable, "
            "or pass the token as argument")

    with metadata_path.open("r", encoding="utf-8") as f:
        metadata = prepare_metadata(json.load(f), settings)

    deposit = ZenodoDeposit(token=token, sandbox=sandbox)

    # if "zenodo_record" in os.environ:
    if record is not None:
        deposit.get_deposit(record)
        deposit.new_version()
        deposit.remove_existing_files()
    else:
        deposit.new_deposit()
        # this is NOT a debug print, it serves to pipe the deposit ID to further scripts.
        # This must remain the only stdout output
        print(deposit.deposition_id)
        logging.info(f"Please add the identifier {deposit.deposition_id}"
                     f" as a variable zenodo_record")

    deposit.upload_metadata({'metadata': metadata})
    deposit.upload(archive_path)

    if publish:
        deposit.publish_latest_draft()


def prepare_metadata(metadata: dict, settings: Settings) -> dict:
    """Prepare metadata for upload to Zenodo

    + The related identifiers 'isIdenticalTo' and 'isCompiledBy' are added to the metadata
    + The version is updated
    + Problematic keys are removed

    Args:
        metadata : dict
            The metadata to prepare for upload
        settings : Settings
            The Settings object - the result of calling `Settings()`

    Returns:
        dict
            The updated metadata
    """
    version = settings.get("version")
    if version is not None:
        metadata["version"] = version

    ident_set = {item["relation"]: item for item in settings.get(
        "related_identifiers", [])}

    # Remove the doi item - the presence confuses zenodo
    if "doi" in metadata:
        del metadata["doi"]

    if "related_identifiers" in metadata:
        rel_meta = [item["relation"]
                    for item in metadata["related_identifiers"]]

        for k, v in ident_set.items():
            if k not in rel_meta:
                metadata["related_identifiers"].append(v)
    else:
        metadata["related_identifiers"] = settings.get("related_identifiers")
    return metadata
