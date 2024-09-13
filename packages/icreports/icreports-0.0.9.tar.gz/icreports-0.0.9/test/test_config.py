import os
from pathlib import Path

from icreports.document import DocumentConfig

def get_test_data_dir():
    return Path(__file__).parent / "data"

def test_config():

    config_file = get_test_data_dir() / "mock_document/_config.yml"

    config = DocumentConfig()
    config.read(config_file)

    config_out = Path(os.getcwd()) / "config_out.yml"
    config.write(config_out)

    config1 = DocumentConfig()
    config1.read(config_out)

    assert config.project_name == config1.project_name

    config_out.unlink()
