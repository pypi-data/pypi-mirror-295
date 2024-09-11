#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re


class Settings(dict):
    """Object for storing and accessing settings variables.
    """

    def __init__(self, args: argparse.Namespace = None) -> None:
        """Create a new settings object

        Suitable default parameters are taken from environment variables.

        Args:
            args : argparse.Namespace, optional
                Command line arguments to set. Will overwrite any environment variables,
                by default None
        """
        # Create and set relation links
        urls = self._create_relation_urls()
        if urls is not None:
            self["related_identifiers"] = urls

        # Set version
        version = self._version_from_commit_tag()
        if version is not None:
            self["version"] = version

        # Set zenodo_token
        if "zenodo_token" in os.environ:
            self["zenodo_token"] = os.environ["zenodo_token"]
        # Set zenodo_record
        if "zenodo_record" in os.environ:
            self["zenodo_record"] = os.environ["zenodo_record"]

        # We add the arguments last to allow other parameters than the environment variables.
        # Command line args are none if not set, but we shouldn't update with 'None'
        if args is not None:
            self.update({k: v for k, v in vars(args).items() if v is not None})

    def _create_relation_urls(self) -> list:
        """Create URLs for the attribute 'related_identifiers' of the zenodo
        metadata field

        Currently, only the URLs for 'isIdenticalTo' and 'isCompiledBy' are
        created from the commit tag or sha and the project URL. The values are
        taken from the environment variables `CI_COMMIT_TAG`, `CI_COMMIT_SHA`,
        `CI_PROJECT_URL`.

        Returns:
            list
                A list of JSON formatted strings. Is None if no commit tag/sha or
                project URL exists
        """
        ret_lst = None
        if "CI_COMMIT_TAG" in os.environ:
            tag = os.environ["CI_COMMIT_TAG"]
        elif "CI_COMMIT_SHA" in os.environ:
            tag = os.environ["CI_COMMIT_SHA"]
        else:
            tag = None

        if "CI_PROJECT_URL" in os.environ and tag is not None:
            url = os.environ["CI_PROJECT_URL"]
            tag_url = url + '/-/tree/' + tag
            tag_relation = {'relation': 'isIdenticalTo', 'identifier': tag_url}
            repo_relation = {'relation': 'isCompiledBy', 'identifier': url}
            ret_lst = [tag_relation, repo_relation]

        return ret_lst

    def _version_from_commit_tag(self) -> str:
        """Extract the version number from the commit tag

        The version number is assumed to be the left most sequence of numbers
        which are separated by a full stop, given by the the regex pattern
        `([0-9]+(\\.[0-9]+)+.*)$`.

        Regex examples

        | Commit tag          | Return value    |
        |---------------------|-----------------|
        | "0.8"               | "0.8"           |
        | "v1.3"              | "1.3"           |
        | "v1.3-beta"         | "1.3-beta"      |
        | "v12.66.99.88"      | "12.66.99.88"   |
        | "test0.4.01-oddity" | "0.4.01-oddity" |

        Returns:
            str
                The version number. Is None no commit tag or pattern exist
        """
        version = None
        if "CI_COMMIT_TAG" in os.environ:
            version_regex = "([0-9]+(\\.[0-9]+)+.*)$"
            match = re.search(version_regex, os.environ["CI_COMMIT_TAG"])
            if match is not None:
                version = match.group(1)
        return version
