# ***********************************************************************************************************************************************
# create_user : business logic for create_user.aspx.py
#               finalyze the user-registration-process
# 
#  18.03.2012   - berndv -              initial release
# ***********************************************************************************************************************************************
import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database


class CreateUser(mongoDbMgr.mongoMgr):
    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
        self.okFlag = 1                     # flag indicates if the input was correct
        self.log.w2lgDvlp('constructor of class CreateUser(mongoDbMgr.mongoMgr) aufgefufen!')


    # ***********************************************************************************************************************************************
    # checkInput : check if the input-data makes sense
    #
    # 29.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def copyDataFromForerunner( self ):
        try:
            # 0. get all the shit from the url-parameter into local vars
            forename = self.Page.Request.QueryString["forename"] 
            familyname = self.Page.Request.QueryString["familyname"] 
            email = self.Page.Request.QueryString["email"] 

            # copy stuff into the webform
            self.ui.getCtrl('txbx_forename').Text = self.Page.Server.UrlDecode(forename)
            self.ui.getCtrl('txbx_name').Text = self.Page.Server.UrlDecode(familyname)
            self.ui.getCtrl('txbx_email').Text = self.Page.Server.UrlDecode(email)
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())












    

    ## ***********************************************************************************************************************************************
    ## createUser : function strats user registration process (incl. MailCaptcha)
    ##
    ## 29.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def createUser(self):
    #    self.ui.getCtrlTree( self.Page.Master )         # put all controls in a box
    #    self.checkPwd()                                 # check password input from user
    #    self.checkInput()                               # check input (all edits must be filled)
    #    self.alreadyExisting()                          # ask the membership-DB if we already have a user with that name in the system

    #    # check the ok-flag. if something went wrong abort the machinery        
    #    if self.okFlag: self.createCodes()  # generate captcha and GUID for the user
    #    if self.okFlag: self.storeInput()   # copy the user input into the input-cache

    #    # when all checks was succesfull write the user to the both dbs: sql-server for membership and mongo
    #    if self.okFlag: self.writeUser2Db() # store stuff into database

    #    return self.okFlag


    ## ***********************************************************************************************************************************************
    ## createUser : function strats user registration process (incl. MailCaptcha)
    ##
    ## 29.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def checkPwd(self):
    #    # check users password choice
    #    # REMARK: we are using hidden asp.net lable-controlls for the status messages to make the internationalization of the application more easy
    #    pwd = self.ui.getCtrl('txbx_password').Text
    #    pwdconfrm = self.ui.getCtrl('txbx_confirmPassword').Text
    #    self.log.w2lgDvlp('password             : ' + pwd)
    #    self.log.w2lgDvlp('password confirmation: ' + pwdconfrm)

    #    if (pwd != pwdconfrm) :
    #        errStr = '<font color="#FF0000"><b>' + self.ui.getCtrl('msg_pwdNotMatch').Text + '</b></font>'
    #        self.ui.getCtrl('lbl_hint').Text = errStr
    #        self.okFlag = 0
    #        return
    #    if ( len(pwd) < 5) :
    #        errStr = '<font color="#FF0000"><b>' + self.ui.getCtrl('msg_pwdToShort').Text + '</b></font>'
    #        self.ui.getCtrl('lbl_hint').Text = errStr
    #        self.okFlag = 0
    #        return


    ## ***********************************************************************************************************************************************
    ## checkInput : check users input and stop process if he has forgotten some stuff
    ##
    ## 29.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def checkInput(self):
    #    txtExsts = 1

    #    if len(self.ui.getCtrl('txbx_forename').Text) < 1: txtExsts = 0
    #    if len(self.ui.getCtrl('txbx_lastname').Text) < 1: txtExsts = 0
    #    if len(self.ui.getCtrl('txbx_email').Text) < 1: txtExsts = 0
    #    if len(self.ui.getCtrl('txbx_password').Text) < 1: txtExsts = 0
    #    if len(self.ui.getCtrl('txbx_confirmPassword').Text) < 1: txtExsts = 0
    #    if len(self.ui.getCtrl('txbx_postcode').Text) < 1: txtExsts = 0
    #    if len(self.ui.getCtrl('txbx_city').Text) < 1: txtExsts = 0

    #    #if len(self.ui.getCtrl('txbx_streetWithNumber').Text) < 1: txtExsts = 0
    #    #if len(self.ui.getCtrl('txbx_country').Text) < 1: txtExsts = 0
    #    
    #    if (txtExsts != 1) :
    #        errStr = '<font color="#FF0000"><b>' + self.ui.getCtrl('msg_inputGap').Text + '</b></font>'
    #        self.ui.getCtrl('lbl_hint').Text = errStr
    #        self.okFlag = 0
    #        return


    ## ***********************************************************************************************************************************************
    ## alreadyExisting : this function checks if we already have a user with the given mailadress
    ##
    ## 02.12.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def alreadyExisting(self):
    #    userLogin = self.ui.getCtrl('txbx_email').Text

    #    if( len(Membership.FindUsersByName(userLogin)) > 0  ):
    #        errStr = '<font color="#FF0000"><b>' + self.ui.getCtrl('msg_userAlreadyExists').Text + '</b></font>'
    #        self.ui.getCtrl('lbl_hint').Text = errStr
    #        self.okFlag = 0
    #        return self.okFlag
    #    return self.okFlag


    ## ***********************************************************************************************************************************************
    ## storeInput : write users inpuit into the User-Data dictionary
    ##
    ## 29.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def storeInput(self):
    #    # 1.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
    #    self.ui.getCtrlTxt('txbx_')
    #    for item in self.ui.ctrlDict.keys():
    #        if item != None:
    #            # get the textboxes
    #            if item.find('txbx_') == 0:
    #                key = item[5:]
    #                value = self.ui.ctrlDict[item].Text
    #                self.usrDt.addNewItem(key, value)

    #    # 2.  copy the stuff from the inputs (filled by user or ajax) into the session-cache of the user
    #    self.ui.getCtrlTxt('jvscr_')
    #    for item in self.ui.ctrlDict.keys():
    #        if item != None:
    #            # get answer from AJAX (hidden lables)
    #            if item.find('jvscr_') == 0:
    #                key = item[6:]
    #                value = self.ui.ctrlDict[item].Text
    #                self.usrDt.addNewItem(key, value)
    #                # jvscr_lngSttngs          local-settings : DE
    #                # jvscr_areaSize           size of action-area in kilomter : 33.3
    #                # jvscr_localCoordinates   lat/long of the middle and north/east/south/west of the service-area
    #                # jvscr_placeIds           place-ids of the places in the mongo-db collection with the places

    #    # 2.  write the collected data to the user-log
    #    self.log.w2lgDvlp('-- start -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )
    #    for item in self.usrDt.userDict.keys():
    #        self.log.w2lgDvlp( 'name of ctrl : ' + item + '     | text-value  : ' + self.usrDt.userDict[item] )
    #    self.log.w2lgDvlp('-- end   -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- what is in the user-session dict after storeInput' )


    ## ***********************************************************************************************************************************************
    ## writeUser2Db : store the user data in the mongo databases. the copy to the sql-server membership db will be done in verify_user.py 
    ##
    ## 09.01.2012    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def writeUser2Db(self):
    #    self.log.w2lgDvlp('CreateUser.writeUser2Db called to store the user-data into mongo.nejoba.user')

    #    # self.createNickName()   # if user has not added a nickname the function creates the name displayed in the system
    #    self.createArrays()     # convert seperated-string-list to arrays. this makes it possible 2 add indexes in the mongo-db

    #    try:
    #        # store tha stuff into tha database, brother
    #        ctrlDct = {'collection':'user.initial','slctKey':None,'data':self.usrDt.userDict}
    #        newObjId = self.insertDoc(ctrlDct)
    #        #self.mongo.save('user.initial', self.usrDt.userDict )
    #        pass
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())


    ## ***********************************************************************************************************************************************
    ## writeUser2Db : store the user data in the mongo databases. the copy to the sql-server membership db will be done in verify_user.py 
    ##
    ## 09.01.2012    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def createNickName(self):
    #    # check if there is a display-name chosen by the user. if not there will be created one automatically
    #    nckname = self.usrDt.userDict['nickname']
    #    if (len(nckname) < 1):
    #        # create a nickname from User input
    #        nckname = self.usrDt.userDict['forename'] + ' ' + self.usrDt.userDict['lastname']
    #        self.usrDt.userDict['nickname'] = nckname


    ## ***********************************************************************************************************************************************
    ## createArrays : list have to be inserted as BSON-Arrays into the mongo-db to be able to add an index to them. this function does this job 
    ##                for the place-ids and the classifications. the are converted to lists. in the mongo db inserter they will be converted to 
    ##                a BSON-array
    ##
    ## 09.01.2012    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def createArrays(self):
    #    try:
    #        self.log.w2lgDvlp('CreateUser.createArrays creating a array with the lists')

    #        # check if there is a display-name chosen by the user. if not there will be created one automatically
    #        nckname = self.usrDt.userDict['nickname']
    #        if (len(nckname) < 1):
    #            # create a nickname from User input
    #            nckname = self.usrDt.userDict['forename'] + ' ' + self.usrDt.userDict['lastname']
    #            self.usrDt.userDict['nickname'] = nckname

    #        # when the user has typed in the data for his account we haven't a sql-server object-id yet
    #        self.usrDt.userDict['sqlUserId'] = unicode('sqlserver membership info not available yet')

    #        # convert the places-sting to a list of mongo-ids
    #        places = self.usrDt.userDict['geo_answer'].rstrip(';').split(';')
    #        self.listOfIds = []

    #        for i in places:
    #            ary = i.split('|')
    #            # self.log.w2lgDvlp('place : ' + i + ' ID : ' + ary[0] )
    #            self.listOfIds.append(ary[0])

    #        self.usrDt.userDict['geo_answer'] = self.listOfIds
    #
    #        # convert the classes-sting to a list of string
    #        classTypes = self.usrDt.userDict['requestClassification'].rstrip(';').split(';')
    #        self.listOfClsTyps = []

    #        for i in classTypes:
    #            # self.log.w2lgDvlp('class : ' + i  )
    #            self.listOfClsTyps.append( i )

    #        self.usrDt.userDict['requestClassification'] = self.listOfClsTyps
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())
    #

    ## **********************************************************************************************************************************************************************************************************************************************************************************************
    ## createCodes : create an random captcha code and a GUID for the mail. the guid is used as url-parameter 
    ##
    ## 29.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def createCodes(self):
    #    try:
    #        guid = Guid.NewGuid().ToString('N')         # global unique ID

    #        # get configuration from web.config
    #        codeSource         = WebConfigurationManager.AppSettings['CodeGenQueue']
    #        lengthCaptchaStrng = int(WebConfigurationManager.AppSettings['captchaStrngLngth'])

    #        # create captcha code
    #        captcha = ''
    #        for a in range(lengthCaptchaStrng):
    #            apd = random.choice(codeSource)
    #            captcha += apd

    #        # save to session cache
    #        self.usrDt.addNewItem('GUID', guid)
    #        self.usrDt.addNewItem('CAPTCHA', captcha)

    #        return guid
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())


    ## ***********************************************************************************************************************************************
    ## prepMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    ##            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    ##
    ## 25.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def prepMail( self ):
    #    try:
    #        # get the configuration from the session cache
    #        cptch = self.usrDt.getItem('CAPTCHA')
    #        guid  = self.usrDt.getItem('GUID')

    #        # get mail-strings from the UI
    #        mailSubj = self.ui.getCtrl('msg_mailSubject').Text
    #        mailBody = self.ui.getCtrl('msg_mailBody').Text

    #        # prepare mail-text
    #        mailBody += '\n'
    #        mailBody += cptch

    #        # create a link with parameter to the confirmation web form
    #        mailBody += '\n\n'
    #        captchaWebForm = WebConfigurationManager.AppSettings['captchaWebForm']        
    #        mailBody += '<' + captchaWebForm + guid + '>'
    #        self.log.w2lgDvlp(mailBody)

    #        self.mailSubj = unicode(mailSubj)
    #        self.mailBody = unicode(mailBody)
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())


    ## ***********************************************************************************************************************************************
    ## sendMail : to finalize the user-registration an email with a captcha code is send to the user. the user must enter this captcha code and 
    ##            his password in the verification webform AppSettings['captchaWebForm']. the message for that mail is porepared here
    ##
    ##            IMPORTANT: it migth be necesary to change the iis configuration
    ##            http://forums.asp.net/t/1404427.aspx/1
    ##
    ##            http://celestialdog.blogspot.com/2011/04/how-to-send-e-mail-using-ironpython.html
    ##
    ## 25.11.2011    berndv  initial realese
    ## ***********************************************************************************************************************************************
    #def sendMail( self ):
    #    try:
    #        smtpServer = WebConfigurationManager.AppSettings['smtpServer']
    #        smtpUser = WebConfigurationManager.AppSettings['smtpUser']
    #        smtpPwd = WebConfigurationManager.AppSettings['smtpPwd']
    #        fromAddr = WebConfigurationManager.AppSettings['cptchSndrAdrss']
    #        toAddrs = self.usrDt.getItem('email')

    #        try:
    #            #Create A New SmtpClient Object
    #            mailClient = SmtpClient(smtpServer,25)
    #            mailCred = NetworkCredential()
    #            mailCred.UserName = smtpUser
    #            mailCred.Password = smtpPwd
    #            mailClient.Credentials = mailCred

    #            msg = MailMessage( fromAddr, toAddrs)
    #            msg.SubjectEncoding = Text.Encoding.UTF8;
    #            msg.BodyEncoding =  Text.Encoding.UTF8;

    #            msg.Subject = self.mailSubj
    #            msg.Body = self.mailBody

    #            mailClient.Send(msg)
    #        except Exception,e:
    #            self.log.w2lgError(traceback.format_exc())
    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())


