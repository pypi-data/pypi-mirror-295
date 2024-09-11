from pathlib import Path

import pytest

from halig.settings import Settings, load_from_file


def test_settings_from_env(settings: Settings, notebooks_root_path_envvar):
    from_env_settings = Settings(recipient_paths=settings.recipient_paths,
                                 identity_paths=settings.identity_paths)  # type: ignore[call-arg]
    assert from_env_settings.notebooks_root_path == settings.notebooks_root_path


def test_settings_from_non_existing_file_raises_value_error():
    with pytest.raises(ValueError, match="Field required"):
        Settings()  # type: ignore[call-arg]


def test_load_from_file(notebooks_path: Path, settings_file_path: Path):
    settings = load_from_file(settings_file_path)
    assert settings.notebooks_root_path == notebooks_path


def test_load_from_empty_file_raises_value_error(empty_file_path: Path):
    with pytest.raises(ValueError, match=f"File {empty_file_path} is empty"):
        load_from_file(empty_file_path)


def test_load_from_non_existing_file_path_raises_file_not_found_error(halig_config_path: Path):
    file = halig_config_path / "some_invalid_file.yml"
    with pytest.raises(FileNotFoundError, match=f"File {file} does not exist"):
        load_from_file(file)


def test_settings_identity_paths_is_not_list_is_converted(settings):
    s = Settings(identity_paths=settings.identity_paths[0], recipient_paths=settings.recipient_paths[0],
                 notebooks_root_path=settings.notebooks_root_path)
    assert s.identity_paths == [settings.identity_paths[0]]
    assert s.recipient_paths == [settings.recipient_paths[0]]
