mysqlTables = {
         "articles":
              (("id" , "integer unsigned not null auto_increment"),
              ("source" , "varchar(45) not null"),
              ("companyName", "varchar(200) not null"),
              ("companyId", "integer unsigned not null"),
              #("headline" , "varchar(200) not null"),
              #("leadParagraph" , "text not null"),
              ("body" , "text not null"),
              #("body" , "blob not null"),
              #("body" , "text SET CHARACTER SET utf8"),
              #("image" , "longblob not null"),
              ("url", "varchar(200) not null"),
              ("pubDate", "date not null"),
              ("primary key" , '(id)')),
         "companies":
              (("id", "integer unsigned not null auto_increment"),
               ("name", "varchar(200) not null"),
               ("primary key" , '(id)'))
            }

tables = {"articles":
              (("id" , "integer unsigned not null auto_increment"),
              ("source" , "varchar(45) not null"),
              ("headline" , "varchar(200) not null"),
              ("leadParagraph" , "text not null"),
              ("image" , "longblob not null"),
              ("primary key" , '(id)')),
         "companies":
              (("id", "integer unsigned not null auto_increment"),
               ("name", "varchar(200) not null"),
               ("primary key" , '(id)'))
            }
