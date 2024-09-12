import argparse
import pytest
import os
from unittest.mock import patch, ANY


def test_setup_parser(tmp_path):
    from tuxbake.argparse import setup_parser

    assert isinstance(setup_parser(), argparse.ArgumentParser)

    """
      ( -- ) Refers to named optional arguments, i.e parser_map data can be in any order and also optional until specified as required.
    """
    build_definition = tmp_path / "oniro.json"
    build_definition.write_bytes(b'{"sources": {"kas": {}}}')
    parser_map = {
        "--build-definition": str(build_definition),
        "--runtime": "docker",
        "--image": None,
        "--src-dir": "test",
        "--build-dir-name": "build",
        "--local-manifest": None,
        "--pinned-manifest": None,
    }
    data = ["test.py"]  # adding first argument as file_name
    for key in parser_map:
        data.extend([key, parser_map[key]])
    with patch("sys.argv", data):
        data = setup_parser().parse_args()
        print(data)
        assert all(
            [
                data.build_definition == parser_map["--build-definition"],
                data.runtime == parser_map["--runtime"],
                data.image == parser_map["--image"],
                data.src_dir == os.path.abspath(parser_map["--src-dir"]),
                data.build_dir_name == parser_map["--build-dir-name"],
                data.local_manifest == parser_map["--local-manifest"],
                data.pinned_manifest == parser_map["--pinned-manifest"],
            ]
        )


def test_file_or_url(tmp_path):
    from tuxbake.argparse import file_or_url

    # case: Path to build definition file
    build_definition = tmp_path / "build-definition.json"
    build_definition.write_text("sample build definition file")
    assert file_or_url(build_definition) == build_definition

    # case: URL build definition file
    build_definition = "https:://path/to/definition_file.json"
    with patch("tuxbake.argparse.download_file") as download_file:
        download_file.return_value = tmp_path
        assert file_or_url(build_definition) == tmp_path
        assert download_file.call_count == 1
        download_file.assert_called_once_with(build_definition, ANY)

    # case: invalid path
    build_definition = "/tmp/definition.json"
    with pytest.raises(argparse.ArgumentTypeError):
        file_or_url(build_definition)

    # case: invalid URL scheme
    build_definition = "www.example.com/file/definition.json"
    with pytest.raises(argparse.ArgumentTypeError):
        file_or_url(build_definition)
