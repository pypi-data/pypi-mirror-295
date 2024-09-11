#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

from gitlab2zenodo.settings import Settings


class TestSettings(TestCase):
    # When we run on gitlab CI we have several CI environment variables set.
    # Easiest is to run each test temporarily without an environment at all

    def test_init(self):
        with patch.dict("os.environ", clear=True):
            settings = Settings()

            self.assertEqual(len(settings.keys()), 0)
            self.assertNotIn("zenodo_token", settings)
            self.assertNotIn("zenodo_record", settings)
            self.assertNotIn("version", settings)
            self.assertNotIn("related_identifiers", settings)

            self.assertEqual(len(settings.keys()), 0)
            args = SimpleNamespace(a_key="a_value")
            settings = Settings(args=args)
            self.assertEqual(settings.get("a_key"), "a_value")

        with patch.dict("os.environ", {"zenodo_token": "a_token"}):
            settings = Settings()
            self.assertEqual(settings.get("zenodo_token"), "a_token")

            settings = Settings(SimpleNamespace(zenodo_token=None))
            self.assertEqual(settings.get("zenodo_token"), "a_token")

            settings = Settings(SimpleNamespace(zenodo_token="args_token"))
            self.assertEqual(settings.get("zenodo_token"), "args_token")

    def test_init_zenodo(self):
        with patch.dict("os.environ", clear=True):
            settings = Settings()
            self.assertEqual(len(settings.keys()), 0)

            # Set zenodo parameters
            env = {
                "zenodo_token": "the token value",
                "zenodo_record": "the record value"
            }

            # with patch.dict('os.environ', env):
            os.environ.update(env)
            settings = Settings()
            self.assertEqual(len(settings.keys()), 2)
            self.assertEqual(settings.get("zenodo_token"), env["zenodo_token"])
            self.assertEqual(settings.get("zenodo_record"),
                             env["zenodo_record"])

    def test_init_version(self):
        with patch.dict("os.environ", clear=True):
            # Set version
            tag_version = {
                "test.version0.4.01-oddity": "0.4.01-oddity",
                "0.8": "0.8",
                "v1.3": "1.3",
                "v1.3-beta": "1.3-beta",
                "v1.3xxx7.8": "1.3xxx7.8",
                "v12.66.99.88": "12.66.99.88"}

            for t, v in tag_version.items():
                os.environ["CI_COMMIT_TAG"] = t
                settings = Settings()
                self.assertEqual(settings.get("version"), v)

            # Changing the tag to a non-version string, should not change the version value
            del settings
            version_value = "1.2.3beta"
            os.environ["CI_COMMIT_TAG"] = version_value
            settings = Settings()
            self.assertEqual(settings.get("version"), version_value)

            os.environ["CI_COMMIT_TAG"] = "all text no version"
            settings = Settings()
            self.assertNotIn("version", settings)

    def test_init_url(self):
        def _test_related_identifiers():
            settings = Settings()
            ret_lst = settings.get("related_identifiers")
            self.assertIsInstance(ret_lst, list)
            self.assertEqual(len(ret_lst), 2)
            for rld in ret_lst:
                self.assertIn("relation", rld.keys())
                self.assertIn("identifier", rld.keys())

        with patch.dict("os.environ", clear=True):
            # Set URLs
            tag_value = "the tag"
            url_value = "the/url/value"

            os.environ["CI_COMMIT_TAG"] = tag_value
            os.environ["CI_PROJECT_URL"] = url_value
            _test_related_identifiers()

            # Remove commit tag
            os.environ.pop("CI_COMMIT_TAG")
            os.environ["CI_COMMIT_SHA"] = tag_value
            _test_related_identifiers()

            # Test requirement of tag/sha AND url
            os.environ.clear()

            var_val = {
                "CI_PROJECT_URL": url_value,
                "CI_COMMIT_SHA": tag_value,
                "CI_COMMIT_TAG": tag_value
            }
            for k, v in var_val.items():
                os.environ[k] = v
                settings = Settings()
                self.assertNotIn("related_identifiers", settings)
                os.environ.pop(k)
