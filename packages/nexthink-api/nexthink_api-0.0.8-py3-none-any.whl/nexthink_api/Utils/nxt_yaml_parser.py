"""Parse Nexthink YAML description API."""
# ruff: noqa: N815     Naming conforme to yaml definition https://developer.nexthink.com/docs/api/

from pathlib import Path
from typing import List, Dict, Optional
import sys
import re
import pickle
from pydantic import BaseModel, Field
import yaml

__all__ = ["NxtYamlParser"]


class Server(BaseModel):
    url: str
    description: Optional[str]
    version: str


class Parameter(BaseModel):
    name: str
    in_: str
    required: bool
    type: dict
    description: Optional[str]


class Endpoint(BaseModel):
    summary: str = Field(exclude=True)
    operationId: str
    description: Optional[str]
    parameters: List[Parameter]


class Response(BaseModel):
    code: str
    description: str


class Method(BaseModel):
    method: str
    responses: List[Response]


class APISpec(BaseModel):
    title: str
    servers: List[Server]
    endpoints: Dict[str, Endpoint]
    methods: Dict[str, Dict[str, list[Response]]]


class ApiConfig(BaseModel):
    APIs: dict[str, APISpec] = Field(default={})


class API(BaseModel):
    version: str
    endpoints: dict
    methods: dict


