<%@ Page Title="dataSource__city" Language="IronPython" CodeFile="dataSource__city.aspx.py" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" EnableEventValidation="true"%>

<!DOCTYPE html>

<!-- 
                 description of the URL-PARAMETER for loading webform behind DataURL
                
                 'http://localhost:7258/njb_2/wbf_topic/mapTwo_dataSource.aspx?loc=DE%7C41836&tags=world&srchMd=OR'
                
                  amount      : the number of items that should be send by the datasource
                  lastdbid    : the last database-id that was received by the client. data-source webform 
                                should start here.
                  loc         : the geo-location as sting like "de|41836". if only "de|" is given all german 
                                results are send to the client from data-source
                  tags        : the tags we are locking for. list is comma-seperated
                  srchMd      : OR means display all items with any tag; AND menas display only tags 
                                that are labeled with all keywords
                  startdate   : a string-coded date-object to define when the event starts
                  enddate     : a string-representation of the end of the event
                
-->

<html xmlns="http://www.w3.org/1999/xhtml">

<head id="Head1" runat="server">
</head>
<body>
    <form id="form1" runat="server">
    </form>
</body>
</html>
