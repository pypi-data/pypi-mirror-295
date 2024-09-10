import math
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import Dict, List

import backoff
import requests
from tqdm import tqdm

from lightning_sdk.lightning_cloud.openapi import (
    ModelsStoreApi,
    ProjectIdStorageBody,
    StorageCompleteBody,
    UploadIdCompleteBody,
    UploadIdPartsBody,
    UploadsUploadIdBody,
    V1CompletedPart,
    V1CompleteUpload,
    V1PresignedUrl,
    V1SignedUrl,
    V1UploadProjectArtifactPartsResponse,
    V1UploadProjectArtifactResponse,
    VersionUploadsBody,
)
from lightning_sdk.lightning_cloud.rest_client import LightningClient
from lightning_sdk.machine import Machine


class _DummyBody:
    def __init__(self) -> None:
        self.swagger_types = {}
        self.attribute_map = {}


_BYTES_PER_KB = 1000
_BYTES_PER_MB = 1000 * _BYTES_PER_KB
_BYTES_PER_GB = 1000 * _BYTES_PER_MB

_SIZE_LIMIT_SINGLE_PART = 5 * _BYTES_PER_GB
_MAX_SIZE_MULTI_PART_CHUNK = 100 * _BYTES_PER_MB
_MAX_BATCH_SIZE = 50
_MAX_WORKERS = 10


class _FileUploader:
    """A class handling the upload to studios.

    Supports both single part and parallelized multi part uploads

    """

    def __init__(
        self,
        client: LightningClient,
        teamspace_id: str,
        cluster_id: str,
        file_path: str,
        remote_path: str,
        progress_bar: bool,
    ) -> None:
        self.client = client
        self.teamspace_id = teamspace_id
        self.cluster_id = cluster_id

        self.local_path = file_path

        self.remote_path = remote_path
        self.multipart_threshold = int(os.environ.get("LIGHTNING_MULTIPART_THRESHOLD", _MAX_SIZE_MULTI_PART_CHUNK))
        self.filesize = os.path.getsize(file_path)
        if progress_bar:
            self.progress_bar = tqdm(
                desc=f"Uploading {os.path.split(file_path)[1]}",
                total=self.filesize,
                unit="B",
                unit_scale=True,
                unit_divisor=1000,
            )
        else:
            self.progress_bar = None
        self.chunk_size = int(os.environ.get("LIGHTNING_MULTI_PART_PART_SIZE", _MAX_SIZE_MULTI_PART_CHUNK))
        assert self.chunk_size < _SIZE_LIMIT_SINGLE_PART
        self.max_workers = int(os.environ.get("LIGHTNING_MULTI_PART_MAX_WORKERS", _MAX_WORKERS))
        self.batch_size = int(os.environ.get("LIGHTNING_MULTI_PART_BATCH_SIZE", _MAX_BATCH_SIZE))

    def __call__(self) -> None:
        """Does the actual uploading.

        Dispatches to single and multipart uploads respectively

        """
        count = 1 if self.filesize <= self.multipart_threshold else math.ceil(self.filesize / self.chunk_size)

        return self._multipart_upload(count=count)

    def _multipart_upload(self, count: int) -> None:
        """Does a parallel multipart upload."""
        body = ProjectIdStorageBody(cluster_id=self.cluster_id, filename=self.remote_path)
        resp: V1UploadProjectArtifactResponse = self.client.lightningapp_instance_service_upload_project_artifact(
            body=body, project_id=self.teamspace_id
        )

        # get indices for each batch, part numbers start at 1
        batched_indices = [
            list(range(i + 1, min(i + self.batch_size + 1, count + 1))) for i in range(0, count, self.batch_size)
        ]

        completed: List[V1CompleteUpload] = []
        with ThreadPoolExecutor(self.max_workers) as p:
            for batch in batched_indices:
                completed.extend(self._process_upload_batch(executor=p, batch=batch, upload_id=resp.upload_id))

        completed_body = StorageCompleteBody(
            cluster_id=self.cluster_id, filename=self.remote_path, parts=completed, upload_id=resp.upload_id
        )
        self.client.lightningapp_instance_service_complete_upload_project_artifact(
            body=completed_body, project_id=self.teamspace_id
        )

    def _process_upload_batch(self, executor: ThreadPoolExecutor, batch: List[int], upload_id: str) -> None:
        """Uploads a single batch of chunks in parallel."""
        urls = self._request_urls(parts=batch, upload_id=upload_id)
        func = partial(self._handle_uploading_single_part, upload_id=upload_id)
        return executor.map(func, urls)

    def _request_urls(self, parts: List[int], upload_id: str) -> List[V1PresignedUrl]:
        """Requests urls for a batch of parts."""
        body = UploadsUploadIdBody(cluster_id=self.cluster_id, filename=self.remote_path, parts=parts)
        resp: V1UploadProjectArtifactPartsResponse = (
            self.client.lightningapp_instance_service_upload_project_artifact_parts(body, self.teamspace_id, upload_id)
        )
        print(resp.urls)
        return resp.urls

    def _handle_uploading_single_part(self, presigned_url: V1PresignedUrl, upload_id: str) -> V1CompleteUpload:
        """Uploads a single part of a multipart upload including retires with backoff."""
        try:
            return self._handle_upload_presigned_url(
                presigned_url=presigned_url,
            )
        except Exception:
            return self._error_handling_upload(part=presigned_url.part_number, upload_id=upload_id)

    def _handle_upload_presigned_url(self, presigned_url: V1PresignedUrl) -> V1CompleteUpload:
        """Straightforward uploads the part given a single url."""
        with open(self.local_path, "rb") as f:
            f.seek((int(presigned_url.part_number) - 1) * self.chunk_size)
            data = f.read(self.chunk_size)

        response = requests.put(presigned_url.url, data=data)
        response.raise_for_status()
        if self.progress_bar is not None:
            self.progress_bar.update(self.chunk_size)

        etag = response.headers.get("ETag")
        return V1CompleteUpload(etag=etag, part_number=presigned_url.part_number)

    @backoff.on_exception(backoff.expo, (requests.exceptions.HTTPError), max_tries=10)
    def _error_handling_upload(self, part: int, upload_id: str) -> V1CompleteUpload:
        """Retries uploading with re-requesting the url."""
        urls = self._request_urls(
            parts=[part],
            upload_id=upload_id,
        )
        if len(urls) != 1:
            raise ValueError(
                f"expected to get exactly one url, but got {len(urls)} for part {part} of {self.remote_path}"
            )

        return self._handle_upload_presigned_url(presigned_url=urls[0])


