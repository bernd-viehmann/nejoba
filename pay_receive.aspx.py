# ***********************************************************************************************************************************************
# edit_annonce
# 
#  16.04.2012   - berndv -              initial release
# ***********************************************************************************************************************************************
from System import *
from System.IO import *
from System.Text import *
from System.Net import *
from System.Web import *

import traceback                                    # for better exception understanding

# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
#  user creation
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 

class payReceive():

    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, pg):
        try:
            self.log = pg.Application['njbLOG']
            if self.log == None:
                self.log = tools.tls_LogCache.LogCache(pg.Application)
                pg.Application['njbLOG'] = self.log

            self.log.w2lgDvlp('PayPal Instant Payment Notification (IPN) received : constructor of payReceive called!')

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())



    # ***********************************************************************************************************************************************
    # constructor : call the base class constructor to initialize log, cache, ui-helper and page-member
    #
    # 28.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def receive( self ):
        try:

            # Post back to either sandbox or live
            strSandbox = "https://www.sandbox.paypal.com/cgi-bin/webscr"
            strLive = "https://www.paypal.com/cgi-bin/webscr"
            req = WebRequest.Create(strSandbox)
 
            # Set values for the request back
            req.Method = "POST"
            req.ContentType = "application/x-www-form-urlencoded"
            param = Request.BinaryRead(HttpContext.Current.Request.ContentLength)
            strRequest = Encoding.ASCII.GetString(param)
            strRequest += "&cmd=_notify-validate"

            req.ContentLength = strRequest.Length

            rquescht = strRequest.split('&')

            for item in rquescht:
                self.log.w2lgDvlp('Request Parameter :' + str(item) )


            # for proxy
            # proxy = WebProxy( Uri("http://url:port#") )
            # req.Proxy = proxy
 
            # Send the request to PayPal and get the response
            streamOut = StreamWriter(req.GetRequestStream(), Text.Encoding.ASCII)
            streamOut.Write(strRequest)
            streamOut.Close()

            streamIn = StreamReader(req.GetResponse().GetResponseStream())
            strResponse = streamIn.ReadToEnd()
            streamIn.Close();

            self.log.w2lgDvlp('strResponse 79 :' + str(strResponse) )

            if strResponse == "VERIFIED":
                # check the payment_status is Completed
                # check that txn_id has not been previously processed
                # check that receiver_email is your Primary PayPal email
                #check that payment_amount/payment_currency are correct
                ## process payment
                self.log.w2lgDvlp('PayPal receive VERIFIED was called ')
                pass

            elif strResponse == "INVALID":
                # log for manual investigation
                self.log.w2lgDvlp('PayPal receive INVALID was called ')
                pass
            
            else:
                # log response/ipn data for manual investigation
                self.log.w2lgDvlp('PayPal receive UNKNOWN (else) was called ')
                pass

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 

logic = payReceive(Page)

# ***********************************************************************************************************************************************
# PageLoad : Get the HTML-document from database if present and copy it to the TinyMCE editor
# 
#  16.04.2012   - berndv -              initial release
# ***********************************************************************************************************************************************
def Page_Load(sender, e):
    try:
        logic.receive()


        pass
        if not IsPostBack:
            pass

    except Exception,e:
        logic.log.w2lgError(traceback.format_exc())

       

















# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 
# # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # ** # 


#public partial class csIPNexample : System.Web.UI.Page
#{
#    protected void Page_Load(object sender, EventArgs e)
#    {
#        //Post back to either sandbox or live
#        string strSandbox = "https://www.sandbox.paypal.com/cgi-bin/webscr";
#        string strLive = "https://www.paypal.com/cgi-bin/webscr";
#        HttpWebRequest req = (HttpWebRequest)WebRequest.Create(strSandbox);
# 
#        //Set values for the request back
#        req.Method = "POST";
#        req.ContentType = "application/x-www-form-urlencoded";
#        byte[] param = Request.BinaryRead(HttpContext.Current.Request.ContentLength);
#        string strRequest = Encoding.ASCII.GetString(param);
#        strRequest += "&cmd=_notify-validate";
#        req.ContentLength = strRequest.Length;

#/////////////////////////////
# 
#        //for proxy
#        //WebProxy proxy = new WebProxy(new Uri("http://url:port#"));
#        //req.Proxy = proxy;
# 
#        //Send the request to PayPal and get the response
#        StreamWriter streamOut = new StreamWriter(req.GetRequestStream(), System.Text.Encoding.ASCII);
#        streamOut.Write(strRequest);
#        streamOut.Close();
#        StreamReader streamIn = new StreamReader(req.GetResponse().GetResponseStream());
#        string strResponse = streamIn.ReadToEnd();
#        streamIn.Close();

#/////////////////////////////

# 
#        if (strResponse == "VERIFIED")
#        {
#            //check the payment_status is Completed
#            //check that txn_id has not been previously processed
#            //check that receiver_email is your Primary PayPal email
#            //check that payment_amount/payment_currency are correct
#            //process payment
#        }
#        else if (strResponse == "INVALID")
#        {
#            //log for manual investigation
#        }
#        else
#        {
#            //log response/ipn data for manual investigation
#        }
#    }
#}
#// --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  
