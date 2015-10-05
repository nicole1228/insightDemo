
# coding: utf-8

import createDB as go


go.connectAndCreate(dbName='news')

go.buildSchema(tables=tables)


