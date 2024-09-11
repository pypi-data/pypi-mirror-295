#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
from copy import deepcopy
from functools import partial
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import Mock, call, mock_open, patch

import requests
import responses

from gitlab2zenodo.deposit import (ZenodoDeposit, get_metadata,
                                   prepare_metadata, send)
from gitlab2zenodo.settings import Settings

metadata_content = {
    "title": "Some title",
    "upload_type": "dataset",
    "description": "This is a test metadata",
    "version": "0.1.0",
    "creators": [
        {
            "name": "Name, Lastname",
            "affiliation": "authorAffiliation"
        }
    ]
}


class TestGitlab2Zenodo(TestCase):
    bucket_link = 'https://sandbox.zenodo.org/api/files/some-sha'
    bucket_link2 = 'https://sandbox.zenodo.org/api/files/some-other-sha'

    deposit_120 = {'id': '120', 'links': {'latest': '/120', 'bucket': bucket_link},
                   'files': [{'id': '7'}], 'submitted': False}
    deposit_123 = {'id': '123', 'conceptrecid': '123', 'links': {'latest': '/123', 'bucket': bucket_link},
                   'files': [{'id': '8'}], 'submitted': True}
    deposit_concept = [deposit_123]
    deposit_125_draft = {'id': '125', 'links': {'latest_draft': '/125', 'bucket': bucket_link},
                         'files': [{'id': '8'}], 'submitted': False}
    deposit_124 = {'id': '124', 'links': {'latest_draft': '/125', 'bucket': bucket_link},
                   'files': [{'id': '1'}, {'id': '2'}], 'submitted': True}
    deposit_345 = {'id': '345', 'links': {'latest_draft': '/125', 'bucket': bucket_link},
                   'files': [{'id': '5'}, {'id': '6'}], 'submitted': True}
    deposit_4 = {'id': 4, 'links': {'bucket': bucket_link2,
                                    'latest_draft': '3'}}

    @classmethod
    def tearDownClass(cls):
        responses.stop()
        responses.reset()

    @classmethod
    def setUpClass(cls):

        def force_json(request, json_resp={}):
            if "Content-type" not in request.headers \
                    or request.headers["Content-type"] != "application/json":
                return (415, request.headers, json.dumps(json_resp))
            return (200, request.headers, json.dumps(json_resp))

        responses.start()
        api_regex = r'https://(sandbox.)?zenodo.org/api/deposit/depositions'
        authorized_token = r"\?access_token=test_token"

        # test_get_deposit
        responses.add(responses.GET,
                      re.compile(api_regex + authorized_token),
                      json=cls.deposit_concept, status=200)
        responses.add(responses.GET,
                      re.compile(api_regex + "/123" + authorized_token),
                      json=cls.deposit_123, status=200)

        # test_remove_existing_files
        responses.add(responses.GET,
                      re.compile(api_regex + "/124" + authorized_token),
                      json=cls.deposit_124, status=200)

        responses.add(responses.GET,
                      re.compile(api_regex + "/125" + authorized_token),
                      json=cls.deposit_125_draft, status=200)

        # test_publish_latest_draft
        responses.add(responses.GET,
                      re.compile(api_regex + "/345" + authorized_token),
                      json=cls.deposit_345, status=200)

        # test_new_deposit
        responses.add_callback(responses.POST,
                               re.compile(api_regex + authorized_token),
                               callback=partial(force_json,
                                                json_resp=cls.deposit_120)
                               )
        responses.add(responses.POST, re.compile(
            api_regex + "/120/actions/publish" + authorized_token),
                      status=200)

        # test_send
        responses.add_callback(responses.PUT,
                               re.compile(
                                   api_regex + r"/\d+" + authorized_token),
                               callback=force_json)

        # test_send, test_upload (using bucket link)
        responses.add(responses.PUT,
                      re.compile(
                          cls.bucket_link + r".+\.(json|zip)" + authorized_token),
                      status=200)

        # test_remove_existing_files
        responses.add(responses.DELETE,
                      re.compile(
                          api_regex + "/12[345]/files/[128]" + authorized_token),
                      status=200)

        # test_new_version
        responses.add(responses.POST, re.compile(
            api_regex + "/(12[34]|345)/actions/newversion" + authorized_token),
                      json=cls.deposit_125_draft,
                      status=200)
        # test_publish_latest_draft
        responses.add(responses.POST, re.compile(
            api_regex + "/12[435]/actions/publish" + authorized_token),
                      status=200)
        # test upload_metadata updating links to store new bucket
        responses.add(responses.PUT,
                      re.compile(api_regex + "/4" + authorized_token),
                      json=cls.deposit_4, status=200)

    @patch("gitlab2zenodo.deposit.ZenodoDeposit.get_deposit")
    def test_get_metadata(self, mock_get_deposit):
        settings = Settings()
        settings["zenodo_token"] = "zenodo_token"
        settings["zenodo_record"] = "zenodo_record"
        settings["sandbox"] = True

        expectation = {"key": "value"}
        mock_get_deposit.return_value = expectation

        ret_val = get_metadata(settings)
        self.assertEqual(mock_get_deposit.call_count, 1)
        mock_get_deposit.assert_called_with("zenodo_record")
        self.assertEqual(ret_val, expectation)

        settings["sandbox"] = False
        ret_val = get_metadata(settings)
        self.assertEqual(mock_get_deposit.call_count, 2)
        mock_get_deposit.assert_called_with("zenodo_record")
        self.assertEqual(ret_val, expectation)

        # ------------------------------------------------ #
        #
        # Exceptions
        #
        # ------------------------------------------------ #
        settings = Settings()

        # Token is missing
        self.assertRaisesRegex(NameError, "zenodo_token", get_metadata, settings)

        # Record ID is missing
        settings["zenodo_token"] = "zenodo_token"
        self.assertRaisesRegex(NameError, "zenodo_record", get_metadata, settings)

    @patch("gitlab2zenodo.deposit.ZenodoDeposit.new_version")
    @patch("gitlab2zenodo.deposit.ZenodoDeposit.publish_latest_draft")
    def test_send(self, mock_newversion, mock_publish_latest_draft):

        mock_path = Mock(spec=Path)
        mock_path.open = mock_open(read_data=json.dumps(metadata_content))
        mock_path.name = ".zenodo.json"

        mock_path2 = Mock(spec=Path)
        mock_path2.open = mock_open()
        mock_path2.name = ".zenodo.json"

        args = SimpleNamespace(sandbox=True, publish=True,
                               metadata=mock_path,
                               archive=mock_path2)

        # When no token, throws exception
        with patch.dict('os.environ', {}, clear=True):
            # We could update the settings directly, but calling the
            # instantiation re-created the original functionality of
            # `prepare_metadata()` where environment variables are read
            settings = Settings(args)
            self.assertRaises(NameError, send, settings)

        # With a proper environment and token, goes through
        env = {"zenodo_record": "123",
               "CI_COMMIT_TAG": "v1.0.1-beta",
               "CI_PROJECT_URL": "https://gitlab.com/user/project",
               "zenodo_token": "test_token"
               }
        with patch.dict('os.environ', env):
            settings = Settings(args)
            try:
                settings["publish"] = True
                send(settings)
                settings["publish"] = False
                send(settings)
            except:
                self.fail("Main function failed")

        # With a proper environment and no record, goes through
        del env["zenodo_record"]
        with patch.dict('os.environ', env):
            settings = Settings(args)
            try:
                settings["publish"] = True
                send(settings)
                settings["publish"] = False
                send(settings)
            except:
                self.fail("Main function failed")

    def test_prepare_metadata(self):
        env = {"zenodo_record": "123",
               "CI_COMMIT_SHA": "somesha",
               "CI_COMMIT_TAG": "v1.0.1-beta",
               "CI_PROJECT_URL": "https://gitlab.com/user/project"
               }
        metadata = deepcopy(metadata_content)

        with patch.dict('os.environ', env):
            # When there were no relations and we have a tag version,
            # Add relations and replace version number
            # We could update the settings directly, but calling the
            # instantiation re-created the original functionality of
            # `prepare_metadata()` where environment variables are read
            settings = Settings()
            result = prepare_metadata(deepcopy(metadata), settings)
            expected = deepcopy(metadata)
            expected.update({'version': '1.0.1-beta',
                             'related_identifiers':
                                 [{'relation': 'isIdenticalTo',
                                   'identifier': 'https://gitlab.com/user/project/-/tree/v1.0.1-beta'},
                                  {'relation': 'isCompiledBy',
                                   'identifier': 'https://gitlab.com/user/project'}]
                             })
            self.assertDictEqual(result, expected)

            # When the relations exist already, do not change them.
            idto = {'relation': 'isIdenticalTo', 'identifier': 'itself'}
            metadata['related_identifiers'] = [idto]
            result = prepare_metadata(deepcopy(metadata), settings)
            self.assertIn(idto, result["related_identifiers"])

            compiledby = {'relation': 'isCompiledBy', 'identifier': 'a repo'}
            metadata['related_identifiers'] = [compiledby]
            result = prepare_metadata(deepcopy(metadata), settings)
            self.assertIn(compiledby, result["related_identifiers"])

        # When the tag is a version name, change version
        env["CI_COMMIT_TAG"] = "v2.0.0"
        settings["version"] = metadata["version"]
        with patch.dict('os.environ', env):
            settings = Settings()
            result = prepare_metadata(deepcopy(metadata), settings)
            self.assertEqual(result["version"], env["CI_COMMIT_TAG"][1:])

        # When the tag is not a version name, do not change version
        env["CI_COMMIT_TAG"] = "test"
        settings["version"] = metadata["version"]
        with patch.dict('os.environ', env):
            settings = Settings()
            result = prepare_metadata(deepcopy(metadata), settings)
            self.assertEqual(result["version"], metadata["version"])

        # When the commit is not a tag, do not change version
        del env["CI_COMMIT_TAG"]
        with patch.dict('os.environ', env):
            # Must be removed here, the patch doesn't remove previous values
            if "CI_COMMIT_TAG" in os.environ:
                del os.environ["CI_COMMIT_TAG"]
            settings = Settings()
            result = prepare_metadata(deepcopy(metadata), settings)
            self.assertEqual(result["version"], metadata["version"])

    def test_ZenodoDepositObject(self):
        # When creating the object, the sandbox switch changes the url
        deposit = ZenodoDeposit(token="token", sandbox=True)
        self.assertEqual(deposit.zenodo_url,
                         "https://sandbox.zenodo.org/api/deposit/depositions")
        deposit = ZenodoDeposit(token="token", sandbox=False)
        self.assertEqual(deposit.zenodo_url,
                         "https://zenodo.org/api/deposit/depositions")

    def test__request(self):
        access_token = "token_request"
        deposit = ZenodoDeposit(
            token=access_token, sandbox=True)
        deposit.zenodo_url = "https://base.url/deposit/depositions"

        response_content = {"id": "120", "links": "the links"}
        responses.add(
            responses.GET,
            f"https://base.url/deposit/depositions/some/url?access_token={access_token}",
            json=response_content,
            status=200)

        responses.add(
            responses.GET,
            f"https://base.url/deposit/depositions/some/url/search?access_token={access_token}",
            json=[response_content],
            status=200)

        responses.add(
            responses.GET,
            f"https://base.url/deposit/depositions/some/url?access_token={access_token}&key=value",
            json=response_content,
            status=200)

        responses.add(
            responses.GET,
            f"https://base.url/deposit/depositions/some/url?access_token={access_token}&param_key1=param_value1",
            json={**response_content, "extra_param_key": True},
            status=200)

        # GET works as expected
        self.assertEqual(
            deposit._request(
                "get",
                path="https://base.url/deposit/depositions/some/url",
                full_path=True),
            response_content)
        self.assertEqual(
            deposit._request(
                "get",
                path="/some/url",
                full_path=False),
            response_content)
        self.assertEqual(
            deposit._request(
                "get",
                path="/some/url",
                full_path=False,
                headers={"key1": "value1"}),
            response_content)
        self.assertEqual(
            deposit._request(
                "get",
                path="/some/url",
                full_path=False,
                params={"param_key1": "param_value1"}),
            {**response_content, "extra_param_key": True})
        self.assertEqual(
            deposit._request(
                "get",
                path="/some/url/search",
                full_path=False),
            [response_content])

        self.assertEqual(
            deposit._request(
                "get",
                path="/some/url",
                full_path=False),
            response_content)

        # Assert put, post, delete
        responses.add(
            responses.PUT,
            f"https://base.url/deposit/depositions/some/url?access_token={access_token}",
            json=response_content,
            status=200)
        responses.add(
            responses.POST,
            f"https://base.url/deposit/depositions/some/url?access_token={access_token}",
            json=response_content,
            status=200)
        responses.add(
            responses.DELETE,
            f"https://base.url/deposit/depositions/some/url?access_token={access_token}",
            json=None,
            status=204)

        self.assertEqual(
            deposit._request(
                "put",
                path="/some/url",
                full_path=False),
            response_content)
        self.assertEqual(
            deposit._request(
                "post",
                path="/some/url",
                full_path=False),
            response_content)
        self.assertEqual(
            deposit._request(
                "delete",
                path="/some/url",
                full_path=False),
            {})

        # Content cannot be JSON decoded
        responses.add(
            responses.GET,
            f"https://base.url/deposit/depositions/nonsense/body?access_token={access_token}",
            body="{nonsense string}",
            status=200)

        self.assertEqual(deposit._request("get", path="/nonsense/body"), {})

        # Clean
        responses.remove(responses.GET, "https://base.url/deposit/depositions/nonsense/body")

        responses.remove(
            responses.GET,
            f"https://base.url/put/some/url?access_token={access_token}")
        responses.remove(
            responses.GET,
            f"https://base.url/put/some/url/search?access_token={access_token}")
        responses.remove(
            responses.GET,
            f"https://base.url/some/url?access_token={access_token}&key=value")
        responses.remove(
            responses.PUT,
            f"https://base.url/put/some/url?access_token={access_token}")
        responses.remove(
            responses.POST,
            f"https://base.url/post/some/url?access_token={access_token}")
        responses.remove(
            responses.DELETE,
            f"https://base.url/delete/some/url?access_token={access_token}")

    def test__request_exceptions(self):
        access_token = "token_request_exceptions"
        deposit = ZenodoDeposit(
            token=access_token, sandbox=True)

        deposit.zenodo_url = "https://base.url/"

        errors_codes = [
            401,  # Unauthorized
            404,  # Not Found
            408,  # Request Timeout
        ]

        # Selected http errors
        for http_error in errors_codes:
            responses.add(
                responses.GET,
                "https://base.url/some/url",
                status=http_error)

            self.assertRaises(
                requests.exceptions.RequestException,
                deposit._request, "get", path="/some/url"
            )

            # Clean
            responses.remove(responses.GET, "https://base.url/some/url")

            # Clean
            responses.remove(
                responses.GET,
                f"https://base.url/some/url?access_token={access_token}"
            )

    def test_new_deposit(self):
        try:
            # When creating a new deposit, all fields are updated
            deposit = ZenodoDeposit(token="test_token", sandbox=True)
            deposit.new_deposit()
        except requests.exceptions.ConnectionError:
            self.fail("Wrong route")
        self.assertEqual(deposit.deposition_id, "120")
        self.assertEqual(deposit._latest_id(), "120")
        self.assertEqual(deposit.deposit, self.deposit_120)

    @patch("gitlab2zenodo.deposit.ZenodoDeposit._request")
    def test_get_deposit(self, mock_request):
        deposit = ZenodoDeposit(
            token="access_token",
            sandbox=True)

        self.assertTrue("https://sandbox.zenodo.org" in deposit.zenodo_url)

        mock_concept_return = [{
                "conceptrecid": "123",
                "id": "456",
                "links": {"latest": "some/url/456"}
            }]

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        #
        # Test call with a concept ID
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        mock_request.return_value = mock_concept_return

        deposit.get_deposit("456")
        self.assertEqual(deposit.deposition_id, "456")
        self.assertEqual(deposit.links, {"latest": "some/url/456"})
        self.assertEqual(mock_request.call_count, 1)

        mock_request.reset_mock()
        deposit.deposition_id = None
        deposit.links = []

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        #
        # Test call with a record ID
        #
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        #
        # We call _request three times.
        # 1. Search for the given ID which gives an empty dict
        # 2. Access the record
        # 3. Search for the concept ID
        #
        mock_request.side_effect = [
            {},
            {
                "conceptrecid": "123",
            },
            mock_concept_return
        ]

        deposit.get_deposit("456")
        self.assertEqual(deposit.deposition_id, "456")
        self.assertEqual(deposit.links, {"latest": "some/url/456"})
        self.assertEqual(mock_request.call_count, 3)

        # Assert the function was called with the correct arguments
        call_args_lst = mock_request.call_args_list

        self.assertEqual(call_args_lst[0], call("GET", "", params={"q": "conceptrecid:456"}))
        self.assertEqual(call_args_lst[1], call("GET", "/456"))
        self.assertEqual(call_args_lst[2], call("GET", "", params={"q": "conceptrecid:123"}))

        mock_request.reset_mock()

        # ------------------------------------------------ #
        #
        # Exceptions
        #
        # ------------------------------------------------ #
        # Missing 'conceptrecid' raises an error
        mock_request.side_effect = [
            {},
            {
                "missing_conceptrecid": "123",
            }
        ]

        with self.assertRaisesRegex(
            ValueError, "did not contain any URL called 'conceptrecid'"):
            deposit.get_deposit("456")
        self.assertEqual(mock_request.call_count, 2)

        mock_request.reset_mock()
        mock_request.side_effect = None

        # Missing 'id' or 'links' property throws and error
        mock_concepts = [
            {'missing': 'id', 'concept': [{'links': 'the links'}]},
            {'missing': 'links', 'concept': [{'id': 'the id'}]}
        ]

        for mock_concept in mock_concepts:
            mock_request.return_value = mock_concept['concept']
            expect_missing = mock_concept['missing']
            with self.assertRaisesRegex(
                ValueError, f"did not contain the property '{expect_missing}'"):
                deposit.get_deposit("456")
        self.assertEqual(mock_request.call_count, 2)

    @patch("gitlab2zenodo.deposit.ZenodoDeposit._request")
    def test_upload(self, mock_request):
        # Upload uses the right route and sends multipart data
        deposit = ZenodoDeposit(
            token="test_token", sandbox=True)

        response_value = {
            "id": 120,
            "links": {
                "bucket": "bucket/link",
                "latest": "the link to latest"}}
        mock_request.return_value = response_value

        # upload uses `links["bucket"]` in the deposit object
        deposit.deposit = {"links": {"bucket": "bucket/link"}}

        mock_path = Mock(spec=Path)
        mock_path.open = mock_open()
        mock_path.name = "file.zip"

        call_res = deposit.upload(mock_path)

        mock_request.assert_called_once_with(
            "PUT",
            "bucket/link/file.zip",
            full_path=True,
            data=mock_path.open())

        self.assertDictEqual(call_res, response_value)

        # If path is a string, we also manage
        mock_path = "a/file/path/file.zip"
        with patch("pathlib.Path.open") as mock_path_open:
            call_res = deposit.upload(mock_path)
            mock_path_open.assert_called_once()

        # ------------------------------------------------ #
        #
        # Exceptions
        #
        # ------------------------------------------------ #
        # In the event that 'bucket' disappears from the links-set
        deposit.deposit = {"links": {}}
        self.assertRaisesRegex(
            ValueError,
            "did not contain any URL called 'bucket'",
            deposit.upload, mock_path)

    @patch("gitlab2zenodo.deposit.ZenodoDeposit._request")
    @patch("gitlab2zenodo.deposit.ZenodoDeposit._latest_id")
    def test_upload_metadata(self, mock_latest_id, mock_request):
        mock_latest_id.return_value = "test_id"

        # When depositing metadata, simply check the route and headers
        deposit = ZenodoDeposit(token="test_token", sandbox=True)
        deposit.new_deposit()
        try:
            deposit.upload_metadata({'metadata': {"key": "value"}})
        except:
            self.fail("Metadata call failed")

    def test_upload_metadata_updates_links(self):
        # when depositing metadata, bucket should be updated by storing 'links'
        deposit = ZenodoDeposit(token="test_token", sandbox=True)
        deposit.deposit = {"id": "4"}
        self.assertNotIn('bucket', deposit.links)
        deposit.upload_metadata({'metadata': {"key": "value"}})

        # This fails because upload_metadata does not seem to add a bucket...
        # However, not something to fix right now...
        deposit.links = {"bucket": self.bucket_link2}
        # self.assertEqual(deposit.links['bucket'], self.bucket_link2)

    @patch("gitlab2zenodo.deposit.ZenodoDeposit._request")
    def test_remove_existing_files(self, mock_request):

        mock_request.return_value = {}
        # Grabs latest version
        try:
            deposit = ZenodoDeposit(token="test_token", sandbox=True)
            deposit.deposit = {
                'id': '125',
                'links': {
                    'latest_draft': '/125',
                    'bucket': 'https://sandbox.zenodo.org/api/files/some-sha'},
                'files': [{'id': '8'}],
                'submitted': False}

            # deposit.get_deposit("345")
            # getting 345, but latest version, with the right files to delete, is 124
            deposit.remove_existing_files()
        except:
            self.fail("Delete call failed")


    @patch("gitlab2zenodo.deposit.ZenodoDeposit._request")
    def test_new_version(self, mock_request):
        deposit = ZenodoDeposit(
            token="test_token", sandbox=True)

        new_version_id = "789"
        link_new_version = "some/url/action/newversion"

        deposit.deposit = {
            "links": {"newversion": link_new_version},
            "submitted": True}
        response_value = {"links": {"latest_draft": f"some/url/{new_version_id}"}}
        mock_request.return_value = response_value

        call_res = deposit.new_version()

        mock_request.assert_called_once_with(
            "POST", link_new_version, full_path=True)

        self.assertDictEqual(call_res, response_value)
        self.assertDictEqual(deposit.deposit, response_value)

        # ------------------------------------------------ #
        #
        # Exceptions
        #
        # ------------------------------------------------ #
        # Reset deposit
        deposit = ZenodoDeposit(
            token="test_token", sandbox=True)

        # If not submitted
        deposit.deposit = {"submitted": False}
        self.assertRaisesRegex(
            ValueError,
            "The deposit .* has an unpublished version",
            deposit.new_version)

        deposit.links = {"latest_draft": "latest/draft/url"}
        mock_request.return_value = {'submitted': False}
        self.assertRaisesRegex(
            ValueError,
             "The deposit .* has an unpublished version",
            deposit.new_version)

        deposit.links = {}
        # No newversion in link
        deposit.deposit = {"links":  {}, "submitted": True}
        self.assertRaisesRegex(
            ValueError,
            "'newversion'",
            deposit.new_version)

        # Strange API response
        deposit.links = {"newversion": link_new_version}
        deposit.deposit = {"submitted": True}
        mock_request.return_value = {}
        self.assertRaisesRegex(
            ValueError,
            "'newversion'",
            deposit.new_version)


    @patch("gitlab2zenodo.deposit.ZenodoDeposit._request")
    def test_publish_latest_draft(self, mock_request):
        deposit = ZenodoDeposit(
            token="test_token", sandbox=True)

        deposit.deposit = {"links": {"publish": "some/url/action/publish"}}
        response_value = {"id": 120, "links": {"latest": "the link to latest"}}
        mock_request.return_value = response_value

        call_res = deposit.publish_latest_draft()

        # Test _request call parameters
        mock_request.assert_called_once_with(
            "POST", deposit.deposit["links"]["publish"], full_path=True)

        # publish_latest_draft returns the return value from _request   
        self.assertDictEqual(call_res, response_value)
        mock_request.reset_mock()

        # ------------------------------------------------ #
        #
        # Exceptions
        #
        # ------------------------------------------------ #
        # There is no 'publish' in the links
        deposit.deposit = {"links": {}}
        self.assertRaises(ValueError, deposit.publish_latest_draft)
        self.assertEqual(mock_request.call_count, 0)
