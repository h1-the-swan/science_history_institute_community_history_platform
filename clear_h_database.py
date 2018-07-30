from h import db

for tbl_name in session.bind.table_names():
    print("deleting table {}...".format(tbl_name))
    session.bind.execute("DROP TABLE `{}`;".format(tbl_name))
