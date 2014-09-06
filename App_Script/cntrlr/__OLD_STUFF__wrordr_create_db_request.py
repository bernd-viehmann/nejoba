# ***********************************************************************************************************************************************
# createWrordrRequest : save the input of a new createrd request/wrokorder to the database.
#
#                       this is a base-class of 
#
#
#  29.12.2011   - berndv -              initial release
#
# ***********************************************************************************************************************************************
import mongoDbMgr                               # father : the acces to the database
import traceback                                # for better exception understanding
import System.DateTime                          # to use System.DateTime.Now
from System.Web.Configuration import *          # get the web.config

class createWrordrRequest(mongoDbMgr.mongoMgr) :
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 29.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)                      # wake up papa

        self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.__init__')

        # adjust the datatype-manipulation-dictionary to insert BSON-ID and kind of stuff
        self.nameSwitch.update({'creator_id' : "<type 'BsonObjectId'>", 'location_id' : "<type 'BsonObjectId'>", 'mother_id' : "<type 'BsonObjectId'>" })


    # ***********************************************************************************************************************************************
    # createDcmnts : generate the BSON-Documents for the request-collections 
    #
    # 14.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createDcmnts(self):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.createDcmnts')
            self.crtTime = System.DateTime.Now             # all data-documents should have the same creation-time-stamp

            core   = self.crtCore()                        # 1. store the known data into the request.cores collection
            coreId = self.feedDataBase(core)

            msg    = self.crtMsg(coreId)                   # 2. put the message-text into its collection request.messages
            msgId  = self.feedDataBase(msg)

            talk   = self.crtTalk(coreId)                  # 3. prepare the document for discussions in the collection request.talks
            talkId = self.feedDataBase(talk)

            offers   = self.crtOffers(coreId)              # 4. prepare the offer-document in request.offers
            offersId = self.feedDataBase(offers)

            self.updtIdsInCore(coreId, msgId, talkId, offersId)      # 5. update the reference-ids into the core-document

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # crtCore : create the document with the core-data of a request
    #
    #       time_doc_created      : time of creation (time.now)
    #       creator_id            : db-id of the user
    #       creator_nick          : nickname of creator
    #
    #       location_id           : location-id
    #       reqstClssfctn         : string with the main-classification of the request
    #       taggingWords          : tags (or catchwords) 
    #       header_txt            : headline with max. 100 characters
    #       message_id            : id of message_text in the collection 'request.messages'
    #
    #       talkList_id           : ID of the corresponding emelment in the talk collection
    #       offerList_id          : ID of the corresponding document in the offer collection
    #
    # returns : dictionary with the needed data for the mongoDbMgr
    #
    # 15.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def crtCore(self):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.crtCore')

            # add core-data of a request
            dat = {}
            creatorId = self.usrDt.userDict['_id']
            creatorNick = self.usrDt.userDict['nickname']

            loctnId = self.formInpt['send2server_place_id']
            loctnName = self.formInpt['send2server_place_name']
            clsctn = self.formInpt['send2server_clssfctn_key']

            # ctchwrds = self.formInpt['catchwords'].split(',')
            ctchwrds = self.createCatchwords()              # catchwords must be unique and lowercase
            subjct = self.formInpt['subject'][:100]

            dat.update({'creation_time' : self.crtTime })
            dat.update({'creator_id' : creatorId })
            dat.update({'creator_nick' : creatorNick })

            dat.update({'location_id' : loctnId })
            dat.update({'reqstClssfctn' : clsctn })
            dat.update({'taggingWords' : ctchwrds })

            dat.update({'header_txt' : subjct })

            #update later with the corresponding documents
            dat.update({'message_id' : None })
            dat.update({'talkList_id' : None })
            dat.update({'offerList_id' : None })

            core = {}
            # add configuration
            core.update({'collection':'request.cores'})
            core.update({'slctKey':None})
            core.update({'data' : dat })

            return core

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # crtMsg : create the document with the message regarding to a request to the community
    #
    # parameters     : idOfCore   : the _id of the request.cores document
    # returns        : dictionary with the needed data for the mongoDbMgr
    #
    # used document-elements:
    #
    # mother_id          [IDX] : objekt-ID of the document this message belongs too ( request.cores._id 4 example )
    # time_msg_created         : datetime is creation-time of this document
    # 
    # creator_id         [IDX] : user_id of the creator of this document.
    #                            for a request in request.cores it is the user-id of the customer, who asked the request.
    #                            in an offer it is the user-id of the service-provider who offered an offer
    #                            for talk it is the user-id of the user who told the shit
    #
    # creator_nick             : Nickname of the creator. migth be displayed in the UI
    # creator_location         : home-place(location-center of the user ( locationList[0] )
    # 
    # message_txt              : message-body with a maximum of 100.000 characters
    # message_type       [IDX] : contains a string describing the type of this text, because this collection can store messages from 
    #                            a couple of documents from other collections : "request","talk","offer","mail" ect., ect. 
    # 
    # status             [IDX] : string-array with the needed status-infomation. this dependes on the message-type. an offer can be 
    #                            'accepted' or 'rejected'; a mail (later) can be 'send'; 'read';'archived'; 'replied' or 'deleted'
    #
    #
    # 18.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def crtMsg(self, idOfCore):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.crtMsg')

            # get the data from user-dictionary
            creatorId = self.usrDt.userDict['_id']
            crtr_nick = self.usrDt.userDict['nickname']
            crtr_location = self.usrDt.userDict['geo_answer'][0]
            requestText = self.formInpt['description']

            # add talk-data of a request
            dat = {}
            dat.update({'mother_id' : idOfCore })
            dat.update({'time_msg_created' : self.crtTime })
            dat.update({'creator_id' : creatorId })
            dat.update({'creator_nick' : crtr_nick })
            dat.update({'creator_location' : crtr_location })
            dat.update({'message_txt' : requestText })
            dat.update({'message_type' : 'request.cores' })                 # indicates that we have a request here, stored in request.cores
            dat.update({'status' : None })

            msg = {}
            msg.update({'collection':'request.messages'})
            msg.update({'slctKey':None})
            msg.update({'data' : dat })

            return msg

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # crtTalk        : generate the skeletton for the talk-documents of a request
    #
    # parameters     : idOfCore is the _id of the request.cores document this doc belongs to
    # returns        : dictionary with the needed data for the mongoDbMgr
    #
    # used document-elements:
    #
    # mother_id          [IDX] : objekt-ID of the document this message belongs too ( request.cores._id 4 example )
    # talk_array               : this BSON array contains a list with all discussion-text, that are stored in 'request.messages'
    #
    # 14.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def crtTalk(self, idOfCore):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.crtTalk')
            # add talk-data of a request
            dat = {}
            dat.update({'mother_id' : idOfCore })
            dat.update({'talk_array' : None })

            talk = {}
            talk.update({'collection':'request.talks'})
            talk.update({'slctKey':None})
            talk.update({'data' : dat })

            return talk

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # crtOffers  : create the skelleton document for the offers of a request
    #
    # parameters     : idOfCore is the _id of the request.cores document this doc belongs to
    # returns        : dictionary with the needed data for the mongoDbMgr
    #
    # used document-elements:
    #
    # mother_id          [IDX] : objekt-ID of the document this message belongs too ( request.cores._id 4 example )
    # offer_list               : BSON-Array with the list of IDs of given offers in 'request.messages'
    # offer_accepted_id        : Offer that was accepted by the requester
    # rating_requester         : rating of the requester done by the man-of-action, who done the job
    # rating_man_of_action     : the requester tells us here how good the job was done by the service-provider
    #
    # 14.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def crtOffers(self, idOfCore):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.crtOffers')
            # add core-data of a request
            dat = {}
            dat.update({'mother_id' : idOfCore })
            dat.update({'offer_list' : None })
            dat.update({'offer_accepted_id' : None })
            dat.update({'rating_requester' : None })
            dat.update({'rating_man_of_action' : None })

            offers = {}
            offers.update({'collection':'request.offers'})
            offers.update({'slctKey':None})
            offers.update({'data' : dat })

            return offers
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # feedDataBase : put all the stuff into a database
    #
    # param : dtSrc {}
    #         dictionary with the data that should be written to the database
    #
    # returns : lastIdx
    #           the monogo_id of the last inserted document
    #
    #
    # 14.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def feedDataBase(self, dtSrc ):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.feedDataBase')

            # debuging output
            self.log.w2lgDvlp(' * -----------------------------------------------------------------' )
            for item in dtSrc.keys():
                self.log.w2lgDvlp( ' *  key  : %20s  | value  : %20s' % (str(item), str(dtSrc[item])) )
            self.log.w2lgDvlp(' * -----------------------------------------------------------------' )

            # insert a new document into the database
            return self.insertDoc(dtSrc)

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # createCatchwords : make a unique list from the catchwords. it would be a waste of space if we have double catchwords in the system
    #
    # parameter : the char used for seperating
    # returns   : the unique list of catchwords givwen by the user
    #
    # 14.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createCatchwords(self, seperator = ','):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.createCatchwords') 

            ctchwrds = self.formInpt['catchwords'].split(seperator)

            # remove the whitespaces at begin and end
            result = []
            for cwrd in ctchwrds:
                item = cwrd.lower().strip()
                if len(item) > 0:
                    result.append(item)

            #create a unique list, delete all double strings
            for cwrd in result:
                cnt = result.count(cwrd)
                while( cnt > 1 ):
                    result.remove(cwrd)
                    cnt = result.count(cwrd)

            return result

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # updtIdsInCore : write the IDs from the daugther-documents into the core-document
    #
    # parameter : 
    #              msgId    :  the _id of the message-text
    #              talkId   :  the _id of the discussion-list
    #              offersId :  the _id of the offer-list and the informations of the accepted document
    #
    # 18.02.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def updtIdsInCore( self, coreId, msgId, talkId, offersId ):
        try:
            self.log.w2lgDvlp('\n--> ###################################################### createWrordrRequest.updtIdsInCore') 
            self.log.w2lgDvlp( ' * |   core-id        :    %20s  |  ' % (str(coreId)) )
            self.log.w2lgDvlp( ' * |   message-id     :    %20s  |  ' % (str(msgId)) )
            self.log.w2lgDvlp( ' * |   talkList-id    :    %20s  |  ' % (str(talkId)) )
            self.log.w2lgDvlp( ' * |   offerList-id   :    %20s  |  ' % (str(offersId)) )

            # update the core-document with the reference to the daughter-documents
            self.nameSwitch.update({'message_id' : "<type 'BsonObjectId'>", 'talkList_id' : "<type 'BsonObjectId'>", 'offerList_id' : "<type 'BsonObjectId'>" })

            # prepare data-dictionärie
            updt = {}
            updt.update({'collection':'request.cores'})
            updt.update({'slctKey':'_id'})
            updt.update({'slctVal':coreId})

            # insert the corresponding massage-id
            updt.update({'updatKey':'message_id'})
            updt.update({'updatVal':msgId})
            msgChangeId = self.updateDoc(updt)

            # insert the corresponding talk_id
            updt.update({'updatKey':'talkList_id'})
            updt.update({'updatVal':talkId})
            tlkChangeId = self.updateDoc(updt)

            # insert the corresponding offers-id
            updt.update({'updatKey':'offerList_id'})
            updt.update({'updatVal':offersId})
            ofrChangeId = self.updateDoc(updt)

            self.log.w2lgDvlp( ' * |      message-change-id     :    %20s  |  ' % (str(msgId)) )
            self.log.w2lgDvlp( ' * |      talkList-change-id    :    %20s  |  ' % (str(talkId)) )
            self.log.w2lgDvlp( ' * |      offerList-change-id   :    %20s  |  ' % (str(offersId)) )

            self.log.w2lgDvlp('createWrordrRequest.updtIdsInCore###################################################### --> \n') 

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



