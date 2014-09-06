<%@ Page Title="Aktive Menschen in einem Postleitzahlgebiet" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="list_map_users.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

<div class="container">
    <!-- Main hero unit for a primary marketing message or call to action -->
    <div class="hero-unit">
        <div class="container-fluid">
            <div class="row-fluid">
                <div class="span3 offset1">
                    <asp:Image ID="Image1" runat="server" class="img-polaroid" ImageUrl="~/style/pic/240x216_search_globe.png" ToolTip="Kartendaten durchsuchen" />
                    </div>
                <div class="span7 offset1">
                    <h4><asp:Label ID="Label2" runat="server" Text="Liste aktiver Menschen eines PLZ-Gebietes" /></h4>
                    <br />


                    <div class="span3">
                        <h5><asp:Label ID="Label11" runat="server" Text="Land" /></h5>

                        <asp:DropDownList ID="drpd_country" runat="server">
                            <asp:ListItem Text="Deutschland" Value="DE" Selected="True" />
                            <asp:ListItem Text="&Ouml;sterreich" Value="AT" />
                            <asp:ListItem Text="Schweiz" Value="CH" />
                            <asp:ListItem Text="Luxemburg" Value="LU" />
                            <asp:ListItem Text="Belgien" Value="BE" />
                            <asp:ListItem Text="Niederlande" Value="NL" />
                        </asp:DropDownList>
                        <br /><br />
                        <asp:Button ID="btn_getList" runat="server" class="btn btn-large btn-primary" Text="Auflistung" ToolTip="Liste der aktiven Menschen für dieses Postleitzahlgebiet abfragen" onclick="HandlBtnClick" />
                    </div>

                    <div class="span3 offset2">
                        <h5><asp:Label ID="lblPstCode" runat="server" Text="Postleitzahl" /></h5>
                        <asp:TextBox ID="txbx_postCode" runat="server" />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div id="divDataArea" class="well" runat="server">
    
        <!-- ############################################################################################################################################ -->
        <!--   repeaer renders stuff from db to the outside world                                                                                         -->
        <!-- ############################################################################################################################################ -->
        <asp:Repeater ID="repHumanList" runat="server">
            <ItemTemplate>
                <div>
                    <h5>
                        <asp:LinkButton ID="btn_openDebate" runat="server" ToolTip="Beitrag aufrufen" OnClick="HandlBtnClick"><%# Eval("nickname")%></asp:LinkButton>
                    </h5>
                    <small>
                        <asp:Label ID='Label8' runat="server"  Text='Standort : ' />
                        <strong>
                            <asp:Label ID='Label9' runat="server"  Text='<%# Eval("email")%>' />
                        </strong>
                        <br />
                        <asp:Label ID='Label6' runat="server"  Text='Benutzer : ' />
                        <strong>
                            <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("link")%>' />
                        </strong>
                        <strong>
                            <asp:Label ID='Label5' runat="server"  class="span12" Text='<%# Eval("picturl")%>' />
                            <br /><br />
                        </strong>
                    </small>
                                    
                </div>
                                
            </ItemTemplate>
        </asp:Repeater>
    
    </div>

</div>


<div style="visibility:hidden;">
</div>


</asp:Content>

