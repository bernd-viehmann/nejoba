<%@ Page Title="Nachbarschaftshilfe" Language="IronPython" MasterPageFile="../MasterPage.master" AutoEventWireup="true" CodeFile="jobs_list.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row">
        <div class="accordion" id="Div1">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                        <h4>regionale Anfragen</h4>
                    </a>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
                        <h5>
                            <asp:Label ID="Label1" runat="server" Text="Jobs in deiner Umgebung "></asp:Label>
                        </h5>
                        <br />
                        <asp:Label ID="Label10" runat="server" Text="Hier ist die Liste mit Arbeitsangeboten. Es werden bei der Suche auch Ergebnisse in benachbarten Orten berücksichtigt. Wenn für den Arbeitsbereich keine Auswahl getroffen wird, sondern 'bitte w&auml;hlen' angeklickt wird, werden alle Ergebnisse in der N&auml;he ber&uuml;cksichtigt." />
                        <br />
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="span12">
            <div class="span1"></div>
            <div class=" span10" style="background-color:White;">
                <asp:Image ID="Image2" runat="server" ImageUrl="~/style/pic/jobmarket_head.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

    <div class="row"><br /></div>

    <!-- ############################################################################################################################################ -->
    <!--   repeaer renders stuff from db to the outside world                                                                                         -->
    <!-- ############################################################################################################################################ -->
    <div class="accordion row" id="accordion2">
        <asp:Repeater ID="repJobList" runat="server">
                <ItemTemplate>
                <div class="accordion-group">
                    <div class="accordion-heading row">
                        <div class="span9 offset1">
                            <div class="span10">
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href='#<%# Eval("_ID")%>'>
                                    <h5><asp:Label ID="Label4" runat="server" Text='<%# Eval("subject")%>' /></h5>
                                </a>
                            </div>
                            <div class="span2">
                                <asp:HyperLink ID="hyLnk_opnJob" runat="server" class="spacedTop btn btn-info pull-right" Text='Aufrufen' NavigateUrl='<%# Eval("tagZero")%>' Target="_blank" />
                            </div>
                        </div>
                        
                    </div>

                    <div id='<%# Eval("_ID")%>' class="accordion-body collapse">
                        <div class="accordion-inner">
                            <small>
                                <div class="row">
                                    <div class="span5 offset1">
                                        <asp:Label ID='Label6' runat="server"  Text='Benutzer : ' />
                                        <asp:Label ID='lblBody' runat="server"  Text='<%# Eval("nickname")%>' />
                                    </div>
                                    
                                    <div class="span6">
                                        <asp:Label ID='Label8' runat="server"  Text='Standort : ' />
                                        <asp:Label ID='Label9' runat="server"  Text='<%# Eval("locationname")%>' />
                                    </div>
                                </div>
                            </small>
                            <div class="row">
                                <div class="span10 offset1">
                                    <asp:Label ID='Label5' runat="server"  Text='<%# Eval("body")%>' />
                                </div>
                                <div class="span1"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <br />
                </ItemTemplate>
                <SeparatorTemplate></SeparatorTemplate>
        </asp:Repeater>
    </div>
    <!-- ############################################################################################################################################ -->
    <!-- ############################################################################################################################################ -->


