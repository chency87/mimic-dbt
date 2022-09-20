

from copy import deepcopy
from dataclasses import dataclass



from pglast.visitors import Visitor, Ancestor, Delete, referenced_relations, Skip
from pglast import parse_sql, ast, Node, scan


from pglast.stream import IndentedStream, RawStream, maybe_double_quote_name
from typing import List

def _parse_Selectstmt(node: ast.SelectStmt, model_name = None, cte_names=None, skip_with_clause=None):
    cte_names = set() if cte_names is None else cte_names.copy()
    rel_names = set()
    nodes = {}

    ## parse withClause
    if node.withClause and node.withClause is not skip_with_clause:
        with_clause = node.withClause
        if with_clause.recursive:
            raise ('Cannot resolve recursive CTE query')
            cte_names.update({maybe_double_quote_name(cte.ctename): cte.ctequery}
                                      for cte in with_clause.ctes)
            r_n, c_n, n_list = _parse_Selectstmt(node = with_clause, model_name= None, cte_names = cte_names )
            rel_names.update(r_n)
            nodes.update(n_list)
        else:
            for cte in with_clause.ctes:
                cte_name = maybe_double_quote_name(cte.ctename)
                tmp_r, _, n_list = _parse_Selectstmt(node = cte.ctequery, model_name= cte_name, cte_names= cte_names)
                rel_names.update(tmp_r)
                cte_names.add(cte_name)
                nodes.update(n_list)
            node.withClause = None
            r_n, c_n, n_list = _parse_Selectstmt(node = node, model_name= model_name, cte_names= cte_names, skip_with_clause= with_clause)
            rel_names.update(r_n)
            cte_names.update(c_n)
            nodes.update(n_list)

    ## Parse the from clause, divide the sub query into several
    from_clause = node.fromClause
    new_from_clause, n_l = _parse_fromClause(from_clause= from_clause)
    node.fromClause = new_from_clause
    nodes[model_name] = RawStream()(node)
    nodes.update(n_l)
    return cte_names, rel_names, nodes

def _parse_fromClause(from_clause):
    assert isinstance(from_clause, tuple)
    nodes = {}
    new_from_clause = []
    for clause in from_clause:
        new_clause = clause
        if isinstance(clause, ast.RangeSubselect) and clause.subquery:
            r_name, c_name, n_list = _parse_Selectstmt(node = clause.subquery, model_name = clause.alias.aliasname)
            new_clause = ast.RangeVar(relname= clause.alias.aliasname, inh= True, relpersistence= 'p', alias= clause.alias)
            nodes.update(n_list)
        new_from_clause.append(new_clause)
    return new_from_clause, nodes

def _parse_rangeVar():
    pass

def _parse_withClause(node, model_name, cte_names, skip_with_clause):
    cte_names = set() if cte_names is None else cte_names.copy()
    rel_names = set()
    nodes = {}

    if node.withClause and node.withClause is not skip_with_clause:
        with_clause = node.withClause
        if with_clause.recursive:
            raise ('Cannot resolve recursive CTE query')
            cte_names.update({maybe_double_quote_name(cte.ctename): cte.ctequery}
                                      for cte in with_clause.ctes)
            r_n, c_n, n_list = _parse_Selectstmt(node = with_clause, model_name= None, cte_names = cte_names )
            rel_names.update(r_n)
            nodes.update(n_list)
        else:
            for cte in with_clause.ctes:
                cte_name = maybe_double_quote_name(cte.ctename)
                tmp_r, _, n_list = _parse_Selectstmt(node = cte.ctequery, model_name= cte_name, cte_names= cte_names)
                rel_names.update(tmp_r)
                cte_names.add(cte_name)
                nodes.update(n_list)
            node.withClause = None
            r_n, c_n, n_list = _parse_Selectstmt(node = node, model_name= model_name, cte_names= cte_names, skip_with_clause= with_clause)
            rel_names.update(r_n)
            cte_names.update(c_n)
            nodes.update(n_list)

    pass

def _parse_SortClause():
    pass


