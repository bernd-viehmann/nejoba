<%@ Page Title="Empfang PayPal" Language="IronPython" CodeFile="pay_receive.aspx.py" Inherits="Microsoft.Scripting.AspNet.UI.ScriptPage" EnableEventValidation="true"%>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head runat="server">
    <title>Zahlungsstatus empfangen</title>
    <link href="../style/faaap.css" rel="stylesheet" type="text/css" />
</head>

<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #  -->

<body>
    <form id="form1" runat="server">
        <div class="headertop">PayPal Empfang</div>             

        <div id="mainarea" runat="server" visible="true">
            Die Form wird von PayPal aufgerufen zur Bearbeitung von Zahlungen
        </div>
    </form>
</body>
</html>

