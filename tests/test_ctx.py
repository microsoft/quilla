import os

import pytest
from pluggy import PluginManager

from quilla.ctx import (
    get_default_context,
    Context
)
from quilla.common.exceptions import (
    InvalidContextExpressionException,
    InvalidOutputName,
)


@pytest.mark.smoke
@pytest.mark.ctx
class ContextTests:
    @pytest.mark.unit
    def test_default_context_singleton(self, plugin_manager: PluginManager):
        '''
        Ensures that the `get_default_context` returns the same object every time
        '''
        ctx = get_default_context(plugin_manager)
        other_ctx = get_default_context(plugin_manager)

        assert ctx is other_ctx

    @pytest.mark.unit
    @pytest.mark.parametrize('debug_opt', [True, False])
    def test_context_sets_debug_options(self, ctx: Context, debug_opt: bool):
        '''
        Ensures that setting the is_debug parameter properly sets all debug options
        '''
        ctx.is_debug = debug_opt

        assert ctx.suppress_exceptions is not debug_opt
        assert ctx.run_headless is not debug_opt
        assert ctx.close_browser is not debug_opt
        assert ctx._debug is debug_opt
        assert ctx.is_debug is debug_opt

    @pytest.mark.unit
    def test_context_sets_path_var(self):
        '''
        Ensures that setting the drivers_path property updates the system
        PATH variable
        '''
        ctx = Context(
            None,
            drivers_path='/some/path'
        )

        assert ctx.drivers_path == '/some/path'
        assert os.environ['PATH'].find('/some/path') > -1

    @pytest.mark.unit
    @pytest.mark.parametrize('expression', [
        'some_text',
        'some_other_text',
        'some_text_with_(parenthesis)',
        '$ some_text_with_$',
        '${ some_text_with_more_characters',
        '${ incorrect expression }',
    ])
    def test_context_replacement_returns_same_on_no_ctx_expression(
        self,
        ctx: Context,
        expression: str
    ):
        '''
        Ensures that strings with no context expressions are not altered
        by the perform_replacements function
        '''
        assert ctx.perform_replacements(expression) == expression

    @pytest.mark.parametrize('output_name', [
        'my_output',
        'my.output',
        'my.deeply.nested.output',
        'my.deeply.nested_output'
    ])
    @pytest.mark.parametrize('output_value', [
        'some_text',
        'some_other_text',
        'this_is_just_some_value_I_guess',
        'some_other_test_value',
    ])
    @pytest.mark.parametrize('context_obj,setup_func', [
        ('Validation', lambda ctx, x, y: ctx.create_output(x, y)),
        ('Environment', lambda _, x, y: os.environ.update({x: y})),
    ])
    def test_context_uses_output_expression(
        self,
        ctx: Context,
        output_name: str,
        output_value: str,
        context_obj: str,
        setup_func,
    ):
        '''
        Ensures that the perform_replacements function can adequately
        retrieve outputed & environment values
        '''
        setup_func(ctx, output_name, output_value)
        context_expression = '${{ %s.%s }}' % (context_obj, output_name)

        assert ctx.perform_replacements(context_expression) == output_value

    def test_context_can_create_nonstr_output(self, ctx: Context):
        '''
        Ensures that it is possible to create non-string outputs, but they will return as
        strings
        '''
        ctx.create_output('some_value', 3)

        assert ctx.perform_replacements('${{ Validation.some_value }}') == '3'

    def test_context_errors_on_invalid_expression(self, ctx: Context):
        '''
        Ensures that attempting to reference values that don't exist will cause an error
        '''
        with pytest.raises(InvalidContextExpressionException):
            ctx.perform_replacements('${{ Validation.some.nonexistent_value }}')

    @pytest.mark.parametrize('nested_output_name', [
        'nested_value',
        'deeply.nested.value'
    ])
    def test_context_expression_errors_on_used_name(
        self,
        ctx: Context,
        nested_output_name: str
    ):
        ctx.create_output('some_output', 'some_output')
        with pytest.raises(InvalidOutputName):
            ctx.create_output('some_output.%s' % nested_output_name, 'some_output')
