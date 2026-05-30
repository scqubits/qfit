#!/usr/bin/env python3
import os
import re
import sys
import requests
def get_latest_version() -> str:
    ref = os.getenv("GITHUB_REF")
    if not ref:
        print("Error: GITHUB_REF or PACKAGE_VERSION environment variable must be set.")
        sys.exit(1)
    tag = ref.split('/')[-1]
    return tag[1:] if tag.startswith("v") else tag

def get_package_version() -> str:
    version = os.getenv("PACKAGE_VERSION")
    if version:
        return version
    return get_latest_version()

def get_sdist_sha256(name: str, version: str) -> str:
    api_url = f"https://pypi.org/pypi/{name}/{version}/json"
    print(f"Fetching release metadata from: {api_url}")
    response = requests.get(api_url, timeout=30)
    response.raise_for_status()
    sdists = [
        url for url in response.json()["urls"]
        if url["packagetype"] == "sdist"
    ]
    if not sdists:
        raise RuntimeError(f"No sdist found for {name} {version} on PyPI")
    sha256 = sdists[0]["digests"]["sha256"]
    print(f"PyPI sdist sha256: {sha256}")
    return sha256

def update_meta_yaml(new_version, new_sha256, filename="meta.yaml"):
    with open(filename, "r") as f:
        content = f.read()
    content_new = re.sub(
        r'{%\s*set\s+version\s*=\s*"[^"]+"\s*%}',
        f'{{% set version = "{new_version}" %}}',
        content
    )
    content_new = re.sub(
        r'(^\s*sha256:\s*)\S+',
        lambda m: f"{m.group(1)}{new_sha256}",
        content_new,
        flags=re.MULTILINE
    )
    with open(filename, "w") as f:
        f.write(content_new)
    print(f"Updated {filename} with version {new_version} and sha256 {new_sha256}")

def main(new_version: str | None = None):
    if new_version is None:
        new_version = get_package_version()
    name = "qfit"
    new_sha256 = get_sdist_sha256(name, new_version)
    update_meta_yaml(new_version, new_sha256)

if __name__ == "__main__":
    main()