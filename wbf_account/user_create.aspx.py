#  
# user_create.aspx.py  : prepare a new nejoba-account. this function saves the infos the user gave with encrypted passwords in the mongo
#  
#  
#  
import System
from System.Web.Configuration import *          # web.config will be used
from System import Guid                         # CREATE GLOBAL UNIQUE id
from System import Text
from System import DateTime
from System.Net import *
from System.Net.Mail import *
from System import UriPartial

import traceback                                # for better exception understanding
import random
import mongoDbMgr                               # father : the acces to the database

import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

from srvcs.tls_WbFrmClasses import CreateUser   # helper class for this dialog

# -- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -
# -- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -
# -- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- -

tool = CreateUser(Page)


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # hide the main-user-interface after a button-click and show  a please-wait sedativ
        tool.ui.getCtrlTree( Page.Master )
        tool.ui.hideFormAfterClick()

        tool.errorMessage('')

        # if user is logged_in use edit-mode for enable change of user_data
        if not IsPostBack:
            if tool.usrDt.isLoggedIn():
                ToggleEditMode()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# 05.05.2013  - bervie -     added check if invalif postcode was given
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        if sender.ID == 'btn_Create':
            if tool.usrDt.isLoggedIn():
                # change the data of logged-in user
                tool.changeUser()
            else:
                # create a new user-account
                tool.createUser()

        # when there was an mistake in user create do not make an redirect
        if tool.okFlag != 1 :
            return

        # check if we had a valid postcode. if not make no redirect
        if not tool.usrDt.userDict.has_key('cities'):
            errStr = tool.ui.getCtrl('msg_unknownPlace').Text
            tool.errorMessage(errStr)
            return

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if tool.confirmUrl != None :
        tool.log.w2lgDvlp('CreateUser redirects to : ' +  unicode(tool.confirmUrl) )
        Response.Redirect( Page.ResolveUrl( tool.confirmUrl ) )




# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# ToggleEditMode    : create user is in change-mode
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ToggleEditMode():
    try:
        # change headline from create to edit user
        newTxt = tool.gtCtl('edit_headline_label').Text
        lable = tool.gtCtl('lbl_headline')
        lable.Text = newTxt


        # change button-lable to change-user
        newTxt = tool.gtCtl('hidden_button_edit_text').Text
        button = tool.gtCtl('btn_Create')
        button.Text = newTxt

        # disable unchangeable data
        emailTxBx = tool.gtCtl('txbx_email')
        emailTxBx.Enabled = False
        emailTxBxCnf = tool.gtCtl('txbx_emailconfirm')
        emailTxBxCnf.Enabled = False
        nickTxBx = tool.gtCtl('txbx_nickname')
        nickTxBx.Enabled = False
        tool.gtCtl('alertbox').Visible = False

        # the location can also not be changed afterwards
        tool.gtCtl('txbx_postcode').Enabled = False
        tool.gtCtl('txbx_city').Enabled = False

        UserDataToUi()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return


# ***********************************************************************************************************************************************
# UserDataToUi    : get data from the user-session-dict ans copy it into the webform
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def UserDataToUi():
    try:
        # put dict-data to the webform 
        tool.ui.getCtrl('txbx_website').Text = tool.usrDt.getItem('website')
        tool.ui.getCtrl('txbx_nickname').Text = tool.usrDt.getItem('nickname') 
        tool.ui.getCtrl('txbx_fax').Text = tool.usrDt.getItem('fax') 
        tool.ui.getCtrl('txbx_phone').Text = tool.usrDt.getItem('phone') 
        tool.ui.getCtrl('txbx_forename').Text = tool.usrDt.getItem('forename') 
        tool.ui.getCtrl('txbx_postcode').Text = tool.usrDt.getItem('postcode') 
        tool.ui.getCtrl('txbx_city').Text = tool.usrDt.getItem('city') 
        tool.ui.getCtrl('txbx_street').Text = tool.usrDt.getItem('street') 
        tool.ui.getCtrl('txbx_familyname').Text = tool.usrDt.getItem('familyname') 
        tool.ui.getCtrl('txbx_email').Text = tool.usrDt.getItem('email') 
        tool.ui.getCtrl('txbx_mobile').Text = tool.usrDt.getItem('mobile') 
        tool.ui.getCtrl('txbx_skype').Text = tool.usrDt.getItem('skype') 
        tool.ui.getCtrl('txbx_housenumber').Text = tool.usrDt.getItem('housenumber') 
        tool.ui.getCtrl('drpd_language').SelectedValue = tool.usrDt.getItem('languagecode')
        tool.ui.getCtrl('drpd_country').SelectedValue = tool.usrDt.getItem('countrycode')
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('GUID') 
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('password') 
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('areasize') 
        #tool.ui.getCtrl('').Text = tool.usrDt.getItem('cities') 

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

