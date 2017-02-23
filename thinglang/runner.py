from thinglang.execution.execution import ExecutionEngine
from thinglang.lexer.lexer import lexer
from thinglang.parser.parser import parse


def run(source):
   if not source:
      raise ValueError('Got empty source')

   source = source.strip().replace(' ' * 4, '\t')

   lexical_groups = list(lexer(source))
   root_node = parse(lexical_groups)

   with ExecutionEngine(root_node) as engine:
      engine.execute()
      return engine.results()