<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
    <!-- div_slct_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <!-- div_slct_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div class="row" id="div_slct_loctn" runat="server">
        <div class="span12 well">
            <div class="span3"></div>
            <div class="span6">
                <!-- CHOOSE COUNTRY ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl_country" runat="server" class="spacedTop span3" Text="Land" /></h5>
                        <asp:DropDownList ID="sel_country" runat="server" class="span7 pull-right"  ToolTip="Liste der derzeit verfügbaren Länder. Es muss natürlich zu Stadt oder Postleitzahl passen." />
                        <div id="nocountryselected" class="row alert alert-danger" style="display:none;">
                            <strong><asp:Label ID="lbl_missing_country_selection" runat="server" Text="Fehler : Es wurde kein Land ausgewählt! Stadt / PLZ hängen mit dem Land zusammen."></asp:Label></strong>
                        </div>
                    </div>
                </div>
                <!-- CHOOSE CITY ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl_city" runat="server" class="spacedTop span3" Text="Stadt / PLZ" ToolTip="Name oder Postleitzahl der gewünschten Daten" /></h5>
                        <asp:TextBox ID="txbx_city" runat="server" class="typeahead span7 pull-right" EnableViewState="false" autocomplete="off" ToolTip="Gib hier den Namen der gesuchten Stadt ein. Denk bitte daran das passende Land auszuwählen."/>
                    </div>
                </div>
                <div class="row"><br /><br /></div>
                <!-- BUTTONS TO GO FORWARD ### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <a id="cancle_slct_loctn" class="span6 btn btn-large btn-danger" data-toggle="tooltip" title="Ortsauswahl abbrechen"><i class="icon-circle-arrow-left icon-black"></i> Abbrechen</a>
                        <asp:LinkButton id="btn_select_slct_loctn" runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" OnClientClick="return checkForCountry();" ><i class="icon-road icon-black"></i> Weiter</asp:LinkButton>
                    </div>
                </div>
                <div class="row"><br /></div>
            </div>
        </div>
    </div>
    <!-- div_show_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <!-- div_show_loctn ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
    <div class="row" id="div_show_loctn" runat="server">
        <div class="span12 well">
            <div class="span3"></div>
            <div class="span6">
                <!-- CHOOSE JOBTYPE ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="Label2" runat="server" class="spacedTop span3" Text="Tätigkeit" /></h5>
                        <asp:TextBox ID="txbx_jobName" runat="server" class="span7 pull-right" ToolTip="Wähle einen Job-Typen. Wenn du nichts (oder einen '*') eingibst wird alles angezeigt" autocomplete="off" ReadOnly="true" />
                    </div>
                </div>
                <!-- LOCATION ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl_show_loctn_city" runat="server" class="spacedTop span3" Text="Ort" ToolTip="Momentanes Postleitzahlgebiet oder Stadt" /></h5>
                        <asp:TextBox ID="txbx_location" runat="server" class="span7 pull-right" EnableViewState="false" disabled="disabled" ToolTip="Das momentan eingestellte Postleitzahlgebiet." />
                    </div>
                </div>
                <div class="row">
                    <div class="span8 offset1">
                        <a id="button_opnloc_srch" class="span6 btn btn-large btn-warning pull-right" data-toggle="tooltip" title="Ändere den Ort der dir angezeigt wird"><i class="icon-road icon-black"></i> Ort wechseln</a>
                    </div>
                </div>
                <div class="row"><br /><br /></div>
                <!-- BUTTONS TO GO FORWARD ### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <div class="span6"></div>
                        <asp:LinkButton id="btn_load_list"  runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" ><i class="icon-th-list icon-black"></i> neu laden</asp:LinkButton>
                    </div>
                </div>
                <div class="row"><br /></div>
            </div>
            <div class="span3"></div>
        </div>
    </div>
    <div class="row"><br /><br /></div>
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->


    <div class="row"><br /><br /></div>

    <div ID="SetUpFiltering" runat="server" visible="true">
    <!-- ############################################################################################################################################ -->
    <!-- ############################################################################################################################################ -->
    <!-- ############################################################################################################################################ -->




</div> <!-- container -->

<div class="thehidden">
    <!-- hidden textfields used for statusmessages from the server (easier internationalization of the text -->
    <asp:Label ID="msg_no_jobs_found" runat="server" Text="Es wurden leider keine Arbeitsangebote gefunden !" ></asp:Label>
    <asp:Label ID="msg_wrong_location" runat="server" Text="Das Postelitzahlgebiet wurde nicht gefunden !" ></asp:Label>

    <!-- hidden text-boxes with the job-stuff -->
    <asp:TextBox ID="txbx_jobType" runat="server" />            <!-- controll is filled by javascript to store the type of job to save !! -->

    <!-- hidden textboxes for storing the location -->
    <asp:TextBox ID="txbx_location_id" runat="server" />        <!-- the hidden textboxes stores the location-id   of hometown -->
    <asp:TextBox ID="txbx_location_name" runat="server" />      <!-- the hidden textboxes stores the location-name of hometown -->
</div>
</asp:Content>

