#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

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

    def _request(self, method, path, full_path=False, params=None, **kwargs):
        """Interface to `requests.request()` which consistently returns a dict

        Args:
            method : str
                The HTTP method. Can be one of 'GET', 'PUT', 'POST', and 'DELETE'
            path : str
                The path to the API object or action, like record, file or new version
            full_path : bool, optional
                Is the given path the full path to the object, by default False

                If false, the path is corrected based on the base URL stored in the deposit object.
            params: dict
                Extra parameters
            kwargs
                Additional arguments passed to `requests.request()`

        Returns:
            dict
                The API response

        Raises:
           requests.HTTPError
                If the response from the server is outside the 200-range
            Exception
                If the JSON could not be decoded
        """
        if not full_path:
            path = self.zenodo_url + path

        # We may send additional params with the kwargs - this is at least the case
        # if we search for a concept id
<<<<<<< HEAD
        if params is None:
            params = self.params
        else:
            params = {**self.params, **params}

        r = requests.request(method, path,
                             params=params,
                             **kwargs)
=======
        params = self.params
        if "params" in kwargs:
            params = {**params, **kwargs["params"]}
            del kwargs["params"]
>>>>>>> 8d74af5 (Handle json decoding errors separately)

        r = requests.request(
            method,
            path,
            params=params,
            **kwargs)

        # Prepare a message to print if something goes wrong
        # The token is stored in `self.params` and will be printed here.
        # Masking it makes little sense, because the exception prints the entire URL,
        # including the token
        error_message = (
            "This error occurred while sending: "
            f"method: {method} | path: {path} | params: {self.params} | metadata: {str(kwargs)}"
        )
        infos = {}

        # No need to continue if if we have some HTTP error
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            error_message = f"{error_message} || server responded: {r.text}"
            raise requests.HTTPError(error_message) from e

        # At least the DELETE method returns an empty body, a search returns a
        # json decodable list, and most other API calls some content which can
        # be JSON decoded.
        # To avoid any unexpected results, we check if the content looks
        # like a JSON - it may still fail though, even if it does have JSON
        # opening and closing
        if re.match(r"^\{.*\}$|^\[.*\]$", r.text):
            # Throw an exception if the response object did not create a valid JSON
            try:
<<<<<<< HEAD
                r.raise_for_status()
            except Exception as e:
                errors = infos.get("errors", [])
                extra_message = "".join([err["field"] + ": " + err["message"] for err in errors])
                extra_message += "\n\tThis error occured while sending metadata:\n\t" + str(kwargs)
                raise requests.RequestException(extra_message) from e
        if not r.ok:
            details = f"\n\nOccurred while sending {method} to {path}"
            raise requests.RequestException(", ".join([f"{k}: {v}" for k, v in r.json().items()]) + details)

        return infos

    def get_deposit(self, zenodo_id: str):
        """
        Gets the latest record from any Zenodo ID (concept/deposit or existing record).

        Args:
            zenodo_id : str
                The ID to search for - either for a concept/deposit or an
                existing record.

        Returns:
            dict: The complete information for the latest record.

        Raises:
            ValueError: If the given ID does not lead to a concept/deposit or record.
        """
        logging.info("Getting the ID for the latest version of the concept")

        # We need the value of  property `newversion` in the `links` section to create a new record.
        # However, Zenodo creates a copy of the record, so it important that we get the `newversion`
        # from the latest record. pThe easiest is to find the concept, because that automatically
        # points to the newest record
        #
        # The process here is first to search for the concept and if that gives an empty body,
        # we have a record ID we can access. We cannot just access the given ID as if it was the
        # record ID, because the request fails with 404 if we have a concept ID and access it
        # through `api/deposit/depositions/:id`

        # Search for the concept
        api_ret = self._request(
            "GET",
            "",
            params={"q": f"conceptrecid:{zenodo_id}"})

        # If the ID passed to the function is for a record, the response is empty
        logging.debug("Search for '%s' gave the response: '%s'.", zenodo_id, api_ret)
        if not api_ret:
            # Get the record
            logging.debug("Search for '%s' gave nothing. Accessing as record.", zenodo_id)
            api_ret = self._request(
                "GET",
                f"/{zenodo_id}")
            # Check that the world is sane
            if "conceptrecid" not in api_ret:
                err_str = (
                    f"The API response for {zenodo_id} did not contain any URL called "
                    "'conceptrecid'. This is highly unexpected and very serious, "
                    "so you should probably file a bug report"
                )
                raise ValueError(err_str)

            # And call again
            zenodo_id = api_ret["conceptrecid"]
            logging.debug("Search using the conceptrecid '%s'", zenodo_id)

            return self.get_deposit(zenodo_id)

        api_ret = api_ret[0]
        print(api_ret)
        # Check for important keys
        important_keys = ["id", "links"]
        for important_key in important_keys:
            print("+" * 60)
            print(important_key)
            if important_key not in api_ret:
                err_str = (
                    f"The API response for {zenodo_id} did not contain the property "
                    f"'{important_key}'. This is highly unexpected and very serious, "
                    "so you should probably file a bug report"
                )
                print(err_str)
                raise ValueError(err_str)

        # We use the record ID mostly for logging purposes
        self.deposition_id = api_ret["id"]
        self.links = api_ret["links"]
        self.deposit = api_ret

        return api_ret
