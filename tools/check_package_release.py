"""Determine if new package should be release (based on version) and consequently write information to env."""
import os
import subprocess
import sys

from security import safe_requests

AVAILABLE_PACKAGES = ["vizro-core", "vizro-ai"]
VERSION_MATCHSTR = r'\s*__version__\s*=\s*"(\d+\.\d+\.\d+)"'
RESPONSE_ERROR = 404


def _check_no_version_pypi(package_name, package_version):
    """Checks if a given package version exists on PyPI and returns a boolean value indicating whether the package should be released or not.
    Parameters:
        - package_name (str): The name of the package to be checked.
        - package_version (str): The version of the package to be checked.

    Returns:
        - bool: True if the package should be released, False if it already exists on PyPI.
    Processing Logic:
        - Generates the PyPI endpoint based on the package name and version.
        - Sends a request to the endpoint and checks the response status code.
        - If the status code indicates an error, the package should be released.
    - If the status code is successful, the package already exists on PyPI and should not be released.
    """
    if package_name == "vizro-core":
        pypi_endpoint = f"https://pypi.org/pypi/vizro/{package_version}/json/"
    else:
        pypi_endpoint = f"https://pypi.org/pypi/{package_name}/{package_version}/json/"
    response = safe_requests.get(pypi_endpoint, timeout=10)
    if response.status_code == RESPONSE_ERROR:
        # Version doesn't exist on Pypi - do release
        print(f"Potential release of {package_name} {package_version}")  # noqa: T201
        return True
    else:
        print(f"Skipped: {package_name} {package_version} already exists on PyPI")  # noqa: T201
        return False


def _check_no_dev_version(package_name, package_version):
    """"""

    if "dev" not in package_version:
        return True
    else:
        print(f"Skipped: {package_name} {package_version} is still under development")  # noqa: T201
        return False


if __name__ == "__main__":
    package_name = "dummy_package"
    package_version = "0.0.0"
    new_release = False
    env_file = str(os.getenv("GITHUB_ENV"))

    for attempted_package_name in AVAILABLE_PACKAGES:
        attempted_package_version = (
            subprocess.check_output(["hatch", "version"], cwd=f"{attempted_package_name}").decode("utf-8").strip()
        )

        if _check_no_dev_version(attempted_package_name, attempted_package_version) and _check_no_version_pypi(
            attempted_package_name, attempted_package_version
        ):
            if new_release:
                sys.exit("Cannot release two packages at the same time. Please modify your PR.")
            new_release = True
            package_name = attempted_package_name
            package_version = attempted_package_version

    with open(env_file, "a") as f:
        f.write(f"NEW_RELEASE={new_release!s}\n")
        if new_release:
            f.write(f"PACKAGE_NAME={package_name}\nPACKAGE_VERSION={package_version}\n")
