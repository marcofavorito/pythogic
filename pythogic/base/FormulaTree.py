# from pythogic.base.Formula import Formula, UnaryOperator, SimpleFormula, BinaryOperator, CommutativeBinaryOperator
# import networkx as nx
#
# class FormulaNode(object):
#     def __init__(self, f:Formula):
#         self.f = f
#
#
#
# class TreeFormula(object):
#
#     def _find_edges(self, f:Formula):
#         parent = f
#         childs = []
#         if isinstance(f, SimpleFormula):
#             pass
#         elif isinstance(f, UnaryOperator):
#             childs.append(f.f)
#         elif isinstance(f, BinaryOperator):
#             childs.append(f.f1)
#             childs.append(f.f2)
#
#         return [(parent, child) for child in childs]
#
#     def _merge_commutative_operator(self, t:nx.Graph):
#         nodes_to_merge = []
#         for n in t.nodes:
#             if isinstance(n, CommutativeBinaryOperator):
#
#
#
#     def __init__(self, f:Formula):
#         edges = self._find_edges(f)
#         self.t = nx.Graph(edges)
#
#
#
