"""
In thinglang, each compilation unit consists of a single thing definition, parsed into an isolated AST.

From this local AST, a symbol map is generated. This symbol map is later used down the road during linking.
Additionally, the symbol map is serializable, and can exist as part of a fully linked thing executable, library or
independently for linking against native thing libraries.

During this process, thing definitions are also indexed into the memory layout.
"""
import pprint

from thinglang.parser.nodes.classes import ThingDefinition


class SymbolMap(object):

    def __init__(self, thing: ThingDefinition):
        self.thing = thing
        self.symbols = thing.members() + thing.methods()
        self.lookup = {
            elem.name: elem for elem in self.symbols
        }

        assert len(self.symbols) == len(self.lookup), 'Thing definition contains colliding elements'

    def serialize(self):
        return [x.serialize() for x in self.symbols]

    def __repr__(self):
        return 'SymbolMap({{{}}})'.format(repr(self.symbols))
