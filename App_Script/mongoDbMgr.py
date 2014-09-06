# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# mongoMgr : nejobas helper class to communicate with the mongo-db
#
# constructor : no parameter      : constructor takes the configuration from the webside
# parameters        : config {}
#
#                     this is a dictionary which contains the configuration and the data of a db-job
#                     collName : name of the collection
#                     query    : the parameters for selction og the needed document(s)
#                     data     : a collection or a singleton with the data thath should be written or was read
#
# keys in the config-dict :                    
#            
#                     dbname            : name of the database
#                     connctionStrng    : string for connection-configuration
#                     collection        : name of the collection we will work on
#                     slctKey           : the selection-criteria key
#                     slctVal           : the selection-criteria value
#                     data              : the data to write or read
#
#                     addSpecialType    : define a special data-type for an element inside the update  
#                                         this dict can be defined to change the insertion-type of an element. normaly the elemts are inserted as unicode-string (no definition for the element in this dict)   
#                                         if you define a key in the val you set the string that toggles to the function for the insert. so we can add object-ids ore time-elemnts by defining them in this dict.
#
# member-fctns      : read     : load a document fom mongo
#                     insert   : save a document to memory
#                     update   : change something inside a document          
#                     delete   : delete a document  
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# 17.01.2012     - bervie -       initial realese
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


import traceback                                                # for better exception understanding
from System.Collections.Generic import *                        # collections from .net are used 
from System.Web.Configuration import *                          # web.config will be used

import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

from njbTools import *                                          # nejoba helper stuff


