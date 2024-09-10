# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SelectCloudArtifact(Component):
    """A SelectCloudArtifact component.
Select a cloud artifact
State
- name (string): Name of the file
- value (string): Base64 string representation of the file
- type (string): folder | file
- key (string): path where the file is

Keyword arguments:

- id (string; default 'po-sel-artifact'):
    Unique ID to identify this component in Dash callbacks.

- apiKey (string; optional):
    API key from Pollination Cloud.

- basePath (string; default 'https://api.pollination.cloud'):
    Base path of the API.

- fileNameMatch (string; optional):
    File name filter.

- projectName (string; default 'demo'):
    Name of the project.

- projectOwner (string; default 'ladybug-tools'):
    Owner of the project.

- studyId (string; optional):
    ID of the job.

- value (dict; optional):
    Initial path where the files are.

    `value` is a dict with keys:

    - key (string; required)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'SelectCloudArtifact'
    @_explicitize_args
    def __init__(self, projectOwner=Component.UNDEFINED, projectName=Component.UNDEFINED, studyId=Component.UNDEFINED, fileNameMatch=Component.UNDEFINED, value=Component.UNDEFINED, apiKey=Component.UNDEFINED, basePath=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'apiKey', 'basePath', 'fileNameMatch', 'projectName', 'projectOwner', 'studyId', 'value']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'apiKey', 'basePath', 'fileNameMatch', 'projectName', 'projectOwner', 'studyId', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(SelectCloudArtifact, self).__init__(**args)
