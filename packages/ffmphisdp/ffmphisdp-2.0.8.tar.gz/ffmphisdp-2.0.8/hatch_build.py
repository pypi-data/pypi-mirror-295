from copy import deepcopy

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.metadata.core import ProjectMetadata

class ExternalDependenciesHook(BuildHookInterface):
    PLUGIN_NAME = 'ExternalDependenciesHook'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initialize(self, version: str, build_data: dict[str, any]) -> None:
        self._default_constructor = self.build_config.core_metadata_constructor

        def metadata_constructor_extended(local_self, metadata: ProjectMetadata, extra_dependencies: tuple[str] | None = None) -> str:
            metadata_file = self._default_constructor(metadata, extra_dependencies)

            external_dependencies = None
            # This syntax feels logical with the rest of pyproject.toml but is undocumented
            # under [project] put a key 'external-dependencies' with a list of strings
            if 'external-dependencies' in metadata.core.config:
                external_dependencies = deepcopy(metadata.core.config['external-dependencies'])

            # This syntax is proposed here (current stage: draft) : https://peps.python.org/pep-0725/
            # under [external] put a key 'dependencies' with a list of strings
            elif 'external' in metadata.config and 'dependencies' in metadata.config['external']:
                external_dependencies = deepcopy(metadata.config['external']['dependencies'])

            if external_dependencies:
                header_section = metadata_file
                content_section = ''
                if 'Description-Content-Type' in metadata_file:
                    split_file = metadata_file.split('Description-Content-Type')
                    header_section = split_file[0]
                    content_section = split_file[1]
                
                print(f"  - {ExternalDependenciesHook.PLUGIN_NAME}")
                for dependency in external_dependencies:
                    print(f"    - Requires-External: {dependency}")
                    header_section += f'Requires-External: {dependency}\n'
                metadata_file = header_section +'Description-Content-Type' + content_section
            
            return metadata_file

        type(self.build_config).core_metadata_constructor = metadata_constructor_extended

