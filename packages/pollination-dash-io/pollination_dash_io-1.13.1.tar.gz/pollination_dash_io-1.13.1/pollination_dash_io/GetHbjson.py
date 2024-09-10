# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class GetHbjson(Component):
    """A GetHbjson component.
Get a model (HBJSON) from CAD
State
- hbjson (dictionary): HBJSON Model

Keyword arguments:

- id (string; default 'po-get-hbjson'):
    Unique ID to identify this component in Dash callbacks.

- buttonLabel (string; optional)

- defaultKey (string; required)

- fullWidth (boolean; optional)

- optionsConfig (dict; optional)

    `optionsConfig` is a dict with keys:

    - preview (dict; required)

        `preview` is a dict with keys:

        - selected (boolean; optional)

        - show (boolean; optional)

    - selection (dict; required)

        `selection` is a dict with keys:

        - selected (boolean; optional)

        - show (boolean; optional)

    - subscribe (dict; required)

        `subscribe` is a dict with keys:

        - selected (boolean; optional)

        - show (boolean; optional)

- showHelpText (boolean; optional)

- useIcon (boolean; optional)"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'GetHbjson'
    @_explicitize_args
    def __init__(self, defaultKey=Component.REQUIRED, optionsConfig=Component.UNDEFINED, buttonLabel=Component.UNDEFINED, useIcon=Component.UNDEFINED, fullWidth=Component.UNDEFINED, onChange=Component.UNDEFINED, showHelpText=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'buttonLabel', 'defaultKey', 'fullWidth', 'optionsConfig', 'showHelpText', 'useIcon']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'buttonLabel', 'defaultKey', 'fullWidth', 'optionsConfig', 'showHelpText', 'useIcon']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['defaultKey']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(GetHbjson, self).__init__(**args)
