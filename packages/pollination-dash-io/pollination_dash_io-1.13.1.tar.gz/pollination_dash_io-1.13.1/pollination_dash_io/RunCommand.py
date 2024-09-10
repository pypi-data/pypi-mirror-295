# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class RunCommand(Component):
    """A RunCommand component.
Run a CAD command

Keyword arguments:

- id (string; default 'po-run-command'):
    Unique ID to identify this component in Dash callbacks.

- command (dict; default ''):
    Command to run  It can be a macro or command name of the host
    software ___________________________________ Available complex
    command for Rhino  View from sun E.g. ``` {     name:
    'ViewFromSun'     param: {         target: {'x': 0, 'y': 0, 'z':
    0, 'type': 'Point3D'},         direction: {'x': -0.062823, 'y':
    1.904328, 'z': -0.42219, 'type': 'Vector3D'},         displayName:
    'Shaded'     } } ```  Add directional light E.g. ``` {     name:
    'SetRhinoDirectLight'     param: {         vectors: [{'x':
    -0.062823, 'y': 1.904328, 'z': -0.42219, 'type': 'Vector3D'}]
    } } ```.

    `command` is a string | dict with keys:

    - name (string; required)

    - param (string; required)

- hideButton (boolean; default False):
    Show/hide button.

- prefix (string; default 'Run'):
    Prefix of the label.

- trigger (boolean | number | string | dict | list; optional):
    External trigger."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'pollination_dash_io'
    _type = 'RunCommand'
    @_explicitize_args
    def __init__(self, command=Component.UNDEFINED, prefix=Component.UNDEFINED, hideButton=Component.UNDEFINED, trigger=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'command', 'hideButton', 'prefix', 'trigger']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'command', 'hideButton', 'prefix', 'trigger']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(RunCommand, self).__init__(**args)