class mongoMgr(NjbBasic):
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # constructor. takes the base-configuration of the system in the dict config
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def __init__(self, page, config=None):
        NjbBasic.__init__(self, page)     # wake up papa
        try:
            if config == None: self.config = {}
            else: self.config = config

            # set needed default-values 
            # kys = self.config.keys()
            # if 'dbname' not in kys :         self.config.update({'dbname':'nejoba'})
            # if 'connctionStrng' not in kys : self.config.update({'connctionStrng':'mongodb://localhost'})

            # set needed default-values 
            kys = self.config.keys()
            if 'dbname' not in kys :
                confDb = WebConfigurationManager.AppSettings['dbName']
                self.config.update({'dbname' : confDb})

            if 'connctionStrng' not in kys : 
                confConctn = WebConfigurationManager.AppSettings['mongoConn']
                self.config.update({'connctionStrng':confConctn})
            
            # create the connection to the database
            self.server = MongoServer.Create( self.config['connctionStrng'] )
            self.database = self.server.GetDatabase( self.config['dbname'] )
            
            # in some cases the element-name should lead to a special data-type when the element is inserted. we copy the 
            # __class__-type into a string and overwrite the __class__ value to manipulate the real-data-type of the element
            self.nameSwitch = {'geo_answer' : "<type 'BsonObjectId'>", '_id' : "<type 'BsonObjectId'>", '_objectDetailID' : "<type 'BsonObjectId'>" }
            
            # create the switch-rules for datainsert. dict is used to call a function for the insert into database with the correspending datatype
            self.typeSwitch = { "<type 'int'>" : self.addBsonInt, 
                                "<type 'str'>" : self.addBsonStrng, 
                                "<type 'float'>" : self.addBsonDouble, 
                                "<type 'SqlString'>" : self.addBsonStrng, 
                                "<type 'list'>" : self.addBsonStrng,
                                "<type 'DateTime'>": self.addBsonDateTime,
                                "<type 'NoneType'>":self.addBsonNull,
                                "<type 'DBNull'>":self.addBsonNull,
                                "<type 'BsonObjectId'>" : self.addBsonId,
                                "<type 'BsonDouble'>" : self.addBsonDouble,
                                "<type 'BsonTimestamp'>" : self.addBsonTimeStamp,
                                "<type 'BsonDateTime'>" : self.addBsonDateTime,
                                "<type 'BsonArray'>" : self.addBsonArray,
                                "<type 'Array'>" : self.addBsonArray,
                                "<type 'BsonString'>" : self.addBsonStrng }
                                
            # the data-manipulation-dictionaries can be overwritten by the client. just define it in the config-dictonary
            if 'nameSwitch' in kys : self.typeSwitch = config['nameSwitch']
            if 'typeSwitch' in kys : self.typeSwitch = config['typeSwitch']

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # prepareConf : helper-function stores the configuration of the parameter-dictionaries. same usage in all functions 
    #
    # param:
    #   config : the dictonary contains the data needed for the mongo-db commands: collection to access; select-key; select-value
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def prepareConf(self, config):
        try:
            # generate configuration for db-access
            self.collname = config['collection']
            
            # most of the time we are using the id for the query
            kys = config.keys()
            if 'slctKey' not in kys: 
                self.slctKey  = '_id'
            else :
                self.slctKey = config['slctKey']
                
            # if using an id we have to use BsonObjectId-VAR
            if self.slctKey == '_id' : 
                self.slctVal = BsonObjectId(config['slctVal'].ToString())
            else : 
                self.slctVal = config['slctVal']
                
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # prepareElem : helper-function writes elements from a dict into a BsonDocument. It distinct between array and singleton and the datatype of 
    #               elem that is going to be inserted. the config is 
    #
    # parameter
    #  element :  a key-value pair (coming from a dictionary)
    #             element[0] : the key (identifier for the bson-elemnet in the document containing the data
    #             element[1] : the data-value. will be stored as bseon-element in the document. it is the pice of information
    #
    # returns:
    #  BsonElement  : a single element that can be added or saved in a document
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def prepareElem(self, element):
        try:
            elemKey = element[0]                                                    # key to access value
            elemVal = element[1]                                                    # data-value
            destinationType = str(elemVal.__class__)                                # decide what BSON-data-type will be used for this element
            
            if destinationType == "<type 'list'>": self.isArray = True              # if it is a list we have to create a BSON-array...
            else : self.isArray = False                                             # ... if not we only have to insert a single element
            
            # check if we have to cast the datatype of the Bson-Elem before inserting.
            # if we have a element mentioned in self.nameSwitch the system will chose the configured datatype
            abnormalKeys = self.nameSwitch.keys()
            if elemKey in abnormalKeys: destinationType = self.nameSwitch[elemKey]
            
            # insert data (for an array a couple of items)
            if self.isArray == True:
                bArr = BsonArray()
                incomingData = element[1]
                for single in incomingData:                                             # create a BsonArry with all Elemnts from incoming data
                    newItem = self.typeSwitch[destinationType](['dummy',single]) 
                    bArr.Add(newItem)
                # add the element if not already in the document
                return BsonElement( unicode(elemKey), bArr )
            else:
                newElem = self.typeSwitch[destinationType](element)
                return BsonElement( unicode(elemKey), newElem)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # add-functions : the functions creates an instance of the needed BsonDataType for writing to the database
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def addBsonInt(self, element):         return BsonInt32( element[1] )
    def addBsonStrng(self, element) :      return BsonString( element[1].ToString() )
    def addBsonDouble(self, element) :     return BsonDouble( element[1] )
    def addBsonTimeStamp(self, element) :  return BsonTimestamp( element[1] )
    def addBsonDateTime(self, element) :   return BsonDateTime( element[1] )
    def addBsonNull(self, element) :       return BsonNull.Value
    def addBsonId(self, element) :         
        self.log.w2lgDvlp('BSON_id key : ' + str(element[0]) + ' ; Value :' + str(element[1]) )
        return BsonObjectId( element[1] )
    def addBsonArray(self, element) :       return BsonArray(element[1])


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # readDoc : gets a single document by its object-id from the mongo-memory. request should be for a single document (selected with _id for example)
    #
    # param : config{} the dictionary contains the configuration for data-acess
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def readDoc(self, config):
        try:
            self.prepareConf(config)                                    # prepare configuration dictionary
            coll = self.database.GetCollection(self.collname)           # set the collection to be accesed
            qry  = QueryDocument(self.slctKey,self.slctVal)             # prepare the query to search the needed document

            doc = coll.FindOne(qry)                                     # get only the first document matching the criteria
            data = {}
            for elem in doc :                                           # copy all found elements into an dictionary
                data.update({elem.Name:elem.Value})
                
            config.update({'data':data})                                # store the data into the configuration dict to enable access from the client
            return unicode(self.slctVal)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # slctDcs : used to make a query with a couple of documents. they are stored as arry in the dictionary under data
    #
    # param     : config{} the dictionary contains the configuration for data-acess
    #             under the key 'data' this function creates an array containing every document as dictonary
    #
    # returns   : length of array = number of found documents
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def slctDocs(self, config):
        try:
            self.log.w2lgDvlp(' -- mongoMgr.slctDocs  function was entered '  )
            # self.log.w2lgDvlp( 'mongoMgr.slctDocs class of selectValue entered !!! ################################ ' )
            self.prepareConf(config)                                    # prepare configuration dictionary
            coll = self.database.GetCollection(self.collname)           # set the collection to be accesed

            element = [self.slctKey,self.slctVal]
            qry  = QueryDocument(element[0],element[1])                     # prepare the query to search the needed document

            # change the datatype of select-value if needed
            if self.slctKey in self.nameSwitch.keys(): 
                destinationType = self.nameSwitch[self.slctKey]
                convertedValue = self.typeSwitch[destinationType](element)
                # self.log.w2lgDvlp( ' key      : ' + unicode(self.slctKey))
                # self.log.w2lgDvlp( ' value    : ' + unicode(convertedValue.__class__))
                qry  = QueryDocument(self.slctKey,convertedValue)       # overwrite the query with the converted value of key

            dataSrc = []
            lstOfDocs = []
            

            self.log.w2lgDvlp(' -- mongoMgr.slctDocs  start Find() of a muti-query  '  )
            for dcumnt in coll.Find(qry) :                              # get the docs found for query
                dataSrc.append(dcumnt)
            self.log.w2lgDvlp(' -- mongoMgr.slctDocs  end Find() of a muti-query  '  )

            for dcmnt in dataSrc:                                       # get a list of 
                dataOfDcmnt = {}
                self.log.w2lgDvlp(' -- mongoMgr.slctDocs  BSON_id key : ' + str(dcmnt['_id']) )
                for elem in dcmnt:
                    dataOfDcmnt.update({elem.Name:elem.Value})
                    # self.log.w2lgDvlp( 'mongoMgr.slctDocs  key : ' +  unicode(elem.Name) + ' |  value ' + unicode(elem.Value) )
                lstOfDocs.append(dataOfDcmnt)

            config.update({'data':lstOfDocs})                           # store the data into the configuration dict to enable access from the client
            self.log.w2lgDvlp(' -- mongoMgr.slctDocs  data copied into the container ' )

            return len(lstOfDocs)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # insertDoc: write a document into the mongo-memory coming fomr the data-dictionary inside the conf-dict
    #
    # config-parameter:
    #    config{} : the dictionary contains the configuration for data-acess
    #       collection : name of the collection to work on
    #       slctKey    :  key to select a document in the collection}
    #       slctVal    :' data-value, that will be written into the database }
    #
    #
    # returns: mongo_obj_id of the new document, created by this function
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def insertDoc(self,config):
        try:
            #newDoc = BsonDocument()                                                     # prepare document
            #toInsert = config['data']                                                   # data to insert comes from configuration-dictionary
            #
            ## add the elements to the document
            #for elem in toInsert.items():                                               # insert the elems to the document in memory
            #    newDoc.Add(self.prepareElem(elem))                                      # prepareElem creates all BsonElements that will be added to the BsonDocument
            #    self.log.w2lgDvlp('mongoMgr:insertDoc  -- going to add element to doc --  : ' + unicode(elem[0]) + ' | ' + unicode(elem[1]) )

            # create the document
            newDoc = self.createDoc(config)

            # ... write the BsonDocument to the database
            coll = self.database.GetCollection[BsonDocument](config['collection'])      # set the collection to be accesed
            coll.Insert(newDoc)
            
            return unicode(newDoc['_id'])
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # createDoc : create a document from a given configuration-dictionary
    #
    # config-parameter:
    #    config{} : the dictionary contains the configuration for data-acess
    #       collection : name of the collection to work on
    #       slctKey    :  key to select a document in the collection}
    #       slctVal    :' data-value, that will be written into the database }
    #
    #
    # returns: mongo_obj_id of the new document, created by this function
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def createDoc(self,config):
        try:
            newDoc = BsonDocument()                                                     # prepare document
            toInsert = config['data']                                                   # data to insert comes from configuration-dictionary
            
            # add the elements to the document
            for elem in toInsert.items():                                               # insert the elems to the document in memory
                newDoc.Add(self.prepareElem(elem))                                      # prepareElem creates all BsonElements that will be added to the BsonDocument
                # self.log.w2lgDvlp('mongoMgr:insertDoc  -- going to add element to doc --  : ' + unicode(elem[0]) + ' | ' + unicode(elem[1]) )
            
            # ... return the BsonDocument to the database
            return newDoc

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # updateDoc: read a document from a collection in the mongo-db
    #
    # config-parameter:
    #    config{} : the dictionary contains the configuration for data-acess
    #       collection : name of the collection to work on
    #       slctKey    :  key to select a document in the collection}
    #       slctVal    :' data-value, that will be written into the database }
    #
    # returns: selection-value of the changed/updated document (normaly mongo_obj_id)
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def updateDoc(self, config):
        try:
            self.prepareConf(config)							# prepare configuration dictionary
            coll = self.database.GetCollection(self.collname)	# set the collection to be accesed
            qry  = QueryDocument(self.slctKey,self.slctVal)		# prepare the query to search the needed document
            
            selectKey = unicode(config['updatKey'])
            valToUpdate = unicode(config['updatVal'])
            newDoc = BsonDocument()										# prepare a new document for the update...
            newDoc.Add(self.prepareElem([selectKey,valToUpdate])) 	 	# ... create a valid instance in self.newDoc ...
            update = UpdateDocument('$set', newDoc)						# ... and update the data in the DB
            
            rsltDoc = coll.Update(qry,update)
            return unicode(self.slctVal)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # saveDoc: change an elemnt in a existing document or create a new element  within the existing ID 
    #
    # config-parameter:
    #    {'saveKey': key to select a document in the collection}
    #    {'saveVal':'data-value, that will be written into the database }
    #
    # 20.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def saveDoc(self, config):
        try:
            self.prepareConf(config)									# prepare configuration dictionary
            coll = self.database.GetCollection(self.collname)			# set the collection to be accesed
            qry  = QueryDocument(self.slctKey,self.slctVal)				# prepare the query to search the needed document
            
            oldDoc = coll.FindOne(qry)									# get the document that should be updated or inserted
            if oldDoc != None :
                selectedKey = unicode(config['saveKey'])
                valToSave = unicode(config['saveVal'])
                tempElem = self.prepareElem([selectedKey,valToSave])	# generate an element with the data to change
                oldDoc[tempElem.Name] = tempElem.Value					# change the source
                coll.Save(oldDoc)										# save it to the database
                
                return unicode(self.slctVal)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())
            


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # delDoc: remove a document from a collection
    #
    # config-parameter:
    #    config{} : the dictionary contains the configuration for data-acess
    #       collection : name of the collection to work on
    #       slctKey    :  key to select a document in the collection}
    #       slctVal    :' data-value, that will be written into the database }
    #
    # returns: selection-value of the deleted document (normaly mongo_obj_id)
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def delDoc(self, config):
        try:
            self.prepareConf(config)							# prepare configuration dictionary
            coll = self.database.GetCollection(self.collname)	# set the collection to be accesed
            qry  = QueryDocument(self.slctKey,self.slctVal)		# prepare the query to search the needed document
            
            coll.Remove(qry)
            return unicode(self.slctVal)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    # arrangeWebform: update the text-widgets in a webform from a given document in a mongo-collection. we call a document by the name of the 
    #                 collection and the mongo-_id. the collection with refernces to the controlls is given to update the 
    # 
    # parameter:
    #    collectionName      : name of collection to read the document from
    #    selectKey           : key-name for data-selection
    #    selectValue         : select parameter
    #    dictWithCtrls       : dictionary with the user-controls from the webform. key-names in the document and ids of the widgets must be partly identical
    #
    # 17.01.2012   - bervie-      initial realese
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    def arrangeWebform(self, collectionName, selectKey, selectValue, dictWithCtrls ):
        try:
            # load the data from the mongo-db
            readCfg = {'collection':collectionName, 'slctKey':selectKey, 'slctVal':selectValue}
            self.readDoc(readCfg)
            result = readCfg['data']
            
            # check if names are partial identicall and store the results from the db in the corresponding text-value of the widget
            wdgtNms = dictWithCtrls.keys()								# list with IDs of the widgets
            rsltKeys = result.keys()									# list with the data we had as databse-result
            
            for itm in wdgtNms:											# go through the ID of the widgets in the webform
                if itm.find('_') > 0:
                    searchStrng = itm[itm.index('_') + 1:]				# get the string after the type-prefix....
                    if searchStrng in rsltKeys:
                        valueFrmDb = result[searchStrng]
                        widget = dictWithCtrls[itm]
                        widget.Text = unicode(valueFrmDb)
            
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

