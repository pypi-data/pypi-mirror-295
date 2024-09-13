import os
import re
import io
import cv2
import time
import boto3
import base64
import asyncio
import aiohttp
import zipfile
import trimesh
import requests
import numpy as np
from typing import Dict
from botocore.config import Config
from botocore.exceptions import ClientError
from urllib.parse import quote, urlparse, unquote

def download_template_dir_s3(local, bucket, client, prefix):
    """
    params:
    - local: local path to folder in which to place files
    - bucket: s3 bucket with target contents
    - client: initialized s3 client object
    """
    keys = []
    dirs = []
    next_token = ""
    base_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != "":
            kwargs.update({"ContinuationToken": next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get("Contents")
        for i in contents:
            k = "/".join(i.get("Key").split("/")[1:])
            if k == "":
                continue
            elif k[-1] != "/":
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get("NextContinuationToken")
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))

        if not os.path.exists(dest_pathname):
            client.download_file(bucket, prefix + "/" + k, dest_pathname)

    return


def download_models(
    aws_access_key_id,
    aws_secret_access_key,
    region_name,
    models_bucket,
    models_prefix_name,
    logger,
):
    config = Config(s3={"use_accelerate_endpoint": True})
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        config=config,
    )

    try:
        logger.debug("Downloading models from S3")
        start_time = time.time()
        download_dir_s3(
            prefix=models_prefix_name,
            local="./models",
            bucket=models_bucket,
            client=s3,
        )
        logger.debug(
            f"Successfully downloaded models from S3 in {time.time() - start_time}s"
        )
        del s3
    except:
        logger.debug(
            "Error downloading models from S3",
            extra={"init error": "downloading models"},
        )


# download models from s3
def download_dir_s3(prefix, local, bucket, client):
    """
    params:
    - prefix: pattern to match in s3
    - local: local path to folder in which to place files
    - bucket: s3 bucket with target contents
    - client: initialized s3 client object
    """
    keys = []
    dirs = []
    next_token = ""
    base_kwargs = {
        "Bucket": bucket,
        "Prefix": prefix,
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != "":
            kwargs.update({"ContinuationToken": next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get("Contents")
        for i in contents:
            k = i.get("Key")
            if k[-1] != "/":
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get("NextContinuationToken")

    for k in keys:
        dest_pathname = os.path.join(local, os.path.basename(k))
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        if not os.path.exists(dest_pathname):
            client.download_file(bucket, k, dest_pathname)
    return


def download_templates(
    aws_access_key_id,
    aws_secret_access_key,
    region_name,
    templates_bucket,
    templates_prefix_name,
    logger,
):
    config = Config(s3={"use_accelerate_endpoint": True})
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
        config=config,
    )
    try:
        logger.debug("Downloading templates from S3")
        start_time = time.time()
        download_template_dir_s3(
            local=".", bucket=templates_bucket, prefix=templates_prefix_name, client=s3
        )
        logger.debug(
            f"Successfully downloaded templates from S3 in {time.time() - start_time}s"
        )
    except Exception as e:
        logger.debug("Error downloading templates from S3", exc_info=True)
    finally:
        s3.close()

def check_object_exists(s3_client, bucket_name, object_name):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
        return True  # The object exists
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False  # The object does not exist
        else:
            raise  # An unexpected error occurred


def get_signed_url_local_file_s3(
    local_file_path, bucket_name, object_name, aws_access_key_id, aws_secret_access_key, region_name, ExpiresIn=3600
):
    if "None" in object_name:
        return ""

    session = boto3.Session(
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
        region_name=region_name,
    )

    s3_client = session.client("s3")
    presigned_url = None
    try:
        if not check_object_exists(s3_client, bucket_name, object_name):
            print(f"Uploading file {object_name} as it does not exist..")
            s3_client.upload_file(local_file_path, bucket_name, object_name)

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=ExpiresIn,
        )
    except ClientError as e:
        print("Error:", e)

    return presigned_url


def get_signed_url_write(
    obj_name, aws_access_key_id, aws_secret_access_key, region_name, field_name=None, bucket_path="", ExpiresIn=3600
):
    session = boto3.Session(
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
        region_name=region_name,
    )
    s3_client = session.client("s3")
    key = obj_name + "_" + field_name if field_name else obj_name
    return s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket_path, "Key": key},
        ExpiresIn=ExpiresIn,
    )


def get_signed_url_read(
    obj_name, aws_access_key_id, aws_secret_access_key, region_name, field_name=None, bucket_path="", ExpiresIn=3600
):
    session = boto3.Session(
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
        region_name=region_name,
    )
    s3_client = session.client("s3")
    key = obj_name + "_" + field_name if field_name else obj_name
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_path, "Key": key},
        ExpiresIn=ExpiresIn,
    )


def upload_object_s3(obj_name, binary_obj, bucket, aws_access_key_id, aws_secret_access_key, region_name):
    session = boto3.Session(
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
        region_name=region_name,
    )
    s3_client = session.client("s3")
    s3_client.put_object(Body=binary_obj, Bucket=bucket, Key=obj_name)


def upload_with_presigned_url(obj_to_upload: object, presigned_write_url: str, headers: dict = None):
    requests.put(presigned_write_url, data=obj_to_upload, headers=headers)


def parse_s3_url(s3_url, aws_region):
    clean_url = s3_url.split("?")[0]
    clean_url = re.sub(f".s3.{aws_region}.amazonaws.com", "", clean_url)
    path_parts = re.sub("https://|.s3.amazonaws.com", "", clean_url).split("/")
    bucket = path_parts.pop(0)
    job_directory = "/".join(path_parts[:-1])
    key = "/".join(path_parts)
    return bucket, key, job_directory


