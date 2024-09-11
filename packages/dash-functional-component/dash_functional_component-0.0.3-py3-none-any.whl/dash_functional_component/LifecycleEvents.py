# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class LifecycleEvents(Component):
    """A LifecycleEvents component.
dispatch mound and unMount Event to document

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    children.

- id (string; required):
    The ID used to identify this component in Dash callbacks."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_functional_component'
    _type = 'LifecycleEvents'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, **kwargs):
        self._prop_names = ['children', 'id']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(LifecycleEvents, self).__init__(children=children, **args)
