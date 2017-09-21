from thinglang.foundation import definitions, templates
from thinglang.parser.common.list_type import ListInitialization


class ArgumentList(ListInitialization):

    def transpile(self, instance_cls_name, static=False):
        lines = []

        for arg in reversed(self.values):
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
                type=instance_cls_name
            ))

        return '\n'.join(lines) + '\n'
