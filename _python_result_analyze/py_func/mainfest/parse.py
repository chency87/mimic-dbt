
from ast import alias
from cProfile import label
from copy import deepcopy
from dataclasses import dataclass

from .mainfest import ManifestTask
from pglast.visitors import Visitor, Ancestor, referenced_relations, Skip
from pglast import parse_sql, ast, Node
from graph.graph import GraphNode
import networkx as nx

from pglast.stream import RawStream, maybe_double_quote_name
from typing import Dict, List
import logging
from .vis import GraphVis

@dataclass
class ExpressionNode(Visitor):
    alias: str
    target: str
    rel_name : set
    where: List
    q_type: str
    raw: str

    def __init__(self, q_type, alias) -> None:
        super().__init__()
        self.q_type = q_type
        self.alias = alias

    def visit_SelectStmt(self, ancestors: Ancestor, node: Node):
        self.target = '' #RawStream()(node.targetList)
        self.rel_name = referenced_relations(node)
        print(type(self.rel_name))
        # self.where =  RawStream()(node.whereClause)
        return Skip

    def __call__(self, root):
        self.target = str
        self.rel_name = {}
        self.where = ''
        self.raw = RawStream()(root)
        super().__call__(root)

        return self
   

class QueryVistor:
    def __init__(self, model_name, query) -> None:
        self.model_name = model_name
        self.query = query
        self.root = parse_sql(self.query)
        self.cte_names = set() 
        self.rel_names = set()
        self.nodes = {}
        self.edges = {}
        
        self.rel_names = referenced_relations(stmt= self.root)
        self._parse_selectStmt(self.root[0].stmt, self.model_name, 'src')

    def get_nodes(self):
        return self.nodes

    def get_cte_names(self):
        return self.cte_names

    def get_rel_names(self):
        return self.rel_names

    def _parse_selectStmt(self, node: Node, model_name: str, query_type: str, skip_with_clause = None):
        # print(RawStream()(node))
      
        ## Parse the with clause if exist
        node = self._parse_withClause(node, skip_with_clause)
        ## Parse the from clause, divide the sub query into several

        if node.fromClause is not None:
          
            from_clause = node.fromClause
            new_from_clause =self._parse_fromClause(from_clause= from_clause)
            node.fromClause = new_from_clause


        ## Parse the where clause
        # print(RawStream()(node))
        # print()
        # self.nodes[model_name] = RawStream()(node)
        if model_name in self.nodes:
            model_name = f'{model_name}_1'

        self.nodes[model_name] = ExpressionNode(q_type= query_type, alias= model_name)(node)
        


    def _parse_fromClause(self, from_clause):
        # print()
        assert isinstance(from_clause, tuple)
        new_from_clause = []
        for clause in from_clause:
            new_clause = clause
            if isinstance(clause, ast.RangeSubselect) and clause.subquery:        
                self._parse_selectStmt(node = clause.subquery, model_name = clause.alias.aliasname, query_type= 'subquery')
                new_clause = ast.RangeVar(relname= clause.alias.aliasname, inh= True, relpersistence= 'p', alias= clause.alias)
            new_from_clause.append(new_clause)
        return new_from_clause

    def _parse_withClause(self, node, skip_with_clause):
        assert isinstance(node, ast.SelectStmt)
        if node.withClause and node.withClause is not skip_with_clause:
            with_clause = node.withClause
            if with_clause.recursive:
                raise ('Cannot resolve recursive CTE query')
                self.cte_names.update({maybe_double_quote_name(cte.ctename): cte.ctequery}
                                        for cte in with_clause.ctes)

            else:
                for cte in with_clause.ctes:
                    cte_name = maybe_double_quote_name(cte.ctename)
                    self._parse_selectStmt(node= cte.ctequery, model_name= cte_name, query_type= 'cte')
                    self.cte_names.add(cte_name)
                node.withClause = None
        return node

class ParseGraphTask(ManifestTask):
    def __init__(self, model_dir, extension, prefix='') -> None:
        super().__init__(model_dir, extension, prefix)
        self.graph = nx.DiGraph()
        self.man = {}




    def _init_graph(self):
        for unique_id, sql in self.manifest.query.items():
            try:
                vistor = QueryVistor(unique_id, sql)              
                # print(unique_id)
                nnnn = vistor.get_nodes() 
                self.graph.add_nodes_from([rel for rel in vistor.get_rel_names() if rel not in self.graph])
                
                for k, v  in nnnn.items():
                    self.graph.add_node(v.alias, title = v.alias, label = v.raw, alias = v.alias) # if v.alias not in self.graph else None
                    self.man[v.alias] = v
                    for rel in v.rel_name:
                        # print(rel)
                        self.graph.add_edge(rel, v.alias)

                    # ['size', 'value', 'title', 'x', 'y', 'label', 'color']
        
            except Exception as e:
                print(self.manifest.expect(unique_id))
                # print(e)
                logging.exception(f'{unique_id} {e}')

        print(GraphVis()(self.graph, self.man))
            
            
