"""
In thinglang, each compilation unit consists of a single thing definition, parsed into an isolated AST.

From this local AST, a symbol map is generated. This symbol map is later used down the road during linking.
Additionally, the symbol map is serializable, and can exist as part of a fully linked thing executable, library or
independently for linking against native thing libraries.

During this process, thing definitions are also indexed into the memory layout.
"""


