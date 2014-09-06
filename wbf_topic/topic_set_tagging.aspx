<%@ Page Title="Liste Debatten" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="topic_set_tagging.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server" EnableViewState="True">

<div class="container">
    <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
    <div ID="SetUpFiltering" runat="server" class="row span12" visible="true">

        <!-- # # #  HEADER for tuning search-results # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
        <div class="container-fluid">

        <div ID="Div1" runat="server" class="hero-unit" visible="true">

                <div class="container-fluid">
                    <div class="row-fluid">
                        <div class="span3 offset1">
                            <h3><asp:Label ID="Label12" runat="server" Text="Rubrik wählen." /></h3>
                            <br />
                            <asp:Image ID="Image2" runat="server" class="img-polaroid" ImageUrl="~/style/pic/quatschtuete.png" ToolTip="regionale Themen" />
                        </div>
                        <div class="span6 offset1">
                            <asp:Label ID="Label15" runat="server" Text="Wähle eine Rubrik aus. In nejoba sind Rubriken eine Sammlung von regionalen Themen. " />
                            <br /><br />
                            <asp:Label ID="Label13" runat="server" Text="Übergeordnete Rubriken beinhalten auch alle Unterpunkte." />
                            <br /><br />
                        </div>
                    </div>
                </div>
            </div>

            <div class="row-fluid">
                <div id="col1" class="span3 well" runat="server" visible="true">
                    <asp:ListBox ID="setRbrc_1" Rows="20" runat="server" Width="99%" AutoPostBack="true" OnSelectedIndexChanged="HandlBtnClick" />
                </div>
                <div id="col2" class="span3 well" runat="server" visible="true">
                    <asp:ListBox ID="setRbrc_2" Rows="20" runat="server" Width="99%" AutoPostBack="true" OnSelectedIndexChanged="HandlBtnClick" />
                </div>
                <div id="col3" class="span3 well" runat="server" visible="true">
                    <asp:ListBox ID="setRbrc_3" Rows="20" runat="server" Width="99%" AutoPostBack="true" OnSelectedIndexChanged="HandlBtnClick" />
                </div>
                <div id="col4" class="span3 well" runat="server" visible="true">
                    <asp:ListBox ID="setRbrc_4" Rows="20" runat="server" Width="99%" AutoPostBack="true" OnSelectedIndexChanged="HandlBtnClick" />
                </div>
            </div>

            <div class="row-fluid">
                <div id="Div2" class="span10">
                    <label class="alert alert-info">
                    <asp:Label ID="lbl_show_selection" runat="server" Text="Wähle einen Bereich aus." />
                    </label>
                </div>
               
                <div id="Div3" class="span2">
                    <asp:Button ID="btn_Next" runat="server" class="btn btn-large btn-primary btn-block pull-right" Text="Alle Rubriken" OnClick="HandlBtnClick" ToolTip="Stichwort übernehmen."/>
                </div>
            </div>
            
            <!--
            <div class="row-fluid">
                <div id="Div5" class="span10">
                    <br />
                </div>
                <div id="Div4" class="span2">
                    <asp:Button ID="btn_delete" runat="server" class="btn btn-large btn-danger btn-block pull-right" Text="Löschen" OnClick="HandlBtnClick" ToolTip="Die letzte Zuordnung wird gelöscht."/>
                </div>
            </div>
            <br /><br />
            
            <div class="row-fluid">
                <div id="Div6" class="span10">
                    <br />
                </div>
                <div id="Div7" class="span2">
                    <asp:Button ID="btn_goOn" runat="server" class="btn btn-large btn-primary btn-block pull-right" Text="Speichern" OnClick="HandlBtnClick" ToolTip="Weiter zur Texteingabe."/>
                </div>
            </div>
            -->

            <div style="visibility:hidden;">
                <asp:Label ID="lbl_indexKey" runat="server" Text=""></asp:Label>
            </div>

        </div>
    </div>
</asp:Content>

