# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import atexit
import socket
import docker
from pathlib import Path
import time


class WebRTCManager:
    http_port = 8080
    report_path_to_container = {}
    image_name = 'nvidia/devtools-streamer-nsys:1.0'
    timeout = 10     # seconds

    # DTSP-16652: Remove when the image is available in the public registry
    build_script_path = "host-linux-x64/Scripts/WebRTCContainer/build.sh"
    atexit.register(
        lambda: [container.stop() for container in WebRTCManager.report_path_to_container.values()])

    @classmethod
    def get_docker_client(cls):
        try:
            return docker.DockerClient()
        except docker.errors.DockerException as e:
            raise RuntimeError('Failed to start docker client. Is the docker service running? '
                               '(start it with "systemctl start docker") '
                               'Also make sure you have sufficient permissions, '
                               'see: https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user'
                               ) from e

    @classmethod
    def get_docker_image(cls, docker_client: docker.DockerClient):
        try:
            return docker_client.images.get(cls.image_name)
        except docker.errors.ImageNotFound as e:
            # DTSP-16652: Fix message when the image is available in the public registry
            raise RuntimeError(
                f'Docker image "{cls.image_name}" was not found. '
                'Build it by running the following script: '
                f'"<nsys installation dir>/{cls.build_script_path}"') from e

    @classmethod
    def create_container(cls, tool_path: Path, report_path: Path, host: str):
        turn_port = cls._get_free_port()
        ports = {cls.http_port: None, turn_port: turn_port}
        environment = {
            'DEVTOOL_CMD': f'{tool_path.name} --fullscreen /mnt/host/reports/{report_path.name}',
            'HOST_IP': f'{host}',
            'TURN_PORT': str(turn_port),
            'NV_AGORA_DISABLE_TELEMETRY': '1'
        }
        volumes = {
            tool_path.parent: {'bind': '/mnt/host/devtool'},
            report_path.parent: {'bind': '/mnt/host/reports'}
        }
        docker_client = cls.get_docker_client()
        container = docker_client.containers.run(image=cls.get_docker_image(docker_client),
                                                 ports=ports,
                                                 environment=environment,
                                                 volumes=volumes,
                                                 detach=True,
                                                 remove=True)
        cls.report_path_to_container[report_path] = container

    @classmethod
    def run(cls, tool_path: Path, report_path: Path, host: str):
        if report_path not in cls.report_path_to_container:
            cls.create_container(tool_path, report_path, host)
        container = cls.report_path_to_container[report_path]
        return cls.get_docker_client().api.port(container.id, cls.http_port)[0]["HostPort"]

    @classmethod
    def stop(cls, report_path: Path):
        cls.report_path_to_container[report_path].stop()
        del cls.report_path_to_container[report_path]

    @staticmethod
    def _get_free_port() -> int:
        with socket.socket() as s:
            s.bind(('', 0))
            return s.getsockname()[1]
