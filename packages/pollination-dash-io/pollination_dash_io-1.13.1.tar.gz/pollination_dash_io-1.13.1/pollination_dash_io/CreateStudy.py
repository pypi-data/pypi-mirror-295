# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class CreateStudy(Component):
    """A CreateStudy component.
Create a pollination study
State
- study (dictionary): Study information

Keyword arguments:

- id (string; default 'po-create-study'):
    Unique ID to identify this component in Dash callbacks.

- apiKey (string; default ''):
    API key from Pollination Cloud.

- basePath (string; default 'https://api.pollination.cloud'):
    Base path of the API."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'CreateStudy'
    @_explicitize_args
    def __init__(self, apiKey=Component.UNDEFINED, basePath=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'apiKey', 'basePath']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'apiKey', 'basePath']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(CreateStudy, self).__init__(**args)
