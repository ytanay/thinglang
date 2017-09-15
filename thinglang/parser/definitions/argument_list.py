from thinglang.foundation import definitions, templates
from thinglang.parser.common.list_type import ListInitialization


class ArgumentList(ListInitialization):

    def transpile(self, static=False):
        lines = []

        for arg in reversed(self.arguments):
            if arg.type in definitions.INTERNAL_TYPE_ORDERING:
                lines.append(templates.ARGUMENT_POP_TYPE.format(
                    name=arg.transpile(),
                    type=templates.format_internal_type_name(arg.type))
                )
            else:
                lines.append(templates.ARGUMENT_POP_GENERIC.format(
                    name=arg.transpile())
                )

        if not static:
            lines.append(templates.ARGUMENT_POP_TYPE.format(
                name='self',
                type='this_type'
            ))

        return '\n'.join(lines) + '\n'
