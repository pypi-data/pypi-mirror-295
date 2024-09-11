# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class PropsInjector(Component):
    """A PropsInjector component.
inject extra props to children from a global register

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    children.

- name (string; required):
    The Name used to get props from the register."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_functional_component'
    _type = 'PropsInjector'
    @_explicitize_args
    def __init__(self, children=None, name=Component.REQUIRED, **kwargs):
        self._prop_names = ['children', 'name']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'name']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['name']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(PropsInjector, self).__init__(children=children, **args)
