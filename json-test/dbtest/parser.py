import sqlparse

splited_query = sqlparse.split('select * from foo; select * from bar;')
sql2=splited_query[0]
#print(type(sql2))
sql3=sqlparse.format(sql2, reindent=True, keyword_case='upper')
#print(sql3)

stmts = sqlparse.parse("select f1, f2+f3 from foo;")
stmt = stmts[0]
for i in range(0, len(stmt.tokens)):
    if stmt.tokens[i].ttype == sqlparse.tokens.Keyword:
        print("'", stmt.tokens[i].normalized, "'", stmt.tokens[i].ttype)