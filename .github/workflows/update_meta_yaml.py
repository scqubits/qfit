#!/usr/bin/env python3
import os
import re
import sys
import requests
import hashlib

def get_latest_version():
    ref = os.getenv("GITHUB_REF")
    if not ref:
        print("Error: GITHUB_REF environment variable not set. Pass the tag or run in GitHub Actions.")
        sys.exit(1)
    tag = ref.split('/')[-1]
    version = tag[1:] if tag.startswith("v") else tag
    return version

def get_sha256(url):
    print(f"Downloading tarball from: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    hash_sha256 = hashlib.sha256()
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            hash_sha256.update(chunk)
    computed_hash = hash_sha256.hexdigest()
    print(f"Computed sha256: {computed_hash}")
    return computed_hash

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
        new_version = get_latest_version()
    name = "qfit"
    tarball_url = f"https://pypi.org/packages/source/{name[0]}/{name}/qfit-{new_version}.tar.gz"
    new_sha256 = get_sha256(tarball_url)
    update_meta_yaml(new_version, new_sha256)

if __name__ == "__main__":
    main()