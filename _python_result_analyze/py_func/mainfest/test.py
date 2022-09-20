from collections import Counter
from pglast.visitors import Visitor
from pglast import parse_sql

raw = """
WITH agetbl AS
(
    SELECT ad.subject_id
    FROM admissions ad
    INNER JOIN patients p
    ON ad.subject_id = p.subject_id
    WHERE
     -- filter to only adults
    DATETIME_DIFF(ad.admittime, p.dob, 'YEAR') > 15
    -- group by subject_id to ensure there is only 1 subject_id per row
    group by ad.subject_id
)
, bun as
(
  SELECT width_bucket(valuenum, 0, 280, 280) AS bucket
  FROM labevents le
  INNER JOIN agetbl
  ON le.subject_id = agetbl.subject_id
  WHERE itemid IN (51006)
)
SELECT 	F1.bucket
FROM 	bun F1
WHERE 	exists
	(SELECT	*
	FROM 	Serves S2
	WHERE 	S2.bar = F1.bar
	AND 	exists
		(SELECT	*
		FROM 	Likes L3
		WHERE 	L3.person = F1.person
		AND 	S2.drink = L3.drink))"""
class Stats(Visitor):
    def __call__(self, node):
        self.counters = Counter()
        super().__call__(node)
        return self.counters

    def visit(self, ancestors, node):
        self.counters.update((node.__class__.__name__,))

stats = Stats()
print(stats(parse_sql(raw)))

# <RawStmt stmt=<SelectStmt targetList=(<ResTarget val=<ColumnRef fields=(<String val='pvt'>, <String val='subject_id'>)>>, <ResTarget val=<ColumnRef fields=(<String val='pvt'>, <String val='charttime'>)>>, <ResTarget name='aniongap' val=<FuncCall funcname=(<String val='avg'>,) args=(<CaseExpr args=(<CaseWhen expr=<A_Expr kind=<A_Expr_Kind.AEXPR_OP: 0> name=(<String val='='>,) lexpr=<ColumnRef fields=(<String val='label'>,)> rexpr=<A_Const val=<String val='ANION GAP'>>> result=<ColumnRef fields=(<String val='valuenum'>,)>>,) defresult=<A_Const val=<Null>>>,) agg_within_group=False agg_star=False agg_distinct=False func_variadic=False>>, <ResTarget name='albumin' val=<FuncCall funcname=(<String val='avg'>,) args=(<CaseExpr args=(<CaseWhen expr=<A_Expr kind=<A_Expr_Kind.AEXPR_OP: 0> name=(<String val='='>,) lexpr=<ColumnRef fields=(<String val='label'>,)> rexpr=<A_Const val=<String val='ALBUMIN'>>> result=<ColumnRef fields=(<String val='valuenum'>,)>>,) defresult=<A_Const val=<Null>>>,) agg_within_group=False agg_star=False agg_distinct=False func_variadic=False>>, <ResTarget name='bands' val=<FuncCall funcname=(<String val='avg'>,) args=(<CaseExpr args=(<CaseWhen expr=<A_Expr kind=<A_Expr_Kind.AEXPR_OP: 0> name=(<String val='='>,) lexpr=<ColumnRef fields=(<String val='label'>,)> rexpr=<A_Const val=<String val='BANDS'>>> result=<ColumnRef fields=(<String val='valuenum'>,)>>,) defresult=<A_Const val=<Null>>>,) agg_within_group=False agg_star=False agg_distinct=False func_variadic=False>>) fromClause=(<RangeVar relname='pvt' inh=True relpersistence='p' alias=<Alias aliasname='pvt'>>, <RangeVar relname='bu' inh=True relpersistence='p' alias=<Alias aliasname='bu'>>) limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> op=<SetOperation.SETOP_NONE: 0> all=False> stmt_location=0 stmt_len=0>



# (<RangeSubselect lateral=False subquery=<SelectStmt limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> op=<SetOperation.SETOP_UNION: 1> 

# all=False 

# larg=<SelectStmt targetList=(<ResTarget val=<ColumnRef fields=(<String val='d1'>, <A_Star>)>>,) fromClause=(<RangeVar relname='msdrg' inh=True relpersistence='p' alias=<Alias aliasname='d1'>>,) limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> op=<SetOperation.SETOP_NONE: 0> all=False> 


# rarg=<SelectStmt targetList=(<ResTarget val=<ColumnRef fields=(<String val='d1'>, <A_Star>)>>,) fromClause=(<RangeVar relname='hcfadrg' inh=True relpersistence='p' alias=<Alias aliasname='d1'>>,) limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> op=<SetOperation.SETOP_NONE: 0> all=False>> alias=<Alias aliasname='d'>>,)


def _yield_pos(idx):
    i = 0
    while True:
        y = yield i + idx * 50
        idx = idx if y is None else y
        i += 1


        
gen = _yield_pos(0)
v0 = next(gen)

# print(next(gen))
print(v0)

print(gen.send(4))
print(gen.send(4))

# print(next(_yield_pos(2, 1)))