# ***********************************************************************************************************************************************
# logicVerifyUser : business logic for verify_user.aspx.py
#                   sends the captcha mail to the user after user data was typed in
# 
#  30.11.2011   - berndv -              initial release
# ***********************************************************************************************************************************************
import mongoDbMgr           # father : the acces to the database
import traceback            # for better exception understanding

# from System.Web.Security import *


class LogIn(mongoDbMgr.mongoMgr):
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to kickstart the machine
    #
    # 23.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa
        self.okFlag = 1                                                 # flag indicates if error occured = FALSE
        self.log.w2lgDvlp(' constructor class LogIn was called!')



    # ***********************************************************************************************************************************************
    # loadUser : get the user data from the mongo db and store it in the session-cache
    #
    # 23.01.2012    berndv  initial realese
    # ***********************************************************************************************************************************************
    def loadUser(self, userName):
        try:
            # get hiom from the user data collection
            usrToLoad = {'collection':'user.initial','slctKey':'email','slctVal':userName}
            self.readDoc(usrToLoad)

            # pump him to the log-file for debuging
            for itm in usrToLoad['data'].items():
                strOut = unicode(itm[0]) + '\t' + unicode(itm[1]) + '\t'
                self.log.w2lgDvlp(' mongo DB    data            :' + strOut )

            # copy the db-values into the session-cache
            for itm in usrToLoad['data'].items():
                self.usrDt.addNewItem( unicode(itm[0]), unicode(itm[1]) )

            # check the data in the session-cache
            self.log.w2lgDvlp(' # * + # * + # * + # * + # * + # * + # * + # * + # * + # * + ' + strOut )
            for itm in self.usrDt.userDict.items():
                strOut = unicode(itm[0]) + '\t' + unicode(itm[1]) + '\t'
                self.log.w2lgDvlp(' session user data           : ' + strOut )
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

