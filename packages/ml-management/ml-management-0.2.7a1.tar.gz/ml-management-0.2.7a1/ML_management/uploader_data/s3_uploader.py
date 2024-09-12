"""Define S3Uploader class."""
import asyncio
import os
import posixpath
import threading
from http import HTTPStatus
from typing import List, Optional

import aioboto3
import boto3
from botocore.awsrequest import AWSRequest, AWSResponse
from tqdm.autonotebook import tqdm

from ML_management.mlmanagement import get_s3_gateway_url, variables
from ML_management.mlmanagement.mlmanager import tar_folder
from ML_management.mlmanagement.session import AuthSession
from ML_management.mlmanagement.visibility_options import VisibilityOptions
from ML_management.uploader_data.utils import get_upload_paths

MAX_TASKS_NUMBER = 50


class S3Uploader:
    """S3 uploader files class."""

    def __init__(self):
        """Init creds."""
        self.default_url = get_s3_gateway_url()
        self.default_access_key_id, self.default_secret_access_key = variables._get_s3_credentials()
        self.session = AuthSession()

    def upload(
        self,
        local_path: str,
        bucket: str,
        upload_as_tar: bool = False,
        new_bucket_visibility: VisibilityOptions = VisibilityOptions.PRIVATE,
        verbose: bool = True,
    ) -> Optional[asyncio.Task]:
        """
        Upload directory to bucket.

        Parameters
        ----------
        local_path: str
            path to directory with files you want to upload.
        bucket: str
            name of bucket you want to upload to.
        upload_as_tar: bool = False
            If the option is set to True, the files will be uploaded as a single tar archive. Default: False
        verbose: bool = True
            If the option is set to True and upload_as_tar set to False,
            a progress bar with the number of uploaded files will be displayed.

        Returns
        -------
        Optional[asyncio.Task].
            If the files uploading to the bucket is started inside an asynchronous application,
            the method will schedule the task in the running event loop and
            return instance of asyncio.Task for further process monitoring by the application
        """
        if upload_as_tar:
            self._upload_as_tar(local_path=local_path, bucket=bucket, new_bucket_visibility=new_bucket_visibility)
            return

        # in case of asyncio.run() was called previously in code, it closed event loop
        # and get_event_loop() will raise exception:
        # RuntimeError: There is no current event loop in thread <THREAD_NAME>
        try:
            if asyncio.get_event_loop().is_running():
                return asyncio.create_task(
                    self._async_upload_files(
                        local_path=local_path,
                        bucket=bucket,
                        new_bucket_visibility=new_bucket_visibility,
                        verbose=verbose,
                    )
                )
            asyncio.get_event_loop().close()
        except Exception:
            pass
        asyncio.run(
            self._async_upload_files(
                local_path=local_path, bucket=bucket, new_bucket_visibility=new_bucket_visibility, verbose=verbose
            )
        )

    def _upload_as_tar(self, local_path: str, bucket: str, new_bucket_visibility: VisibilityOptions) -> None:
        local_path = os.path.normpath(local_path)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Path: {local_path} does not exist")

        r, w = os.pipe()

        try:
            thread = threading.Thread(target=tar_folder, args=(w, local_path), daemon=True)
            thread.start()
        except Exception as err:
            os.close(r)
            os.close(w)
            raise err

        s3_client = boto3.client(
            service_name="s3",
            use_ssl=True,
            endpoint_url=posixpath.join(self.default_url, "s3/"),
            aws_access_key_id=self.default_access_key_id,
            aws_secret_access_key=self.default_secret_access_key,
        )
        event_system = s3_client.meta.events
        event_system.register("before-sign.s3.*", self._add_auth_cookies)
        event_system.register("after-call.s3.*", self._update_auth_cookies)
        buckets = self._list_buckets()
        if bucket not in buckets:
            self._create_bucket(name=bucket, visibility=new_bucket_visibility)
        try:
            with open(r, "rb") as fileobj:
                s3_client.upload_fileobj(Fileobj=fileobj, Bucket=bucket, Key=f"{os.path.basename(local_path)}.tar")
        finally:
            thread.join()

    async def _async_upload_files(
        self, local_path: str, bucket: str, new_bucket_visibility: VisibilityOptions, verbose: bool = True
    ):
        local_path = os.path.normpath(local_path)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Path: {local_path} does not exist")

        session = aioboto3.Session(
            aws_access_key_id=self.default_access_key_id, aws_secret_access_key=self.default_secret_access_key
        )
        async with session.client(
            "s3", use_ssl=True, endpoint_url=posixpath.join(self.default_url, "s3/")
        ) as s3_client:
            event_system = s3_client.meta.events
            event_system.register("before-sign.s3.*", self._add_auth_cookies)
            event_system.register("after-call.s3.*", self._update_auth_cookies)
            buckets = self._list_buckets()
            if bucket not in buckets:
                self._create_bucket(name=bucket, visibility=new_bucket_visibility)

            upload_paths = get_upload_paths(local_path)
            total_tasks = len(upload_paths)

            with tqdm(
                total=total_tasks,
                disable=not verbose,
                unit="Files",
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                current_task_num = 0
                while current_task_num < total_tasks:
                    tasks: list[asyncio.Task] = []
                    for path in upload_paths[current_task_num : current_task_num + MAX_TASKS_NUMBER]:
                        tasks.append(
                            asyncio.create_task(
                                s3_client.upload_file(Filename=path.local_path, Bucket=bucket, Key=path.storage_path)
                            )
                        )
                    await asyncio.gather(*tasks)
                    pbar.update(len(tasks))
                    current_task_num += MAX_TASKS_NUMBER

    # arguments to callback are passed like kwargs, so kwargs must be present in signature
    def _add_auth_cookies(self, request: AWSRequest, **kwargs) -> None:  # noqa
        request.headers.add_header("Cookie", self.session._get_cookie_header())

    # arguments to callback are passed like kwargs, so kwargs must be present in signature
    def _update_auth_cookies(self, http_response: AWSResponse, **kwargs) -> None:  # noqa
        cookie_header = http_response.headers.get("set-cookie")
        if cookie_header is None:
            return
        cookies: list[str] = cookie_header.split("; ")
        for cookie in cookies:
            if "kc-access" not in cookie:
                continue
            _, new_access_token = cookie.split("=", maxsplit=1)
            self.session.cookies["kc-access"] = new_access_token
            break

    def _list_buckets(self) -> List[str]:
        with self.session.get(posixpath.join(self.default_url, "list-buckets")) as response:
            buckets_info: list[dict[str, str]] = response.json()["buckets"]
            return [bucket["name"] for bucket in buckets_info]

    def _create_bucket(self, name: str, visibility: VisibilityOptions) -> None:
        with self.session.post(
            posixpath.join(self.default_url, "create-bucket"), json={"name": name, "visibility": visibility.value}
        ) as response:
            if response.status_code != HTTPStatus.CREATED:
                raise RuntimeError(f"Failed to create bucket: {response.text}")