def list_s3_objects(bucket, aws_access_key_id, aws_secret_access_key, region_name):
    session = boto3.Session(
        aws_secret_access_key=aws_secret_access_key,
        aws_access_key_id=aws_access_key_id,
        region_name=region_name,
    )
    s3_client = session.client("s3")
    objects = s3_client.list_objects(Bucket=bucket)["Contents"]
    return objects


async def upload_image_to_presigned_s3_url(
    presigned_url, input_image, timeout_seconds=10, max_retries=4, logger=None, extra_params={}, is_local=False, compress=0
):
    if input_image is None:
        logger.warning("Nothing saved.. image is NONE", extra=extra_params)
        return

    if is_local:
        cv2.imwrite(presigned_url, input_image)
    else:
        try:
            encoded_signed_url = quote(presigned_url, safe=":/?=&%")
            retry_count = 0
            while retry_count < max_retries:
                try:
                    image = np.ascontiguousarray(input_image)
                    _, buffer = cv2.imencode(".png" if compress == 0 else ".jpg", image)
                    image = base64.b64decode(base64.b64encode(buffer))
                    response = requests.put(presigned_url, data=image, headers={"Content-Type": "image/jpeg"}, timeout=timeout_seconds)
                    if response.status_code == 200:
                        logger.info("File uploaded successfully with requests.", extra=extra_params)
                        return
                    else:
                        raise Exception(f"Upload failed with non-200 status code: {response.status_code}")
                except Exception as e:
                    logger.info(f"Upload failed. Error: {e}", extra=extra_params)

                retry_count += 1
                if retry_count < max_retries:
                    logger.info(f"Retrying ({retry_count}/{max_retries})... URL: {presigned_url}", extra=extra_params)
                time.sleep(1)
            raise Exception("Upload failed after maximum retries.")
        except Exception as e:
            logger.error(f"Upload failed after {max_retries} retries for URL: {presigned_url}", extra=extra_params)
            raise e

def get_file_extension_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Extract the filename from the path
    filename = os.path.basename(unquote(path))

    # Extract file extension from the filename
    _, file_extension = os.path.splitext(filename)

    if file_extension:
        return file_extension.lower()[
            1:
        ]  # Remove the leading dot and convert to lowercase
    else:
        return "ply"

def get_file_size(file_obj):
    if isinstance(file_obj, io.BytesIO):
        return len(file_obj.getvalue())
    return 0

async def upload_mesh_s3(mesh, url: str, mesh_name: str = "", logger=None):
    mesh_extension = get_file_extension_from_url(url)

    # Export the mesh in the correct format
    if mesh_extension == "ply":
        file_obj = trimesh.exchange.ply.export_ply(mesh)
    elif mesh_extension == "stl":
        file_obj = trimesh.exchange.stl.export_stl(mesh)
    elif mesh_extension == "obj":
        file_obj = trimesh.exchange.obj.export_obj(mesh)
    else:
        logger.warning(f"Unsupported mesh extension [{mesh_extension}] for mesh [{mesh_name}].")
        return

    logger.debug(f"Uploading [{mesh_name}] mesh with extension [{mesh_extension}] to S3..")

    # Perform the upload asynchronously
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(
                url, data=file_obj, headers={"Content-Type": "application/octet-stream"}
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to upload [{mesh_name}] mesh to S3: {response.status}", exc_info=True)
                else:
                    logger.info(f"Successfully uploaded [{mesh_name}] mesh to S3.")
        except Exception as e:
            logger.error(f"Error uploading [{mesh_name}] mesh to S3: {e}", exc_info=True)

async def save_output_meshes_to_s3(
        outputs,
        output_urls,
        logger,
        extra_params,
):
    tasks = []
    for mesh_name, mesh_data in outputs.items():
        url = output_urls[mesh_name]
        if url and mesh_data and mesh_data.valid:
            tasks.append(
                upload_mesh_s3(
                    mesh=mesh_data.aligned_mesh,
                    url=url,
                    mesh_name=mesh_name,
                    logger=logger,
                )
            )
        else:
            logger.warning(f"URL for {mesh_name} is empty or file is not valid.", extra=extra_params)

    if tasks:
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logger.error(f"Error occurred while uploading meshes: {e}", exc_info=True)
    else:
        logger.warning("No valid URLs or files found.", extra=extra_params)

async def export_meshes_to_zip(meshes_dict: Dict, mesh_type: str = "stl"):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for mesh_name, scan in meshes_dict.items():
            if mesh_type == "stl":
                file_ = trimesh.exchange.stl.export_stl(scan.aligned_mesh)
            elif mesh_type == "obj":
                file_ = trimesh.exchange.obj.export_obj(scan.aligned_mesh)
            else:
                file_ = trimesh.exchange.ply.export_ply(scan.aligned_mesh)

            zipf.writestr(f"{mesh_name}.{mesh_type}", file_)

    return zip_buffer.getvalue()

async def upload_zip_meshes_s3(
        meshes_dict: Dict, mesh_type: str = "stl", url: str = "", logger=None, is_local: bool = False
):
    zip_data = await export_meshes_to_zip(meshes_dict, mesh_type=mesh_type)

    if is_local:
        with open(url, "wb") as local_file:
            local_file.write(zip_data)
    else:
        async with aiohttp.ClientSession() as session:
            async with session.put(
                    url, data=zip_data, headers={"Content-Type": "application/zip"}
            ) as response:
                if response.status != 200:
                    logger.info(f"Failed to upload zip with status {response.status}")
                else:
                    logger.info(f"Successfully uploaded zip file")

    return
