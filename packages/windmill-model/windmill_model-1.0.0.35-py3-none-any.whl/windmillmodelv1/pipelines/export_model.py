#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
windmill_dump.py
Authors: zhangzhijun06(zhangzhijun06@baidu.com)
Date:    2024/09/04-2:38 PM
"""
import tarfile
from datetime import datetime
import os
from argparse import ArgumentParser

from windmillclient.client.windmill_client import WindmillClient
from windmillcomputev1.filesystem import upload_by_filesystem
from windmillartifactv1.client.artifact_client import parse_artifact_name
from windmillmodelv1.client.model_client import parse_model_name
from windmillmodelv1.client.model_api_modelstore import ModelStoreName
from windmilltrainingv1.client.training_api_job import parse_job_name


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--artifact_name", required=False, type=str, default="")
    parser.add_argument("--job_name", required=False, type=str, default="")
    parser.add_argument("--output_uri", required=False, type=str, default=".")

    args, _ = parser.parse_known_args()
    return args


def tar_directory(directory, filename):
    """
    将指定目录（包括其子目录和文件）压缩成一个tar文件。

    参数:
    directory (str): 要压缩的目录路径。
    filename (str): 输出的tar文件名（包括路径，如果需要）。
    """
    with tarfile.open(filename, "w:") as tar:
        tar.add(directory, arcname=os.path.basename(directory))


def get_tar_file_name(model_name, version):
    """
    生成导出模型包文件名
    # artifactName: workspaces/aaa/modelstores/bbb/models/ccc/versions/ddd
    # 提取fileName: ccc-ddd-xxxxxxxx.tar xxxx为时间戳
    """
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{model_name.local_name}-{version}-{timestamp}.tar"


def update_job(client, job_name, tag_map):
    """
    更新作业标签
    Args:
        client (WindmillClient):
        job_name:
        tag_map:
    """
    client.update_job(workspace_id=job_name.workspace_id,
                      project_name=job_name.project_name,
                      local_name=job_name.local_name,
                      tags=tag_map)


def run():
    """
    export model.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    artifact_name = parse_artifact_name(args.artifact_name)
    model_name = parse_model_name(artifact_name.object_name)
    job_name = parse_job_name(args.job_name)

    # 1、dump models
    output_uri = args.output_uri
    tag_map = {}
    try:
        windmill_client.dump_models(artifact_name=args.artifact_name, rename="ensemble", output_uri=output_uri)
        if not os.path.exists(os.path.join(output_uri, "apply.yaml")):
            tag_map = {
                "errorCode": "101",
                "errorMessage": "文件格式错误：apply.yaml文件不存在！"
            }
    except Exception as e:
        tag_map = {
            "errorCode": "400",
            "errorMessage": "内部服务错误!"
        }

    if len(tag_map) != 0:
        update_job(windmill_client, job_name, tag_map)
        return

    # 压缩导出模型包
    file_name = get_tar_file_name(model_name, artifact_name.version)
    tar_directory(output_uri, file_name)
    tag_map["name"] = file_name

    model_list = windmill_client.get_model_manifest(model_name.workspace_id,
                                                    model_name.model_store_name,
                                                    model_name.local_name,
                                                    artifact_name.version)
    for item in model_list.subModels:
        tag_map[item["localName"]] = str(item["artifact"]["version"])

    # 上传模型包
    model_store = ModelStoreName(workspace_id=model_name.workspace_id, local_name=model_name.model_store_name)
    filesystem = windmill_client.suggest_first_filesystem(model_name.workspace_id,
                                                          guest_name=model_store.get_name())
    upload_uri = model_list.artifact["uri"]
    upload_uri = os.path.join(os.path.dirname(upload_uri), file_name)
    upload_by_filesystem(filesystem, file_name, upload_uri)

    # 更新job
    update_job(windmill_client, job_name, tag_map)


if __name__ == "__main__":
    run()
