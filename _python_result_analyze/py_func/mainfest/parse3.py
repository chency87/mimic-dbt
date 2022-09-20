
from copy import deepcopy
from dataclasses import dataclass



from pglast.visitors import Visitor, Ancestor, Delete, referenced_relations, Skip
from pglast import parse_sql, ast, Node, scan


from pglast.stream import IndentedStream, RawStream, maybe_double_quote_name
from typing import List


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
        self._parse_selectStmt(self.root[0].stmt, self.model_name)

    def get_nodes(self):
        return self.nodes

    def get_cte_names(self):
        return self.cte_names

    def get_rel_names(self):
        return self.rel_names

    def _parse_selectStmt(self, node: Node, model_name, skip_with_clause = None):
        ## Parse the with clause if exist
        node = self._parse_withClause(node, skip_with_clause)
        ## Parse the from clause, divide the sub query into several
        from_clause = node.fromClause
        new_from_clause =self._parse_fromClause(from_clause= from_clause)
        node.fromClause = new_from_clause

        ## Parse the where clause
        print(RawStream()(node))
        self.nodes[model_name] = RawStream()(node)


    def _parse_fromClause(self, from_clause):
        assert isinstance(from_clause, tuple)
        new_from_clause = []
        for clause in from_clause:
            new_clause = clause
            if isinstance(clause, ast.RangeSubselect) and clause.subquery:                
                self._parse_selectStmt(node = clause.subquery, model_name = clause.alias.aliasname)
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
                # r_n, c_n, n_list = _parse_Selectstmt(node = with_clause, model_name= None, cte_names = cte_names )
                # rel_names.update(r_n)
                # nodes.update(n_list)
            else:
                for cte in with_clause.ctes:
                    cte_name = maybe_double_quote_name(cte.ctename)
                    self._parse_selectStmt(node= cte.ctequery, model_name= cte_name)
                    self.cte_names.add(cte_name)
                node.withClause = None
        return node


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
    vistor = QueryVistor('raw', raw)
    print(len(vistor.get_nodes()))
    # print(vistor.get_nodes())
    # for k,v in vistor.get_nodes().items():
    #     print(f'mode name : {k}')
    #     print(v)
    #     print()

    cte_name = vistor.get_cte_names()
    print(cte_name)

    # print()
    print(vistor.get_rel_names())

