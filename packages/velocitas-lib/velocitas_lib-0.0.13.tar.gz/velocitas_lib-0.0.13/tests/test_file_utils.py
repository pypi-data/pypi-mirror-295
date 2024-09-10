# Copyright (c) 2024 Contributors to the Eclipse Foundation
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

import os
import tempfile

import pytest

from velocitas_lib.file_utils import (
    read_file,
    write_file,
)


@pytest.fixture
def temp_file():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    yield temp_file

    if os.path.exists(temp_file.name):
        os.remove(temp_file.name)


def test_write_file(temp_file):
    temp_file_path = temp_file.name
    write_file(
        temp_file_path,
        "Lorem ipsum dolor sit amet ...\n1...2...3...",
    )

    assert os.path.exists(temp_file.name)

    read_file_content = temp_file.readlines()
    assert read_file_content[0] == b"Lorem ipsum dolor sit amet ...\n"
    assert read_file_content[1] == b"1...2...3..."


def test_read_file(temp_file):
    file_content = "Lorem ipsum dolor sit amet ...\n1...2...3..."
    temp_file.write(file_content.encode("utf-8"))
    temp_file.flush()
    temp_file.close()

    temp_file_path = temp_file.name
    read_file_content = read_file(temp_file_path)

    assert read_file_content == file_content
