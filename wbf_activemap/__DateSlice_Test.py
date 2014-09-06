#
#  get slice of date ( just testing some stuff)
#
#
#  http://api.mongodb.org/csharp/1.2/html/92a76252-d1b1-1acb-4584-ad2eaeb66091.htm
#
import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
from System import DateTime

server = MongoServer.Create( 'mongodb://localhost' )
database = server.GetDatabase('henry')
collection = database.GetCollection('item.base')

idnt  = BsonObjectId('51efd5cb773e6f0ab8354d68')
start = BsonDateTime( DateTime( 2012,1,1 ) )
end   = BsonDateTime( DateTime( 2012,12,31 ) )
query = Builders.Query.GT( "creationTime", start ).LT ( end )

#print start.ToString()
#print end .ToString()
#collection.Find({created_on: {$gte: start, $lt: end}});

for row in collection.Find( query ) :    
    if row['_id'] < idnt:
        print row['_id'].ToString()

print 'danke fuer Ihre Aufmerksamkeit !!'