class YamlParser:
    """Parse Nexthink YAML description API.

    Attributes
    ----------
        api_config : dict
            Configuration for the API.
        yaml_dir : str
            Directory where the YAML files are stored.
        pkl_file : str
            File where the parsed data are stored.

    """

    api_config = None
    yaml_dir = None
    pkl_file = None

    @classmethod
    def get_package_root(cls) -> Path:
        """Get the root of package.

        Returns
        -------
            Path:
                Absolute path of root package

        """
        # Module name
        module_name = cls.__module__
        module = sys.modules[module_name]
        # module file path
        module_file_path = module.__file__
        # Convert to Path object
        module_path = Path(module_file_path)
        package_name = module_name.split('.', 1)[0]
        # search for top level __init__.py
        package_root = module_path.parent
        while package_root.name != package_name:
            package_root = package_root.parent

        return package_root

    @classmethod
    def get_class_file_path(cls) -> Path:
        """Get the path of the class file.

        Returns
        -------
            Path:
                Absolute path of class file

        """
        # Module name
        module_name = cls.__module__
        module = sys.modules[module_name]
        # module file path
        module_file_path = module.__file__
        # Convert to Path object
        return Path(module_file_path)

    def __init__(self):
        self.yaml_dir = self.get_package_root() / 'yaml'
        self.pkl_file = self.get_package_root() / 'Pkl/api_config.pkl'

        if self.pkl_file.exists():
            # reload api_config from PKL
            self.load_pk_file()
        else:
            # Parser les fichiers YAML et sauvegarder le résultat
            yaml_files = list(self.yaml_dir.glob('*.yaml'))
            self.api_config = self.parse_yaml_files(yaml_files)
            # save api_config to pkl_file)
            self.save_pk_file()

    def load_yaml_file(self, yaml_file: Path) -> dict:
        """Load a YAML file.

        Parameters
        ----------
        yaml_file : Path
            The path of Yaml file to read

        Returns
        -------
        dict
            The parsed YAML file

        """
        with yaml_file.open('r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def load_pk_file(self) -> None:
        """Load the PKL file."""
        with (open(self.pkl_file, 'rb')) as f:
            self.api_config = pickle.load(f)

    def save_pk_file(self) -> None:
        """Save the PKL file."""
        with (open(self.pkl_file, 'wb')) as f:
            pickle.dump(self.api_config, f)

    def parse_yaml_files(self, yaml_files: List[Path]) -> ApiConfig:  # pylint: disable=too-many-locals
        """Parse a list of YAML files.

        Parameters
        ----------
            yaml_files: List[Path]
                Files list to be parsed

        Returns
        -------
            ApiConfig
                Class holding the parsed YAML files

        """
        api_specs = {}
        for yaml_file in yaml_files:
            data = self.load_yaml_file(yaml_file)
            title = data.get('info', {}).get('title', 'No Title')
            description = data.get('info', {}).get('description', '')
            version = data.get('info', {}).get('version', '')
            servers = [Server(url=server['url'], description=description, version=version) for server in
                       data.get('servers', [])]
            endpoints = {}
            methods = {}

            for path, methods_info in data.get('paths', {}).items():
                for method, method_info in methods_info.items():
                    if method in ['get', 'post', 'put', 'delete', 'patch']:  # standard HTTP methods
                        endpoint = Endpoint(
                                summary=method_info.get('summary', ''),
                                operationId=method_info.get('operationId', ''),
                                description=method_info.get('description', ''),
                                parameters=self.parse_parameters(method_info.get('parameters', []))
                        )
                        if path not in endpoints:
                            endpoints[path] = endpoint

                        response_list = []
                        for code, response_info in method_info.get('responses', {}).items():
                            response_list.append(Response(code=code, description=response_info.get('description', '')))

                        if path not in methods:
                            methods[path] = {}
                        methods[path][method] = response_list

            api_specs[yaml_file.stem] = APISpec(title=title, servers=servers, endpoints=endpoints, methods=methods)
        return ApiConfig(APIs=api_specs)

    def parse_parameters(self, params: list) -> List[Parameter]:
        """Parse a list of parameters from the Yaml file.

        Parameters
        ----------
            params: list
                parameters section from the YAML file

        Returns
        -------
            list[Parameter]
                Parsed list of parameters

        """
        parameters = []
        for param in params:
            parameter = Parameter(
                    name=param.get('name', ''),
                    in_=param.get('in', ''),
                    required=param.get('required', False),
                    type=param.get('type', {}),
                    description=param.get('description', '')
            )
            parameters.append(parameter)
        return parameters


class NxtYamlParser:
    """NXT API Specification Parser.

    Attributes
    ----------
    versions: dict
        The version of each API.
    APIs: list
        list of API.
    endpoints: dict
        Endpoints by API.
    methods: dict
        Methods by endpoints and by APIs.
    api_definitions: dict
        global API definition.

    """

    # APIs Version:  {api : version}
    versions = {}
    # API list:  {index: api_name, }
    APIs = []
    # Endpoints by API {api1: [endpoint1, endpoint2],  api2: [endpoint3, endpoint4]}
    endpoints = {}
    # Methods by endpoints and by APIs: {api1: {endpoint1: [method1, method2, ...]}, api2}
    methods = []
    # Global API definition
    api_definitions = {}

    _api_specs: ApiConfig

    def __init__(self):
        """Nxt API Specification Parser."""
        api_parser = YamlParser()
        self._api_specs = api_parser.api_config
        self.parse_specs()

    def parse_specs(self) -> None:
        """Parse all section of API."""
        self.versions = self.get_versions()
        self.APIs = self.get_apis()
        self.endpoints = self.get_endpoints()
        self.methods = self.get_methods_for_endpoint()
        self.api_definitions = self.get_api_definition()

    def get_versions(self) -> dict[str:str]:
        """Build a dictionary of api version.

        Returns
        -------
            dict(str,str)
                dictionary of each apis version

        """
        return {api: apispec.servers[0].version for api, apispec in self._api_specs.APIs.items()}

    def get_apis(self) -> list[str]:
        """Build a list of apis.

        Returns
        -------
        list(str)
            List of available API

        """
        return list(self._api_specs.APIs.keys())

    def get_api_for_endpoint(self, endpoint: str) -> str:
        """Get the API name for a given endpoint.

        Parameters
        ----------
        endpoint : str
            Endpoint name.

        Returns
        -------
            API name or None if no API is found for the endpoint.

        """
        endpoints = self.get_endpoints()
        return next((api for api, values in endpoints.items()
                     if any(re.match(rf"(/)?{re.escape(endpoint)}", value)
                            for value in values)), None)

    def get_endpoints(self) -> dict[str, list[str]]:
        """Return all endpoints for each API.

        Returns
        -------
        dict(str, list[str])
            dictionary of endpoints used by each API

        """
        return {api: self.get_endpoints_for_api(api) for api in self.APIs}

    def get_endpoints_for_api(self, api: str) -> list[str]:
        """Get all endpoints for a given API.

        Parameters
        ----------
        api: str
            api name

        Returns
        -------
            list(str)
                list of endpoint for the API

        """
        return list(self._api_specs.APIs[api].endpoints.keys())

    def get_methods_for_endpoint(self) -> dict[str, list[str]]:
        """Get the methods that can be used on each endpoints.

        Returns
        -------
        dict(str, list(str))
            dictionary of endpoints and supported methods.

        """
        return {
            endpoint: list(methods.keys())
            for api in self._api_specs.APIs.keys()
            for endpoint, methods in self._api_specs.APIs[api].methods.items()
        }

    def get_methods_for_api(self, api: str) -> dict[str, list[str]]:
        """Get supported method for a given API.

        Parameters
        ----------
            api : str
                api name

        Returns
        -------
            dict(str, list(str))
                list of all methods that can be used on the API.

        """
        return {
            endpoint: [method.upper() for method in responses.keys()]
            for endpoint, responses in self._api_specs.APIs[api].methods.items()
        }

    def get_api_definition(self) -> dict:
        """Build the complete dictionary definition API from YAML specification.

        Returns
        -------
        dict
            Dictionary of the Nexthink API.

        """
        return {
            api: {
                endpoint: {
                    method: {
                        response.code: response.description
                        for response in self._api_specs.APIs[api].methods[endpoint][method]
                    }
                    for method in self.methods[endpoint]
                }
                for endpoint in self.endpoints[api]
            }
            for api in self.APIs
        }

    @property
    def api_config(self) -> ApiConfig:
        """Return the parsed API."""
        return self._api_specs
