import pytest

from halig import utils
from halig.commands.reencrypt import ReencryptCommand


@pytest.fixture()
def reencrypt_command(settings):
    return ReencryptCommand(settings)


@pytest.mark.usefixtures("notes")
def test_reencrypt(reencrypt_command):
    reencrypt_command.run()
    for note_path in reencrypt_command.traverse():
        with note_path.open("rb") as f:
            assert reencrypt_command.encryptor.decrypt(f.read()) == b""


@pytest.mark.usefixtures("current_daily")
def test_reencrypt_warns_no_matching_key(reencrypt_command, halig_ssh_path, capfd):
    reencrypt_command.encryptor.identities = []
    reencrypt_command.run()
    out, _ = capfd.readouterr()
    assert f'because no matching keys were found, skipping ...' in out
