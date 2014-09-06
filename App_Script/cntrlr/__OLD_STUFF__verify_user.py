# ***********************************************************************************************************************************************
# logicverifyUser : business logic for verify_user.aspx.py
#                   sends the captcha mail to the user after user data was typed in
# 
#  30.11.2011   - berndv -              initial release
# ***********************************************************************************************************************************************
import mongoDbMgr           # father : the acces to the database
import traceback            # for better exception understanding

from System.Web.Security import *
from System.Drawing import *


class verifyUser(mongoDbMgr.mongoMgr):
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 3011.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa
        self.okFlag = 1                                                 # flag indicates if error occured = FALSE
        self.log.w2lgDvlp(' constructor class logicVerifyUser was called!')

    # ***********************************************************************************************************************************************
    # checkInpt : compare the user input with the values in the session-cache
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def checkInpt(self):
        try:
            # get the input from the user
            rulesConfirmed = self.ui.getCtrl('cbx_confirmBuiRules').Checked
            inptCptch = self.ui.getCtrl('txbx_code').Text
            inptPwd = self.ui.getCtrl('txbx_password').Text

            # get the defaults from the session-cache
            cptch = self.usrDt.getItem('CAPTCHA')
            pwd  = self.usrDt.getItem('password')

            # user must confirm the business-rules by checking the checkbox
            if not rulesConfirmed:
                self.ui.getCtrl('lbl_message').Text = self.ui.getCtrl('msg_notVerified').Text
                self.ui.getCtrl('lbl_message').ForeColor = Color.FromName("Red")
                self.ui.getCtrl('cbx_confirmBuiRules').BackColor = Color.FromName("Red")
                self.okFlag = 0                     # flag indicates if the input was correct
                return self.okFlag
            else:
                self.ui.getCtrl('lbl_message').ForeColor = Color.FromName("Black")
                self.ui.getCtrl('cbx_confirmBuiRules').BackColor = Color.FromName("White")


            # check if users input is correct
            if (inptCptch != cptch) or (inptPwd != pwd):
                self.ui.getCtrl('lbl_message').Text = self.ui.getCtrl('msg_inptWrong').Text
                self.okFlag = 0                     # flag indicates if the input was correct
            else:
                self.ui.getCtrl('lbl_message').Text = self.ui.getCtrl('msg_inptOk').Text
                self.dsblCtrls()
            return self.okFlag
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # dsblCtrls : disable all controls after succesfull verification
    #
    # 25.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def dsblCtrls( self ): self.ui.getCtrl('btn_save').Visible = 0


    # ***********************************************************************************************************************************************
    # createUser : create a new user from the input of the user: write the stuff into the databases ( SQL-Server & Mongo )
    #
    # 02.12.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def createUser(self):
        try:
            # write the entries form the dict into the message-log
            self.log.w2lgDvlp('logicVerifyUser(userInterface).create User was called ')

            # get user from the session-cache . works only if webform is called from create_user.aspx directly
            # for ky in self.usrDt.userDict:
            #     vl = self.usrDt.userDict[ky]
            #     self.log.w2lgDvlp('key   : ' + ky + ' ; value  : ' + vl )

            # get user from the database by the url-parameter 'key' ......
            dataDict = self.loadUserData()

            # .... and create the user with the result from MONGO-DB into the sql-server DB which is the membership-proviider for nejoba
            self.storeUserToSqlServer(dataDict)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # loadUserData : function is called from page-load. it puts all data from the session-cache into the webform
    #
    # prepare the load-dict to get the data in following way 
    #
    # collname   : the name of the collection
    # key        : the querying-key to get the data (col-name)
    # filter     : the condition that must match with the item in the queriying key
    #               
    # valNames[] : array with the keys that we will read from the document
    #              the array with keys comes from the ui. it correspondents with the textfields we have there
    #
    #
    # 02.12.2011    berndv  initial realese
    #
    # ***********************************************************************************************************************************************
    def loadUserData(self):
        try:
            # check for URL-parameter and abort if it is missing
            filter = self.Page.Request.QueryString['key']
            if filter == None:
                self.log.w2lgDvlp('logic.VerifyUser.there is the db-access-parameter missing as url-parameter')
                return

            # keylist with the names of the keys 
            # valueNames = ['debug','requestClassification','lngSttngs ','confirmPassword ','nickname','email','geo_answer','lastname','CAPTCHA','ajax_result','placeIds','streetWithNumber','GUID','password','forename','postcode','city','areaSize','passwordQuestion','_id','sqlUserId'] 

            self.log.w2lgDvlp('loadUserData : calling mongoDBMgr with |' + unicode(filter) + '|')
            ctrlDict = {'collection':'user.initial','slctKey':'GUID','slctVal':filter}
            self.readDoc(ctrlDict)
            result = ctrlDict['data']

            return result
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # storeUserToSqlServer : finally create an user in the sql-server mebership api
    #
    # 13.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def storeUserToSqlServer(self, data):
        ## create the user account in the ASP.NET membership provider
        try:
            # create a user in the 
            outs = Membership.CreateUser(   unicode(data['email']),	            # string username ( email is used to login )
                                            unicode(data['password']),	        # string password
                                            unicode(data['email']),	            # string email
                                            unicode(data['passwordQuestion']),	# string passwordQuestion
                                            unicode(data['CAPTCHA']), True)	    # string passwordAnswer

            self.log.w2lgDvlp('logicVerifyUser(userInterface).storeUserToSqlServer User store to SQL with following output from CreateUser(..) :' + str(outs[1]) )

            # if the user was created succesfully in the sql-server, we add the userid to the mongo-collection to have a bridge with 'sqlUserId'
            if 'Success' == str(outs[1]):
                usrObj = Membership.GetUser(data['email'])
                userID = unicode(usrObj.ProviderUserKey)

                self.log.w2lgDvlp('logicVerifyUser(userInterface).storeUserToSqlServer User was created with UserID in SQL-Server: ' + userID )

                # usage : update('zielsammlung', {'_id':'123'}, {'farbe':'rot'} )
                self.mongo.update('user.initial',{'_id':data['_id']},{'sqlUserId':userID})


        except Exception,e:
            errMsg = unicode('\nerror in storing the user to the sql-database !')
            errMsg += '\nuser      : ' + unicode(data['email'])
            errMsg += '\npassword  : ' + unicode(data['password'])
            errMsg += '\nemail     : ' + unicode(data['email'])
            errMsg += '\nCAPTCHA   : ' + unicode(data['CAPTCHA'])
            errMsg += '\nmessage   : ' + unicode(traceback.format_exc())

            self.log.w2lgError(errMsg)









