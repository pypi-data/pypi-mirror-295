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

from io import TextIOWrapper
from typing import Callable, List, Optional

from velocitas_lib.text_utils import replace_item_in_list


def replace_text_in_file(file_path: str, text: str, replacement: str) -> None:
    """Replace all occurrences of text in a file with a replacement.

    Args:
        file_path (str): The path to the file.
        text (str): The text to find.
        replacement (str): The replacement for text.
    """

    with open(file_path, mode="r+", encoding="utf-8") as file:
        file_text = file.readlines()
        replaced_text_list = replace_item_in_list(file_text, text, replacement)
        replaced_text = "".join(replaced_text_list)
        # replace old content
        file.seek(0)
        file.write(replaced_text)
        file.truncate()


def capture_area_in_file(
    file: TextIOWrapper,
    start_line: str,
    end_line: str,
    map_fn: Optional[Callable[[str], str]] = None,
) -> List[str]:
    """Capture an area of a textfile between a matching start line (exclusive) and the first line matching end_line (exclusive).

    Args:
        file (TextIOWrapper): The text file to read from.
        start_line (str): The line which triggers the capture (will not be part of the output)
        end_line (str): The line which terminates the capture (will not be bart of the output)
        map_fn (Optional[Callable[[str], str]], optional): An optional mapping function to transform captured lines. Defaults to None.

    Returns:
        List[str]: A list of captured lines.
    """
    area_content: List[str] = []
    is_capturing = False
    for line in file:
        if line.strip() == start_line:
            is_capturing = True
        elif line.strip() == end_line:
            is_capturing = False
        elif is_capturing:
            line = line.rstrip()

            if map_fn:
                line = map_fn(line)

            area_content.append(line)
    return area_content


def read_file(
    file_path: str,
) -> Optional[str]:
    """Reads the file with the given file_path and returns it's content as a str.

    Args:
        file_path (str): the file_path of the file to read.

    Returns:
        str: the content of the specified file.
    """

    try:
        with open(file_path, "r") as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        print(f"File {file_path} not found")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def write_file(
    file_path: str,
    content: str,
) -> bool:
    """Writes the content to the file_path and returns the success of the write operation.

    Args:
        file_path (str): the file_path of the file to write.
        content (str): the content to be written to the file.

    Returns:
        bool: True if writing was successful, False otherwise.
    """

    try:
        with open(file_path, "w") as file:
            file.write(content)
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
