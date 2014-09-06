#  
# data_geoimport.aspx.py 
#  
# this form is used to copy data from a CSV into the mongo-database
#  
#
#  03.10.2012   bevie    initial realese
#  
import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *
 
import System.DateTime
import System.Drawing.Color
import System.Guid
import System.Web
from System.Web.Configuration import *
from System.IO import Path
from System.Globalization import *

import traceback                    # for better exception understanding
import re                           # for finding the taggs
import codecs
import mongoDbMgr                   # father : the acces to the database
tool = mongoDbMgr.mongoMgr(Page)

# ------------------------------------------------------------------------------------------------------------------------------------------------##__aspn.net ------------------------------------------------
# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    pass


# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# usrLoggedIn      : called after user succesfully logged in
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HndlrButtonClick(sender, e):
    try:
        if sender.ID == 'btnImport':
            GetFileToServer()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())



# ------------------------------------------------------------------------------------------------------------------------------------------------##__handler ------------------------------------------------
# ***********************************************************************************************************************************************
# GetFileToServer  : copy user-choosen file to the server
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def GetFileToServer():
    try:
        uploader = tool.gtCtl('fileUploadCtrl')

        if uploader.HasFile :
            tool.logMsg('size of file : ' + str(uploader.PostedFile.ContentLength) )

            destDir = Server.MapPath('./data')
            fileName = Path.GetFileName(uploader.PostedFile.FileName)
            destination = Path.Combine( destDir, fileName)

            tool.logMsg('place of file  : ' + str(destination) )

            uploader.SaveAs( destination )

            ImportPlaces( destination );

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())


# ***********************************************************************************************************************************************
# ImportPlaces  : read the input file and send all needed lines to the data-base-inserting-function
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def ImportPlaces(destination):
    try:
        tool.logMsg('ImportPlaces(destination) called' )

        file        = codecs.open( destination, 'rb', 'utf-8' )        # get the text-datafile
        countries   = unicode(WebConfigurationManager.AppSettings['nationList']).split(';')

        fileData = file.readlines()
        for l in fileData:
            line = unicode(l)
            arr = line.split('\t')
            # tool.logMsg('city loaded from file = : ' + arr[2] )
            if arr[0] in countries:
                SaveLine(arr)
        file.close()
        tool.logMsg('ImportPlaces(destination) : file closed !!' )

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        tool.log.w2lgError("lines processed : " + str(count))


# ***********************************************************************************************************************************************
# SaveLine  : read the input file and send all needed lines to the data-base-inserting-function
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def SaveLine(line):
    try:
        # locations are also added as BsonArray for later usage of spatial indexing
        lat  = float(line[9]   )
        long = float(line[10]  )

        geoArr = BsonArray()
        geoArr.Add( BsonDouble( lat  ) )
        geoArr.Add( BsonDouble( long ) ) 
        place = {}
        place['countryCode']    = line[0]               # : 'DE'
        place['postalCode']     = line[1]               # : '41812'
        place['placeName']      = line[2]               # : 'Erkelenz'
        place['adminName1']     = line[3]               # : 'Nordrhein-Westfalen'
        place['adminCode1']     = line[4]               # : 'NW'
        place['adminName2']     = line[5]               # : 'Reg.-Bez. Koeln'
        place['adminCode2']     = line[6]               # : '053'
        place['adminName3']     = line[7]               # : 'Heinsberg'
        place['adminCode3']     = line[8]               # : '05370'
        place['loc']            = geoArr                # : 'BsonArray( '51.0784', '6.3089' )'
        place['latitude']       = lat                   # : '51.0784'
        place['longitude']      = long                  # : '6.3089'
        place['accuracy ']      = line[11]              # : '6/n'

        storeDataDct = {'collection':'geo.cities','slctKey':None,'data': place}
        newObjId = tool.insertDoc(storeDataDct)
        
    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
