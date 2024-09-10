# Copyright (c) 2023-2024 Contributors to the Eclipse Foundation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional

from velocitas_lib import get_package_path, get_workspace_dir, require_env
from velocitas_lib.variables import ProjectVariables


class ServiceSpecConfig(NamedTuple):
    image: str
    is_enabled: bool = True
    env_vars: Dict[str, Optional[str]] = dict()
    args: List[str] = list()
    ports: List[str] = list()
    port_forwards: List[str] = list()
    mounts: List[str] = list()
    startup_log_patterns: List[str] = list()


class Service(NamedTuple):
    id: str
    config: ServiceSpecConfig


def resolve_functions(input_str: str) -> str:
    while True:
        input_str_match = re.search(r"\$(\w+)\((.*)\s*\)", input_str)

        if not input_str_match:
            return input_str

        function_name = input_str_match.group(1).strip()
        parameter = input_str_match.group(2).strip()

        return_value = None
        if function_name == "pathInWorkspaceOrPackage":
            path_in_workspace = os.path.join(get_workspace_dir(), parameter)
            if os.path.isfile(path_in_workspace):
                return_value = path_in_workspace

            if return_value is None:
                path_in_package = os.path.join(get_package_path(), parameter)
                if os.path.isfile(path_in_package):
                    return_value = path_in_package

            if return_value is None:
                raise RuntimeError(
                    f"Path {parameter!r} not found in workspace or package!"
                )
        else:
            raise RuntimeError(f"Unsupported function: {function_name!r}!")

        match_span = input_str_match.span(0)
        input_str = (
            input_str[0 : match_span[0]] + return_value + input_str[match_span[1] :]
        )


def parse_service_config(
    service_id: str, service_spec_config: List[Dict[str, Any]]
) -> ServiceSpecConfig:
    """Parse service spec configuration and return it as an named tuple.

    Args:
        service_id: The ID of the service to be parsed.
        service_spec_config: The specificon of the services from config file.
    """

    is_enabled = True
    container_image = None
    env_vars = dict[str, Optional[str]]()
    ports = []
    port_forwards = []
    mounts = []
    args = []
    patterns = []

    variables = ProjectVariables(env=dict(os.environ))

    for config_entry in service_spec_config:
        key = config_entry["key"]
        value = config_entry["value"]

        if isinstance(value, str):
            value = variables.replace_occurrences(value)
            value = resolve_functions(value)

        if key == "enabled":
            is_enabled = value is True or value == "true"
        elif key == "image":
            container_image = value
        elif key == "env":
            pair = value.split("=", 1)
            inner_key = pair[0].strip()
            env_vars[inner_key] = None
            if len(pair) > 1:
                env_vars[inner_key] = pair[1].strip()
        elif key == "arg":
            args.append(value)
        elif key == "port":
            ports.append(value)
        elif key == "port-forward":
            port_forwards.append(value)
        elif key == "mount":
            mounts.append(value)
        elif key == "start-pattern":
            patterns.append(value)

    if container_image is None:
        raise KeyError(f"Service {service_id!r} does not provide an image!")

    return ServiceSpecConfig(
        image=container_image,
        is_enabled=is_enabled,
        env_vars=env_vars,
        args=args,
        ports=ports,
        port_forwards=port_forwards,
        mounts=mounts,
        startup_log_patterns=patterns,
    )


def get_services(verbose: bool = True) -> List[Service]:
    """Return all specified services as Python object."""
    path = Path(f"{get_package_path()}/runtime.json")
    variable_value = require_env("runtimeFilePath")

    if variable_value is not None:
        overwritten_path = Path(variable_value)
        if not overwritten_path.is_absolute():
            overwritten_path = Path(get_workspace_dir()).joinpath(overwritten_path)

        if overwritten_path.exists():
            path = overwritten_path

            if verbose:
                print(f"runtime.json path redirected to {path}")

    json_array: List[Dict[str, Any]] = json.load(
        open(
            path,
            encoding="utf-8",
        )
    )

    services: List[Service] = list()
    for service_json in json_array:
        service_id = service_json["id"]
        service_config = None
        is_service_enabled = True
        if "config" in service_json:
            service_config = parse_service_config(service_id, service_json["config"])
            is_service_enabled = service_config.is_enabled

        if is_service_enabled:
            if service_config is None:
                raise KeyError(f"Service {service_id!r} does not have a config entry!")

            services.append(Service(service_id, service_config))

    return services


def get_specific_service(service_id: str) -> Service:
    """Return the specified service as Python object.

    Args:
        service_id: The ID of the service to be parsed.
    """
    services = get_services()
    services = list(filter(lambda service: service.id == service_id, services))
    if len(services) == 0:
        raise RuntimeError(f"Service with id '{service_id}' not defined")
    if len(services) > 1:
        raise RuntimeError(
            f"Multiple service definitions of id '{service_id}' found, which to take?"
        )
    return services[0]


def get_service_port(service_id: str) -> str:
    """Return the service port as string for the specified service.

    Args:
        service_id: The ID of the service to be parsed.
    """
    return get_specific_service(service_id).config.ports[0]
