# list_map_data.aspx.py
#
#  
#  
#  
#  
#  
#
#  
from System.Web.Configuration import *
from System.Net.Mail import *
from System.Net import NetworkCredential 
from System.Data import *

import clr                                                      # external libraries
clr.AddReference('MongoDB.Bson')                                # mongo-db
clr.AddReference('MongoDB.Driver')
from MongoDB.Bson import *
from MongoDB.Driver import *

import traceback                                # for better exception understanding
import mongoDbMgr                               # father : the acces to the database
import System.Text

tool = mongoDbMgr.mongoMgr( Page )


# ***********************************************************************************************************************************************
# Page_Load        : initializer of the webpage
#
# 18.03.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        # tool.ui.getCtrlTree( Page.Master )
        # tool.ui.hideFormAfterClick()

        pass

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return



# ***********************************************************************************************************************************************
# HndlrButtonClick    : handler for button-click-events. chose button by ID
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def HandlBtnClick(sender, e):
    try:
        url = None

        if sender.ID == 'btn_getList':
            # tool.log.w2lgDvlp('der schickma buttton wurde gerade gedr?ckt')
            loadData()

    except Exception,e:
        tool.log.w2lgError(traceback.format_exc())
        return

    if url != None :
        Response.Redirect(urlNext)




# ***********************************************************************************************************************************************
# sendToNejobaTeam    : send a mesage to the nejoba-team via email-helper-class
#
# 18.11.2012  - bervie -     initial realese
# ***********************************************************************************************************************************************
def loadData():
        try:
            # get the select-parameter
            tool.ui.getCtrlTree( Page.Master )
            country     = tool.ui.getCtrl('drpd_country').SelectedValue
            postcode    = tool.ui.getCtrl('txbx_postCode').Text 
            dataKey = country + '|' + postcode

            # create database-connection
            mngConnStrng   = WebConfigurationManager.AppSettings['mongoConn']              # connection 2 database
            dbName         = WebConfigurationManager.AppSettings['dbName']                 # get name of db from conf
            server         = MongoServer.Create(str( mngConnStrng ) )
            njbDb          = server.GetDatabase( dbName )

            table = DataTable()
            col = DataColumn()
            col = table.Columns.Add("_id"            , type("String") )
            col = table.Columns.Add("location_key"   , type("String") )
            col = table.Columns.Add("type"           , type("String") )

            col = table.Columns.Add("email"          , type("String") )
            col = table.Columns.Add("nickname"       , type("String") )
            col = table.Columns.Add("link"           , type("String") )
            col = table.Columns.Add("picturl"        , type("String") )
            
            col = table.Columns.Add("lat"            , type("String") )
            col = table.Columns.Add("lon"            , type("String") )
            col = table.Columns.Add("postcode"       , type("String") )

            collection = njbDb.GetCollection("user.final")
            query = QueryDocument("post_code_key",dataKey)
            for humans in collection.Find(query) :

                row = table.NewRow()
                row['_id']           = humans['_id'             ].ToString()
                row['location_key']  = humans['post_code_key'   ].ToString()
                row['type']          = humans['item_type'       ].ToString()
                row['email']         = humans['email'           ].ToString()
                row['nickname']      = humans['nickname'        ].ToString()
                row['link']          = humans['website'         ].ToString()
                row['picturl']       = humans['picturl'         ].ToString()
                row['lat']           = humans['lat'             ].ToString()
                row['lon']           = humans['lon'             ].ToString()
                row['postcode']      = humans['postcode'        ].ToString()
                table.Rows.Add(row)
                tool.log.w2lgDvlp('list_map_data -> loadData : ' + humans['nickname'].ToString() )

            repeater = tool.ui.getCtrl('repHumanList')
            repeater.DataSource = table
            repeater.DataBind()


    #   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # user.final
    #
    #
    #"_id" : ObjectId("51af361b773e6f09988e098b"),
    #"website" : "",
    #"post_code_key" : "DE|02977",
    #"languagecode" : "de",
    #"creation_time" : ISODate("2013-06-05T12:59:07.242Z"),
    #"nickname" : "Herr Schnitzel",
    #"fax" : "",
    #"google_plus" : "",
    #"cities" : ["50c237f1773e6f12e0076780", "50c237f3773e6f12e0076788", "50c237f1773e6f12e0076782", "50c237f2773e6f12e0076784", "50c237f3773e6f12e0076789", "50c237db773e6f12e0076717", "50c237f2773e6f12e0076785", "50c237f1773e6f12e0076781", "50c237f3773e6f12e007678b"],
    #"CAPTCHA" : "5xx1xwLf",
    #"phone" : "",
    #"account_roles" : ["free"],
    #"emailconfirm" : "njb01@t-online.de",
    #"item_type" : "human",
    #"facebook" : "",
    #"forename" : "",
    #"postcode" : "02977",
    #"city" : "",
    #"street" : "",
    #"countrycode" : "DE",
    #"picturl" : "http://guikblog.com/wp-content/uploads/2012/08/anonymus-logo-.png",
    #"marker_line" : "",
    #"familyname" : "",
    #"email" : "njb01@t-online.de",
    #"mobile" : "",
    #"info" : "",
    #"areasize" : "17",
    #"twitter" : "",
    #"skype" : "",
    #"lat" : "51.4329869178",
    #"housenumber" : "",
    #"password" : "Y2TPAEVTJDscoNnhGbxHN5qHTRcy90TN0uxp+7ZjaDmzrtDShs2o+/wFwD7lcshOtJ0nACDQO9SKuryuv6HO0Q==",
    #"GUID" : "85fe32419374403e89eb6a0a4380878f",
    #"lon" : "14.2637824408"
    #   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # initiatives.final
    #
    #"_id" : ObjectId("51af4e5c773e6f09988e0995"),
    #"txbx_emailconfirm" : "njb01@t-online.de",
    #"country_code" : "DE",
    #"txbx_picturl" : "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc1/c0.38.180.180/s160x160/375125_524041300967023_601086960_a.jpg",
    #"txbx_captcha" : "5xx1xwLf",
    #"location_key" : "DE|40212 ",
    #"txbx_socialnetwork" : "https://www.facebook.com/Occupy.Duesseldorf",
    #"marker_line" : "51.2341315027,6.77354296066\t<h4>Occupy D?sseldorf</h4>\t<div><img src=\"https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc1/c0.38.180.180/s160x160/375125_524041300967023_601086960_a.jpg\" class=\"img-polaroid\" style=\"height: 180px; width: 180px;\" alt=\"Profilbild\" /><table class=\"table table-bordered\" style=\"vertical-align: middle;width: 300px;\"><tbody><tr><td colspan=\"2\"><h6>Mitteilung:</h6><p><img src=\"http://www.occupyduesseldorf.de/wp/wp-content/uploads/2012/06/header.png\" alt=\"\"><br><br><a href=\"http://www.occupyduesseldorf.de/wp/\" rel=\"nofollow\" target=\"_blank\">http://www.occupyduesseldorf.de/wp/</a> <br><br></p></td></tr><tr><td colspan=\"2\"><a href=\"http://www.nejoba.net/njb_02/wbf_topic/parameter_result_list.aspx?loc=DE|40212 \" target=\"_blank\"><h6>regionales B?rgerforum</h6></a></td></tr><tr><td><strong>Soziales Netzwerk :</strong></td><td>https://www.facebook.com/Occupy.Duesseldorf</td></tr><tr><td><strong>Mail :</strong></td><td>info@occupyduesseldorf.de</td></tr><tr><td><strong>Hashtag :</strong></td><td>occupy</td></tr><tr><td><strong>PLZ :</strong></td><td>40212 </td></tr><tr><td><strong>Webseite :</strong></td><td> http://www.occupyduesseldorf.de/wp/ </td></tr></tbody></table></div>\thttp://maps.google.com/mapfiles/marker_black.png\t20, 34\t-10,-33\n",
    #"txbx_lat" : "51.2341315027",
    #"txbx_email" : "info@occupyduesseldorf.de",
    #"txbx_info" : "<img src=\"http://www.occupyduesseldorf.de/wp/wp-content/uploads/2012/06/header.png\" alt=\"\"><br><br><a href=\"http://www.occupyduesseldorf.de/wp/\" rel=\"nofollow\" target=\"_blank\">http://www.occupyduesseldorf.de/wp/</a> <br><br>",
    #"txbx_hashtag" : "occupy",
    #"creator_GUID" : "85fe32419374403e89eb6a0a4380878f",
    #"marker" : "http://maps.google.com/mapfiles/marker_black.png",
    #"txbx_nickname" : "Occupy D?sseldorf",
    #"type" : "monetary",
    #"txbx_lon" : "6.77354296066",
    #"txbx_postcode" : "40212 ",
    #"txbx_website" : " http://www.occupyduesseldorf.de/wp/ "












        except Exception,e:
            tool.log.w2lgError(traceback.format_exc())
                 

