<SelectStmt targetList=(<ResTarget name='blood_urea_nitrogen' val=<ColumnRef fields=(<String val='bucket'>,)>>, 

<ResTarget val=<FuncCall funcname=(<String val='count'>,) agg_within_group=False agg_star=True agg_distinct=False func_variadic=False>>) 


fromClause=(<RangeVar relname='bun' inh=True relpersistence='p'>,) groupClause=(<ColumnRef fields=(<String val='bucket'>,)>,) 

sortClause=(<SortBy node=<ColumnRef fields=(<String val='bucket'>,)> sortby_dir=<SortByDir.SORTBY_DEFAULT: 0> sortby_nulls=<SortByNulls.SORTBY_NULLS_DEFAULT: 0>>,) 

limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> 

withClause=<WithClause ctes=(<CommonTableExpr ctename='agetbl' ctematerialized=<CTEMaterialize.CTEMaterializeDefault: 0> 
    ctequery=<SelectStmt targetList=(<ResTarget val=<ColumnRef fields=(<String val='ad'>, <String val='subject_id'>)>>,) 
    fromClause=(<JoinExpr jointype=<JoinType.JOIN_INNER: 0> isNatural=False larg=<RangeVar relname='admissions' inh=True relpersistence='p' alias=<Alias aliasname='ad'>> rarg=<RangeVar relname='patients' inh=True relpersistence='p' alias=<Alias aliasname='p'>> quals=<A_Expr kind=<A_Expr_Kind.AEXPR_OP: 0> name=(<String val='='>,) lexpr=<ColumnRef fields=(<String val='ad'>, <String val='subject_id'>)> rexpr=<ColumnRef fields=(<String val='p'>, <String val='subject_id'>)>> rtindex=0>,) 
    whereClause=<A_Expr kind=<A_Expr_Kind.AEXPR_OP: 0> name=(<String val='>'>,) lexpr=<FuncCall funcname=(<String val='datetime_diff'>,) args=(<ColumnRef fields=(<String val='ad'>, <String val='admittime'>)>, <ColumnRef fields=(<String val='p'>, <String val='dob'>)>, <A_Const val=<String val='YEAR'>>) agg_within_group=False agg_star=False agg_distinct=False func_variadic=False> rexpr=<A_Const val=<Integer val=15>>> groupClause=(<ColumnRef fields=(<String val='ad'>, <String val='subject_id'>)>,) 
    limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> op=<SetOperation.SETOP_NONE: 0> all=False> cterecursive=False cterefcount=0>, <CommonTableExpr ctename='bun' ctematerialized=<CTEMaterialize.CTEMaterializeDefault: 0> ctequery=<SelectStmt targetList=(<ResTarget name='bucket' val=<FuncCall funcname=(<String val='width_bucket'>,) args=(<ColumnRef fields=(<String val='valuenum'>,)>, <A_Const val=<Integer val=0>>, <A_Const val=<Integer val=280>>, <A_Const val=<Integer val=280>>) agg_within_group=False agg_star=False agg_distinct=False func_variadic=False>>,) fromClause=(<JoinExpr jointype=<JoinType.JOIN_INNER: 0> isNatural=False larg=<RangeVar relname='labevents' inh=True relpersistence='p' alias=<Alias aliasname='le'>> rarg=<RangeVar relname='agetbl' inh=True relpersistence='p'> quals=<A_Expr kind=<A_Expr_Kind.AEXPR_OP: 0> name=(<String val='='>,) lexpr=<ColumnRef fields=(<String val='le'>, <String val='subject_id'>)> rexpr=<ColumnRef fields=(<String val='agetbl'>, <String val='subject_id'>)>> rtindex=0>,) whereClause=<A_Expr kind=<A_Expr_Kind.AEXPR_IN: 7> name=(<String val='='>,) lexpr=<ColumnRef fields=(<String val='itemid'>,)> rexpr=(<A_Const val=<Integer val=51006>>,)> limitOption=<LimitOption.LIMIT_OPTION_DEFAULT: 0> op=<SetOperation.SETOP_NONE: 0> all=False> cterecursive=False cterefcount=0>) recursive=False> op=<SetOperation.SETOP_NONE: 0> all=False>