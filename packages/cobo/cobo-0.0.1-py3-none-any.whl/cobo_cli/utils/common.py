import json
import os
import zipfile
from pathlib import Path
from typing import Union

import click
import requests


def is_response_success(body: Union[str, dict], stdout: bool = False) -> bool:
    if isinstance(body, str):
        body = json.loads(body)

    is_success = body.get("success", False)
    if not is_success and stdout:
        click.echo(
            f"Error creating auth. "
            f"error_code={body.get('error_code')}, "
            f"error_message={body.get('error_message')}, "
            f"error_id={body.get('error_id')}",
            err=True,
            color=True,
        )
    return is_success


def download_file(url: str, directory: str = None):
    local_filename = url.split('/')[-1]
    if directory is None:
        path = os.environ.get("COBO_ENV", f"{Path.home()}/.cobo/{local_filename}")
    else:
        path = f"{directory}/{local_filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return path


def extract_file(file_path: str, directory: str):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        root_dirs = []
        for f in zip_ref.namelist():
            info = zip_ref.getinfo(f)
            if info.is_dir():
                r_dir = f.split('/')
                r_dir = r_dir[0]
                if r_dir not in root_dirs:
                    root_dirs.append(r_dir)
        if len(root_dirs) == 1:
            root_dir = root_dirs[0].rstrip("/")
            for info in zip_ref.infolist():
                if info.filename.rstrip("/") != root_dir and info.filename.startswith(root_dir + "/"):
                    info.filename = info.filename[len(root_dir + "/"):]
                    zip_ref.extract(info, directory)
        else:
            zip_ref.extractall(directory)
