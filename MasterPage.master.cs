using System;
using System.Text;
using System.Security.Cryptography;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Web.UI.HtmlControls;
using System.Web.Configuration;

using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Builders;

public class Account
{
    public string email { get; set; }
    public string password { get; set; }
}

public partial class MasterPage : System.Web.UI.MasterPage
{
    //protected HtmlControl accountdiv { get; set; }
    //HtmlControl logindiv { get; set; }
    //public HyperLink hyLnk_nejoba { get; set; }

    protected void Page_Load(object sender, EventArgs e)
    {
        // for resolving path to javascripts dynamically
        Page.Header.DataBind();

        // check if we have a looged-in email in session-cache
        // and show needed controlls and hide unneeded stuff
        if (Session["LOGGEDIN_EMAIL"] != null)
        {
            // user is logged in
            //accountdiv.Visible = true;

            hyLnk_endUserSession.Visible = true;
            divider_endUserSession.Visible = true;

            logindiv.Visible = false;
            this.enableLinks(true);
        }
        else
        {
            // user is not logged in
            // accountdiv.Visible = false;

            hyLnk_endUserSession.Visible = false;
            divider_endUserSession.Visible = false;

            logindiv.Visible = true;
            // this.enableLinks(false);

            //hyLnk_userHome.Visible = false;
            hyLnk_userHome.Text = "Anmelden";
            hyLnk_userHome.ToolTip = "Anmeldung für registrierte Benutzer";
            hyLnk_maintainAccount.Text = "Konto erstellen";
            hyLnk_maintainAccount.ToolTip = "Erstelle Dir ein Benutzerkonto";

            
        }
    }


    protected void HndlrButtonClick(Object sender, EventArgs e)
    {
        // 
        var uiEmail = txbx_email.Text.Trim();
        var uiPwrd = txbx_password.Text.Trim();

        UnicodeEncoding uEncode = new UnicodeEncoding();
        byte[] bytPassword = uEncode.GetBytes(uiPwrd);
        SHA512Managed sha = new SHA512Managed();
        byte[] hash = sha.ComputeHash(bytPassword);

        var crypted = Convert.ToBase64String(hash);

        // prepare mongo-connection
        var connection = WebConfigurationManager.AppSettings["mongoConn"];
        var dbname = WebConfigurationManager.AppSettings["dbName"];

        var server = MongoServer.Create(connection);
        var db = server.GetDatabase(dbname);
        var collection = db.GetCollection("user.final");
        var query = Query.EQ("email", uiEmail);

        var allItems = collection.Find(query);

        var usrData = allItems.ToList();

        if (usrData.Count < 1) this.SendToLogInPage();  // found nothing
        
        var guid = Convert.ToString(usrData[0]["GUID"]);
        var pwd = Convert.ToString(usrData[0]["password"]);

        // send to next page
        if (pwd == crypted) this.SendToStartPage(uiEmail);
        else this.SendToLogInPage();
        
        return;
    }

    /* SendToStartPage()
     * 
     * store email in session-cache and redirect to userhome. there user-data will be loaded by given email
     * 
     * */
    protected void SendToStartPage(string email)
    {
        Session["LOGGEDIN_EMAIL"] = email;      // Session["LOGGEDIN_EMAIL"] will initiate the load and login
                                                // of user-data in the webform AppSettings["userStartPage"] == usere_home

        // redirect user home after succesfully log-in
        Response.Redirect(Page.ResolveUrl(WebConfigurationManager.AppSettings["UserMainPage"]));
    }


    /* SendToLogInPage()
     * 
     * store email in session-cache and redirect to userhome. there user-data will be loaded by given email
     * 
     * 11.12.2013  bervie changed : created a static info-page to inform user about unsuccesfull login
     * */
    protected void SendToLogInPage()
    {
        // Response.Redirect( Page.ResolveUrl(WebConfigurationManager.AppSettings["LogIn"]) );            // redirect user home after succesfully log-in
        Response.Redirect(Page.ResolveUrl(WebConfigurationManager.AppSettings["LogInFailure"]));            // redirect user home after succesfully log-in
    }



    /* enableLinks()
     * 
     * store email in session-cache and redirect to userhome. there user-data will be loaded by given email
     * 
     * */
    protected void enableLinks(bool doIt)
    {
        if (doIt == true)
        {
            //li_1.Attributes.Remove("class");     create in forum is always enabled 02.12.2013
            li_3.Attributes.Remove("class");
            li_4.Attributes.Remove("class");
            li_5.Attributes.Remove("class");
            //li_6.Attributes.Remove("class");     create in forum is always enabled 02.12.2013
            li_7.Attributes.Remove("class");
            li_8.Attributes.Remove("class");
        }
        else
        {
            //li_1.Attributes.Add("class", "disabled");               create in forum is always enabled 02.12.2013
            li_3.Attributes.Add("class", "disabled");
            li_4.Attributes.Add("class", "disabled");
            li_5.Attributes.Add("class", "disabled");
            //li_6.Attributes.Add("class", "disabled");     create in forum is always enabled 02.12.2013
            li_7.Attributes.Add("class", "disabled");
            li_8.Attributes.Add("class", "disabled");
        }
    }







}
