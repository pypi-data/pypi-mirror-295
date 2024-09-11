#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pathlib
from io import StringIO
from unittest import TestCase
from unittest.mock import mock_open, patch

from gitlab2zenodo import main
from gitlab2zenodo.settings import Settings
import contextlib

class TestMain(TestCase):

    @patch('sys.stderr', new_callable=StringIO)
    @patch('builtins.open', new_callable=mock_open())
    @patch('gitlab2zenodo.main.get_metadata', return_value={"metadata": {"value_a": "A"}})
    def test_g2z_meta_command(self, mock_get_meta, mock_open_file, captured_stderr):
        test_cmd = [
            # Run test with positional ID and given ID
            "g2z-get-meta -t a_token an_id",
            "g2z-get-meta --token a_token an_id",
            "g2z-get-meta -i an_id -t a_token",
            "g2z-get-meta --id an_id --token a_token",
            "g2z-get-meta -i an_id -t a_token id_not_stored", ]
        for cmd in test_cmd:
            with contextlib.redirect_stdout(StringIO()):
                with patch("sys.argv", cmd.split()):
                    main.g2z_meta_command()

            expect = {'zenodo_token': 'a_token',
                      'zenodo_record': 'an_id',
                      'sandbox': False,
                      'out_file': 'stdout'}
            settings = Settings()
            settings.update(expect)
            mock_get_meta.assert_called_with(settings=settings)

        # Test setting the sandbox flag
        cmd = "g2z-get-meta -i an_id -t a_token -s"
        with patch("sys.argv", cmd.split()):
            with contextlib.redirect_stdout(StringIO()):
                main.g2z_meta_command()

        expect = {'zenodo_token': 'a_token',
                  'zenodo_record': 'an_id',
                  'sandbox': True,
                  'out_file': 'stdout'}
        settings = Settings()
        settings.update(expect)
        mock_get_meta.assert_called_with(settings=settings)

        # Test file output
        cmd = "g2z-get-meta -i an_id -t a_token -s -o out_file"
        with patch("sys.argv", cmd.split()):
            main.g2z_meta_command()
            mock_open_file.assert_called_once_with('out_file', 'w', encoding='utf-8')

        expect = {'zenodo_token': 'a_token',
                  'zenodo_record': 'an_id',
                  'sandbox': True,
                  'out_file': 'out_file'}
        settings = Settings()
        settings.update(expect)
        mock_get_meta.assert_called_with(settings=settings)

        # Error when missing named or positional ID
        cmd = "g2z-get-meta"

        with patch("sys.argv", cmd.split()):
            with self.assertRaises(SystemExit):
                main.g2z_meta_command()
            self.assertIn("Gitlab2Zenodo: get zenodo metadata",
                          captured_stderr.getvalue())

    @patch('gitlab2zenodo.main.send')
    def test_g2z_command(self, mock_send):
        base_expect = {'archive': pathlib.Path('archive.zip'),
                       'metadata': pathlib.Path('.zenodo.json'),
                       'publish': False,
                       'sandbox': False,
                       'zenodo_record': 'an_id',
                       'zenodo_token': 'a_token'}
        test_cmd = [
            "g2z-send -i an_id -t a_token archive.zip",
            "g2z-send --id an_id -t a_token archive.zip",
            "g2z-send -i an_id --token a_token archive.zip",
            "g2z-send -i an_id -t a_token -v 1.0.0 archive.zip",
            "g2z-send -i an_id -t a_token -s archive.zip",
            "g2z-send -i an_id -t a_token --sandbox archive.zip",
            "g2z-send -i an_id -t a_token -p archive.zip",
            "g2z-send -i an_id -t a_token --publish archive.zip",
            "g2z-send -i an_id -t a_token -m my_meta archive.zip",
            "g2z-send -i an_id -t a_token --metadata my_meta archive.zip",
            "g2z-send archive.zip"
        ]
        test_expect = [
            {}, {}, {},
            {"version": "1.0.0"},
            {"sandbox": True}, {"sandbox": True},
            {"publish": True}, {"publish": True},
            {'metadata': pathlib.Path('my_meta')}, {
                'metadata': pathlib.Path('my_meta')},
            {'zenodo_record': None, 'zenodo_token': None}
        ]

        for cmd, expect_base_add in zip(test_cmd, test_expect):
            with patch("sys.argv", cmd.split()):
                main.g2z_command()

            expect = base_expect.copy()
            expect.update(expect_base_add)
            # Settings contain no entries = None
            expect = {k: v for k, v in expect.items() if v is not None}

            settings = Settings()
            settings.update(expect)
            mock_send.assert_called_with(settings=settings)

    @patch('gitlab2zenodo.main.send')
    @patch('gitlab2zenodo.main.get_metadata', return_value={"metadata": {"value_a": "A"}})
    def test_g2z_env_vars(self, mock_get_meta, mock_send):
        os.environ["zenodo_token"] = "a_token"
        os.environ["zenodo_record"] = "an_id"

        cmd = "g2z-get-meta -i an_id"
        with patch("sys.argv", cmd.split()):
            with contextlib.redirect_stdout(StringIO()):
                main.g2z_meta_command()
            expect = {'zenodo_token': 'a_token',
                      'zenodo_record': 'an_id',
                      'sandbox': False,
                      'out_file': 'stdout'}
            settings = Settings()
            settings.update(expect)
            mock_get_meta.assert_called_once_with(settings=settings)

        cmd = "g2z-send archive.zip"
        with patch("sys.argv", cmd.split()):
            main.g2z_command()

        expect = {'archive': pathlib.Path('archive.zip'),
                  'metadata': pathlib.Path('.zenodo.json'),
                  'publish': False,
                  'sandbox': False,
                  'zenodo_record': 'an_id',
                  'zenodo_token': 'a_token'}
        settings = Settings()
        settings.update(expect)
        mock_send.assert_called_once_with(settings=settings)
