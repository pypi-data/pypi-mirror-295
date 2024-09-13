#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
windmill_dump.py
Authors: zhangzhijun06(zhangzhijun06@baidu.com)
Date:    2024/09/04-2:38 PM
"""
import tarfile
import yaml
import os
import requests
from argparse import ArgumentParser

from windmillclient.client.windmill_client import WindmillClient
from windmilltrainingv1.client.training_api_job import parse_job_name
from windmillmodelv1.client.model_api_modelstore import parse_modelstore_name
from windmillcategoryv1.client.category_api import match
from windmillmodelv1.client.model_api_model import Category


model_tar = "model.tar"


def parse_args():
    """
    Parse arguments.
    """
    parser = ArgumentParser()
    parser.add_argument("--uri", required=False, type=str, default="")
    parser.add_argument("--model_store_name", required=False, type=str, default="")
    parser.add_argument("--job_name", required=False, type=str, default="")

    args, _ = parser.parse_known_args()
    return args


def extract_tar(tar_path, directory='.'):
    """
    解压tar文件到指定目录。

    参数:
    tar_path (str): tar文件的路径。
    extract_to (str): 解压到的目标目录（默认为当前目录）。
    """
    with tarfile.open(tar_path, 'r:*') as tar:
        tar.extractall(path=directory)


def download_models(uri):
    """
    下载模型文件
    """
    with requests.get(uri, stream=True) as r:
        r.raise_for_status()
        with open(model_tar, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


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
    import model.
    """
    args = parse_args()
    org_id = os.getenv("ORG_ID", "")
    user_id = os.getenv("USER_ID", "")
    windmill_endpoint = os.getenv("WINDMILL_ENDPOINT", "")
    windmill_client = WindmillClient(endpoint=windmill_endpoint,
                                     context={"OrgID": org_id, "UserID": user_id})

    # 下载模型
    job_name = parse_job_name(args.job_name)
    tag_map = {}
    try:
        download_models(args.uri)
    except Exception as e:
        tag_map = {
            "errorCode": "102",
            "errorMessage": "模型路径有误：uri不存在！"
        }
        update_job(windmill_client, job_name=job_name, tag_map=tag_map)

    # 模型解压
    extract_tar(model_tar)
    if not os.path.exists("./apply.yaml"):
        tag_map = {
            "errorCode": "101",
            "errorMessage": "文件格式错误：apply.yaml文件不存在！"
        }
        update_job(windmill_client, job_name=job_name, tag_map=tag_map)

    # 解析并上传模型
    model_store = parse_modelstore_name(args.model_store_name)
    model_list = []
    with open('./apply.yaml', 'r') as fb:
        for data in yaml.safe_load_all(fb):
            tag_map[data["metadata"]["localName"]] = ""
            model_list.append(data)
    # 更新模型名
    update_job(windmill_client, job_name=job_name, tag_map=tag_map)

    try:
        for model in model_list:
            resp = windmill_client.create_model(
                        workspace_id=model_store.workspace_id,
                        model_store_name=model_store.local_name,
                        local_name=model["metadata"]["localName"],
                        display_name=model["metadata"]["displayName"],
                        prefer_model_server_parameters=model["metadata"]["preferModelServerParameters"],
                        category=model["metadata"]["category"],
                        model_formats=model["metadata"]["modelFormats"],
                        artifact_tags=model["metadata"]["artifact"]["tags"],
                        artifact_metadata=model["metadata"]["artifact"]["metadata"],
                        artifact_uri=model["metadata"]["artifact"]["uri"])

            if match(model["metadata"]["category"], Category.CategoryImageEnsemble.value):
                model_list = windmill_client.get_model_manifest(model_store.workspace_id,
                                                                model_store.local_name,
                                                                resp.localName,
                                                                str(resp.artifact["version"]))
                for item in model_list.subModels:
                    tag_map[item["localName"]] = str(item["artifact"]["version"])
    except Exception as e:
        tag_map = {
            "errorCode": "400",
            "errorMessage": "内部服务错误！"
        }

    # 更新版本
    update_job(windmill_client, job_name=job_name, tag_map=tag_map)


if __name__ == "__main__":
    run()