class _ModelFileUploader:
    """A class handling the upload of model artifacts.

    Supports parallelized multi-part uploads.

    """

    def __init__(
        self,
        client: LightningClient,
        model_id: str,
        version: str,
        teamspace_id: str,
        cluster_id: str,
        file_path: str,
        remote_path: str,
        progress_bar: bool,
    ) -> None:
        self.client = client
        self.model_id = model_id
        self.version = version
        self.teamspace_id = teamspace_id
        self.cluster_id = cluster_id
        self.local_path = file_path
        self.remote_path = remote_path

        self.api = ModelsStoreApi(client.api_client)
        self.multipart_threshold = int(os.environ.get("LIGHTNING_MULTIPART_THRESHOLD", _MAX_SIZE_MULTI_PART_CHUNK))
        self.filesize = os.path.getsize(file_path)
        if progress_bar:
            self.progress_bar = tqdm(
                desc=f"Uploading {os.path.split(file_path)[1]}",
                total=self.filesize,
                unit="B",
                unit_scale=True,
                unit_divisor=1000,
            )
        else:
            self.progress_bar = None
        self.chunk_size = int(os.environ.get("LIGHTNING_MULTI_PART_PART_SIZE", _MAX_SIZE_MULTI_PART_CHUNK))
        assert self.chunk_size < _SIZE_LIMIT_SINGLE_PART
        self.max_workers = int(os.environ.get("LIGHTNING_MULTI_PART_MAX_WORKERS", _MAX_WORKERS))
        self.batch_size = int(os.environ.get("LIGHTNING_MULTI_PART_BATCH_SIZE", _MAX_BATCH_SIZE))

    def __call__(self) -> None:
        """Does the actual uploading."""
        count = 1 if self.filesize <= self.multipart_threshold else math.ceil(self.filesize / self.chunk_size)
        return self._multipart_upload(count=count)

    def _multipart_upload(self, count: int) -> None:
        """Does a parallel multipart upload."""
        body = VersionUploadsBody(filepath=self.remote_path)
        resp = self.api.models_store_create_multi_part_upload(
            body,
            project_id=self.teamspace_id,
            model_id=self.model_id,
            version=self.version,
        )

        # get indices for each batch, part numbers start at 1
        batched_indices = [
            list(range(i + 1, min(i + self.batch_size + 1, count + 1))) for i in range(0, count, self.batch_size)
        ]

        completed: List[V1CompletedPart] = []
        with ThreadPoolExecutor(self.max_workers) as p:
            for batch in batched_indices:
                completed.extend(self._process_upload_batch(executor=p, batch=batch, upload_id=resp.upload_id))

        completed_body = UploadIdCompleteBody(filepath=self.remote_path, parts=completed)
        self.api.models_store_complete_multi_part_upload(
            completed_body,
            project_id=self.teamspace_id,
            model_id=self.model_id,
            version=self.version,
            upload_id=resp.upload_id,
        )

    def _process_upload_batch(self, executor: ThreadPoolExecutor, batch: List[int], upload_id: str) -> None:
        """Uploads a single batch of chunks in parallel."""
        urls = self._request_urls(parts=batch, upload_id=upload_id)
        func = partial(self._handle_uploading_single_part, upload_id=upload_id)
        return executor.map(func, urls)

    def _request_urls(self, parts: List[int], upload_id: str) -> List[V1SignedUrl]:
        """Requests urls for a batch of parts."""
        body = UploadIdPartsBody(filepath=self.remote_path, parts=parts)
        resp = self.api.models_store_get_model_file_upload_urls(
            body,
            project_id=self.teamspace_id,
            model_id=self.model_id,
            version=self.version,
            upload_id=upload_id,
        )
        return resp.urls

    def _handle_uploading_single_part(self, presigned_url: V1SignedUrl, upload_id: str) -> V1CompletedPart:
        """Uploads a single part of a multipart upload including retires with backoff."""
        try:
            return self._handle_upload_presigned_url(
                presigned_url=presigned_url,
            )
        except Exception:
            return self._error_handling_upload(part=presigned_url.part_number, upload_id=upload_id)

    def _handle_upload_presigned_url(self, presigned_url: V1SignedUrl) -> V1CompletedPart:
        """Straightforward uploads the part given a single url."""
        with open(self.local_path, "rb") as f:
            f.seek((int(presigned_url.part_number) - 1) * self.chunk_size)
            data = f.read(self.chunk_size)

        response = requests.put(presigned_url.url, data=data)
        response.raise_for_status()
        if self.progress_bar is not None:
            self.progress_bar.update(self.chunk_size)

        etag = response.headers.get("ETag")
        return V1CompletedPart(etag=etag, part_number=presigned_url.part_number)

    @backoff.on_exception(backoff.expo, (requests.exceptions.HTTPError), max_tries=10)
    def _error_handling_upload(self, part: int, upload_id: str) -> V1CompletedPart:
        """Retries uploading with re-requesting the url."""
        urls = self._request_urls(
            parts=[part],
            upload_id=upload_id,
        )
        if len(urls) != 1:
            raise ValueError(
                f"expected to get exactly one url, but got {len(urls)} for part {part} of {self.remote_path}"
            )

        return self._handle_upload_presigned_url(presigned_url=urls[0])


