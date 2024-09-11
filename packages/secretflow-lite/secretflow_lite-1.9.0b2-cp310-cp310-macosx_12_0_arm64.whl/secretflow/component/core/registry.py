# Copyright 2024 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from secretflow.spec.v1.component_pb2 import ComponentDef

from .definition import Definition


class Registry:
    _definitions: dict[str, Definition] = {}

    @staticmethod
    def register(d: Definition):
        key = Registry.gen_key(d.domain, d.name, d.version)
        if key in Registry._definitions:
            raise ValueError(f"{key} is already registered")

        Registry._definitions[key] = d

    @staticmethod
    def unregister(domain: str, name: str, version: str) -> bool:
        key = Registry.gen_key(domain, name, version)
        if key not in Registry._definitions:
            return False
        del Registry._definitions[key]
        return True

    @staticmethod
    def get_definition(domain: str, name: str, version: str) -> Definition:
        key = Registry.gen_key(domain, name, version)
        if key not in Registry._definitions:
            return None
        return Registry._definitions[key]

    @staticmethod
    def get_component_defs() -> list[ComponentDef]:  # type: ignore
        result = []
        for d in Registry._definitions.values():
            result.append(d.component_def)
        return result

    @staticmethod
    def gen_key(domain: str, name: str, version: str) -> str:
        tokens = version.split('.')
        assert len(tokens) == 3, f"version must be in format of x.y.z, {version}"
        major = tokens[0]
        return f"{domain}/{name}:{major}"


def register(domain: str, version: str, name: str = "", desc: str = None):
    assert (
        domain != "" and version != ""
    ), f"domain<{domain}> and version<{version}> cannot be empty"

    def wrapper(cls):
        d = Definition(cls, domain, version, name, desc)
        Registry.register(d)
        return cls

    return wrapper