class QueryReferencedRelations(Visitor):
    """Concrete implementation of the :func:`.referenced_relations` function.

    :param set cte_names: the set of surrounding CTE names
    :param WithClause skip_with_clause: skip this clause, when specified

    Calling an instance of this class will return a set of the names of the
    relations referenced by the given :class:`node <pglast.ast.Node>`.
    """

    def __init__(self, model_name = None, cte_names=None, skip_with_clause=None):
        super().__init__()
        self.cte_names = set() if cte_names is None else cte_names.copy()
        self.skip_with_clause = skip_with_clause
        # self.sub_query = set() if sub_query is None else sub_query.copy()
        # self.skip_with_subquery = skip_with_subquery
        self.rel_names = set()
        self.model_namme = model_name
        self.nodes = {}
   

    def __call__(self, node):
        super().__call__(node)
        return self.rel_names, self.cte_names, self.nodes

    def _get_counters(self):
        return {'Counters': None}
    def _get_nodes(self):
         return self.nodes

    def _parse_fromClause(self, from_clause):
        assert isinstance(from_clause, tuple)
        new_from_clause = []
        for clause in from_clause:
            new_clause = clause
            if isinstance(clause, ast.RangeSubselect) and clause.subquery:
                r_name, c_name, n_list = QueryReferencedRelations(model_name = clause.alias.aliasname) (clause.subquery)                
                new_clause = ast.RangeVar(relname= clause.alias.aliasname, inh= True, relpersistence= 'p', alias= clause.alias)
                self.nodes.update(n_list)
            new_from_clause.append(new_clause)
            if isinstance(clause, ast.RangeVar):
                tname = maybe_double_quote_name(clause.relname)
                if clause.schemaname:
                    tname = f'{maybe_double_quote_name(clause.schemaname)}.{tname}'
                if clause.catalogname:
                    tname = f'{maybe_double_quote_name(clause.catalogname)}.{tname}'
                if tname not in self.cte_names:
                    self.rel_names.add(tname)
        return new_from_clause



    def visit_SelectStmt(self, ancestors: Ancestor, node: Node):
        # CTEs are tricky to get right, as issue #106 demonstrates!
        #
        # We must first collect the CTE names as well as the table referenced by their
        # queries, and then process the statement with that knowledge.
        #
        # In the normal case, each CTE must be processed in order, with the CTE names found
        # earlier; in the "WITH RECURSIVE" case all its CTEs must be considered valid at
        # the same time.
        # For CTE query, set withClause to None
        # For Sub query in FromClause, build a new RangeVar node

        if node.withClause and node.withClause is not self.skip_with_clause:
            with_clause = node.withClause
            if with_clause.recursive:
                self.cte_names.update({maybe_double_quote_name(cte.ctename): cte.ctequery}
                                      for cte in with_clause.ctes)
                r_n, c_n, n_list = QueryReferencedRelations(model_name= cte_name, cte_names= self.cte_names )(with_clause)
                self.rel_names.update(r_n)
                self.nodes.update(n_list)
            else:
                for cte in with_clause.ctes:
                    cte_name = maybe_double_quote_name(cte.ctename)
                    tmp_r, _, n_list = QueryReferencedRelations(model_name= cte_name, cte_names= self.cte_names )(cte)
                    self.rel_names.update(tmp_r)
                    self.cte_names.add(cte_name)
                    self.nodes.update(n_list)

            node.withClause = None
            r_n, c_n, n_list = QueryReferencedRelations(model_name= self.model_namme, cte_names= self.cte_names, skip_with_clause= with_clause)(node)
            self.rel_names.update(r_n)
            self.cte_names.update(c_n)
            self.nodes.update(n_list)
            return Skip

        ## Parse the from clause, divide the sub query into several
        from_clause = node.fromClause
        new_from_clause = self._parse_fromClause(from_clause= from_clause)
        node.fromClause = new_from_clause

        ## Build Node for every parts. Ignore queries in where clause
        # if ('whereClause') in ancestors:
        #     print('==========================')
        # for ans in ancestors:
        #     print(ans)
        print(ancestors)
        # print('')
        self.nodes[self.model_namme] = RawStream()(node)
        
        # return Skip
    # def visit(self, aancestors, node):
    #     # if isinstance(node, ast.where)
    #     print('VISITING where clause')

    def visit_WithClause(self, ancestors, node):
        if node is self.skip_with_clause:
            return Skip

    def visit_RangeVar(self, ancestors, node):
        "Collect relation names, taking into account defined CTE names"       
        tname = maybe_double_quote_name(node.relname)
        if node.schemaname:
            tname = f'{maybe_double_quote_name(node.schemaname)}.{tname}'
        if node.catalogname:
            tname = f'{maybe_double_quote_name(node.catalogname)}.{tname}'
        if tname not in self.cte_names:
            self.rel_names.add(tname)        
        return Skip


if __name__ == '__main__':
    raw = """
        WITH agetbl AS (
    with bun as (
        SELECT
            width_bucket(valuenum, 0, 280, 280) AS bucket
        FROM
            labevents le
            INNER JOIN agetbl2 ON le.subject_id = agetbl2.subject_id
        WHERE
            itemid IN (51006)
    )
    SELECT
        ad.subject_id
    FROM
        bun ad
        INNER JOIN patients p ON ad.subject_id = p.subject_id
    WHERE
        -- filter to only adults
        DATETIME_DIFF(ad.admittime, p.dob, 'YEAR') > 15 -- group by subject_id to ensure there is only 1 subject_id per row
    group by
        ad.subject_id
)
SELECT
    pvt.subject_id,
    pvt.charttime,
    avg(
        CASE
            WHEN label = 'ANION GAP' THEN valuenum
            ELSE NULL
        END
    ) AS ANIONGAP,
    avg(
        CASE
            WHEN label = 'ALBUMIN' THEN valuenum
            ELSE NULL
        END
    ) AS ALBUMIN,
    avg(
        CASE
            WHEN label = 'BANDS' THEN valuenum
            ELSE NULL
        END
    ) AS BANDS
FROM
    (
        SELECT
            le.subject_id,
            le.hadm_id,
            le.charttime,
            CASE
                WHEN itemid = 50868 THEN 'ANION GAP'
                ELSE NULL
            END AS label,
            CASE
                WHEN itemid = 50862
                AND valuenum > 10 THEN NULL
                ELSE valuenum
            END AS valuenum
        FROM
            labevents le
        WHERE
            le.ITEMID in (50868, 50862, 51144, 51300)
            AND valuenum IS NOT NULL
            AND valuenum > 0
    ) pvt,
    (
        select
            *
        from
            (
                SELECT
                    *
                FROM
                    Likes L3,
                    bbb F1
                WHERE
                    L3.person = F1.person
            ) ff
    ) bu"""
    root = parse_sql(raw)
    print(type(root))
    r_n, c_n, n_l = _parse_Selectstmt(root[0].stmt, model_name= 'raw')
    print(r_n)
    print(c_n)
    print(n_l)
    for k, v in n_l.items():
        print(f' model name is {k}')
        print(v)
        print()

