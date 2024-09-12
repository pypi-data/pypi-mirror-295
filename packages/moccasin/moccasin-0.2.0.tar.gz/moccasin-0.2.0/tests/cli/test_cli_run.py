from pathlib import Path
import subprocess
import os
from tests.utils.anvil import AnvilProcess, ANVIL_URL
from tests.conftest import (
    COMPLEX_PROJECT_PATH,
    ANVIL1_PRIVATE_KEY,
    ANVIL1_KEYSTORE_NAME,
    ANVIL1_KEYSTORE_PASSWORD,
)
from web3 import Web3


def test_run_help(mox_path):
    current_dir = Path.cwd()
    try:
        os.chdir(COMPLEX_PROJECT_PATH)
        result = subprocess.run(
            [mox_path, "run", "-h"], check=True, capture_output=True, text=True
        )
    finally:
        os.chdir(current_dir)
    assert "Moccasin CLI run" in result.stdout


def test_run_default(mox_path):
    current_dir = Path.cwd()
    try:
        os.chdir(COMPLEX_PROJECT_PATH)
        result = subprocess.run(
            [mox_path, "run", "deploy"], check=True, capture_output=True, text=True
        )
    finally:
        os.chdir(current_dir)
    assert "Ending count:  1" in result.stdout


def test_run_with_network(mox_path):
    current_dir = Path.cwd()
    os.chdir(COMPLEX_PROJECT_PATH)
    try:
        with AnvilProcess():
            result = subprocess.run(
                [
                    mox_path,
                    "run",
                    "deploy",
                    "--network",
                    "anvil",
                    "--private-key",
                    ANVIL1_PRIVATE_KEY,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
    finally:
        os.chdir(current_dir)
    assert "Ending count:  1" in result.stdout
    assert "tx broadcasted" in result.stdout
    assert result.returncode == 0


def test_run_with_keystore_account(mox_path, anvil_keystore):
    current_dir = Path.cwd()
    os.chdir(COMPLEX_PROJECT_PATH)
    try:
        with AnvilProcess():
            result = subprocess.run(
                [
                    mox_path,
                    "run",
                    "deploy",
                    "--network",
                    "anvil",
                    "--account",
                    ANVIL1_KEYSTORE_NAME,
                    "--password",
                    ANVIL1_KEYSTORE_PASSWORD,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
    finally:
        os.chdir(current_dir)
    assert "Ending count:  1" in result.stdout
    assert "tx broadcasted" in result.stdout
    assert result.returncode == 0


def test_run_fork_should_not_send_transactions(mox_path, anvil_fork):
    current_dir = Path.cwd()
    os.chdir(COMPLEX_PROJECT_PATH)
    try:
        with AnvilProcess():
            w3 = Web3(Web3.HTTPProvider(ANVIL_URL))
            starting_block = w3.eth.get_block("latest").number
            result = subprocess.run(
                [mox_path, "run", "deploy", "--fork", "--network", "fake_chain"],
                check=True,
                capture_output=True,
                text=True,
            )
            ending_block = w3.eth.get_block("latest").number
    finally:
        os.chdir(current_dir)
    assert "Ending count:  1" in result.stdout
    assert "tx broadcasted" not in result.stdout
    assert starting_block == ending_block
    assert result.returncode == 0