class _DummyResponse:
    def __init__(self, data: bytes) -> None:
        self.data = data


# TODO: This should really come from some kind of metadata service
_MACHINE_TO_COMPUTE_NAME: Dict[Machine, str] = {
    Machine.CPU_SMALL: "m3.medium",
    Machine.CPU: "cpu-4",
    Machine.DATA_PREP: "data-large-3000",
    Machine.DATA_PREP_MAX: "data-max-3000",
    Machine.DATA_PREP_ULTRA: "data-ultra-3000",
    Machine.T4: "g4dn.2xlarge",
    Machine.T4_X_4: "g4dn.12xlarge",
    Machine.L4: "g6.4xlarge",
    Machine.L4_X_4: "g6.12xlarge",
    Machine.L4_X_8: "g6.48xlarge",
    Machine.A10G: "g5.8xlarge",
    Machine.A10G_X_4: "g5.12xlarge",
    Machine.A10G_X_8: "g5.48xlarge",
    Machine.L40: "6e.4xlarge",
    Machine.L40_X_4: "g6e.12xlarge",
    Machine.L40_X_8: "g6e.48xlarge",
    Machine.A100_X_8: "p4d.24xlarge",
    Machine.H100_X_8: "p5.48xlarge",
}

_COMPUTE_NAME_TO_MACHINE: Dict[str, Machine] = {v: k for k, v in _MACHINE_TO_COMPUTE_NAME.items()}

_DEFAULT_CLOUD_URL = "https://lightning.ai:443"


def _get_cloud_url() -> str:
    cloud_url = os.environ.get("LIGHTNING_CLOUD_URL", _DEFAULT_CLOUD_URL)
    os.environ["LIGHTNING_CLOUD_URL"] = cloud_url
    return cloud_url


def _sanitize_studio_remote_path(path: str, studio_id: str) -> str:
    return f"/cloudspaces/{studio_id}/code/content/{path.replace('/teamspace/studios/this_studio/', '')}"


def _download_model_files(
    client: LightningClient,
    name: str,
    version: str,
    download_dir: Path,
    progress_bar: bool,
) -> List[str]:
    api = ModelsStoreApi(client.api_client)
    response = api.models_store_get_model_files(name=name, version=version)

    if progress_bar:
        pbar = tqdm(
            desc=f"Downloading {version}",
            unit="B",
            unit_scale=True,
            unit_divisor=1000,
        )

        pbar_update = pbar.update
    else:
        pbar_update = lambda x: None

    for filepath in response.filepaths:
        url_response = api.models_store_get_model_file_url(
            project_id=response.project_id,
            model_id=response.model_id,
            version=response.version,
            filepath=filepath,
        )
        r = requests.get(url_response.url, stream=True)
        local_file = download_dir / filepath
        local_file.parent.mkdir(parents=True, exist_ok=True)
        with open(local_file, "wb") as file:
            for chunk in r.iter_content(chunk_size=(4096 * 8)):
                file.write(chunk)
                pbar_update(len(chunk))

    return response.filepaths
