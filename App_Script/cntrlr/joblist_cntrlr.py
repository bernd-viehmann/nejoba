# ***********************************************************************************************************************************************
# editor.cntrlr.py : controller class for the nejoba text input webform
# 
#  03.10.2012   bervie    initial realese
#
# ***********************************************************************************************************************************************
#from System.Web.Security import *
#from System import DateTime
import System.DateTime
import System.Drawing.Color

import traceback                    # for better exception understanding
import mongoDbMgr                   # father : the acces to the database



class JobList(mongoDbMgr.mongoMgr):

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 03.10.2012   bervie    initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        mongoDbMgr.mongoMgr.__init__(self, pg)      # wake up papa ; mother njbTools is included by inheritance!
        
        self.wrtLog('joblist.cntrlr.py : constructor of class JobList(mongoDbMgr.mongoMgr) was called !')
        



    # ***********************************************************************************************************************************************
    # kickstart 
    # get the jobs in job_list and write them into the log
    #
    #
    #
    # 03.10.2012   bervie    initial realese
    # ***********************************************************************************************************************************************
    def kickstart(self):
        self.wrtLog('JobList(..).kickstart was called !')
        
        #testList = ["adam","bernd","Karl","Johannes","Werner"]
        repeater = self.gtCtl('repJobList')
        #repeater.DataSource = testList
        repeater.DataSource = self.jobSrc.jobTable
        repeater.DataBind()



    # ***********************************************************************************************************************************************
    # publish
    # a new job-offer will be inserted in the job-cache and the database
    #
    # 03.10.2012   bervie    initial realese
    # ***********************************************************************************************************************************************
    #def publish(self):
    #    try:
    #        creation_date = System.DateTime.Now                                         
    #        dayOfAction = System.DateTime.Parse( self.gtCtl('txbTimeOfAction').Text )
    #        data = {"locationID" : self.gtCtl('selLocation').SelectedIndex ,
    #        "jobTypeID" : self.gtCtl('selJobType').SelectedIndex ,
    #        "timeOfAction" : dayOfAction, 
    #        "created" : creation_date,
    #        "headerTxt" : self.gtCtl('txbHeader').Text ,
    #        "bodyTxt" : self.gtCtl('txtMain').Text }


    #        # put the stuff into the database
    #        ctrlDct = {'collection':'job.main','slctKey':None,'data': data}
    #        newObjId = self.insertDoc(ctrlDct)

    #        self.wrtLog("Editor->published a new job with _id : " + newObjId )

    #        # show that job was done  and hide the edit 
    #        self.gtCtl("lblStatusMsg").Visible = True
    #        self.gtCtl("lblStatusMsg").ForeColor = System.Drawing.Color.Green
    #        self.gtCtl("lblStatusMsg").Text = "Vielen Dank. Ihre Eingaben wurden erfolgreich gespeichert.";
    #        self.gtCtl("divStatus").Visible = True
    #        self.gtCtl("divEditArea").Visible = False
    #        

    #    except Exception,e:
    #        self.log.w2lgError(traceback.format_exc())