=======
                infos = r.json()
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(error_message, r.text, 0) from e

        return infos


    def get_deposit(self, id):
        logging.info("get deposit")
        r = self._request("GET", "/" + id)
        self.deposition_id = str(r['id'])
        self.links = r["links"]
        self.deposit = r
        return r
>>>>>>> 8d74af5 (Handle json decoding errors separately)

    def new_deposit(self):
        logging.info("new deposit")
        r = self._request("POST", "", json={})  # , headers=self.headers)
        self.deposit = r
        self.deposition_id = str(r['id'])
        self.links = r["links"]
        return r

    def upload(self, path: Path) -> dict:
        """Upload a file to the current bucket

        Args:
            path : Path
                The path to the file to upload

        Returns:
            dict
                The API response

        Raises:
            ValueError
                If the links-set does not contain the key 'bucket'
        """

        # Make sure the path really is a Path
        if isinstance(path, str):
            path = Path(path)
        logging.info("Upload the file '%s' to the record ''%s", path.name, self.deposition_id)

        bucket_url = self.deposit.get("links", {}).get("bucket", None)

        if not bucket_url:
            raise ValueError(
                f"The API response for {self.deposition_id} did not contain any URL called 'bucket'. "
                "This is highly unexpected and very serious, so you should "
                "probably file a bug report")

        with path.open("rb") as fp:
            r = self._request(
                "PUT", bucket_url + "/" + path.name, full_path=True, data=fp)
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

        req_url = self.deposit.get("links", {}).get("newversion", None)

        if not req_url:
            error_msg = (
                f"The API response for {self.deposition_id} did not contain any URL called "
                "'newversion'. This is highly unexpected and very serious, so you should "
                "probably file a bug report")
            raise ValueError(error_msg)

        r = self._request("POST", req_url, full_path=True)
        if "links" in r:
            self.links = r["links"]
            self.deposit = r
        return r


    def publish_latest_draft(self) -> dict:
        """Publish the current record

        Returns:
            dict
                The API response

        Raises:
            ValueError
                If links do not contain a 'publish' URL
        """

        logging.info("Publish record '%s'", self.deposition_id)

        req_url = self.deposit.get("links", {}).get("publish", None)

        if not req_url:
            error_msg = (
                f"The API response for {self.deposition_id} did not contain any URL called "
                "'publish'. This is highly unexpected and very serious, so you should "
                "probably file a bug report")
            raise ValueError(error_msg)
        return self._request("POST", req_url, full_path=True)


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
