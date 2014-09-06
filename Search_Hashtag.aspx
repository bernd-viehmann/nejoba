<%@ Page Title="Themensuche" Language="IronPython" MasterPageFile="~/MasterPage.master" AutoEventWireup="true" CodeFile="Search_Hashtag.aspx.py" %>

<asp:Content ID="ContentHead" ContentPlaceHolderID="head" Runat="Server">
    <style type="text/css">
        body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color:transparent;
        }
    </style>
    <script src="<%# ResolveUrl("~/js/MatrixManager.js") %>" type="text/javascript"></script>
</asp:Content>

<asp:Content ID="ContentTop" ContentPlaceHolderID="CoPlaTop" Runat="Server">
</asp:Content>

<asp:Content ID="ContentBottom" ContentPlaceHolderID="CoPlaBottom" Runat="Server">

    <div class="row"><br /></div>

    <div class="row">
        <div class="accordion" id="accordion2">
            <div class="accordion-group">
                <div class="accordion-heading">
                    <h4>
                        <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseHeader" >
                            Hashtag aussuchen
                        </a>
                    </h4>
                </div>
                <div id="collapseHeader" class="accordion-body collapse">
                    <div class="accordion-inner">
<strong>
Ein Hashtag ist ein Stichwort dem ein ‘#’ vorangestellt wurde. Auf diese Weise können Nutzer von nejoba Beiträge thematisch gruppieren. 
<br /><br />
Auf dieser Seite findest Du ein Textfeld, in das du dein gesuchtes Hashtah eingeben musst.
<br /><br />
Darunter findest du wie gewohnt den Button “Ort wechseln” um nach Region oder Stadt zu filtern. Es ist möglich Ortsunabhängig zu suchen (“Land: Alle vorhandenen”), Einträge eines Landes anzeigen zu lassen oder in der Umgebung einer Stadt zu suchen.
<br /><br />
Ganz unten kannst du mit dem Button “Liste” die Liste aller passenden Einträge anzeigen lassen. Mit “Karte” zeigt nejoba die alle passenden Einträge für die eine geographische Markierung festgelegt wurde.
<br /><br />
</strong>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="span12">
            <div class="span1"></div>
            <div class=" span10" style="background-color:White;">
                <asp:Image ID="Image1" runat="server" ImageUrl="~/style/pic/mainhead_pict_nejoba.jpg" ImageAlign="Middle" />
            </div>
            <div class="span1"></div>
        </div>
    </div>

<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
<!-- ########### LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           LOCATION_CHOOSE_AREA              LOCATION_CHOOSE_AREA           ###########-->
    <div class="row"><br /><br /><br /></div>
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
                            <strong><asp:Label ID="lbl_missing_country_selection" runat="server" Text="<br /><br />Fehler : Es wurde kein Land ausgewählt! Stadt / PLZ hängen mit dem Land zusammen."></asp:Label></strong>
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
                <!-- CHOOSE RUBRIC ########### ########### ########### ########### ########### ########### ########### ########### ########### ###########-->
                <div class="row">
                    <div class="span8 offset1">
                        <h5><asp:Label ID="lbl__show_loctn_itemOfRubric" runat="server" class="spacedTop span3" Text="Hashtag" /></h5>
                        <asp:TextBox ID="txbx_hashtag" runat="server" autocomplete="off" class="typeahead span7 pull-right" ToolTip="nejoba macht Hashtags zu regionalen Themen." EnableViewState="false" ></asp:TextBox>
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
                        <asp:LinkButton id="btn_show_loctn_list" runat="server" class="span6 btn btn-large btn-success" OnClick="HandlBtnClick" ><i class="icon-th-list icon-black"></i> Liste</asp:LinkButton>
                        <asp:LinkButton id="btn_show_loctn_map"  runat="server" class="span6 btn btn-large btn-success pull-right" OnClick="HandlBtnClick" ><i class="icon-map-marker icon-black"></i> Karte</asp:LinkButton>
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


<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->
<!-- # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # -->


<div style="display:none;">
    <asp:Label ID="timeIsNow" runat="server" ></asp:Label> 
    <asp:TextBox ID="txbx_selected_function" runat="server"></asp:TextBox>

    <!-- the hidden textbox stores the tag for a rubric -->
    <asp:TextBox ID="txbx_tagforitem" runat="server" />

    <!-- the hidden textboxes stores the name id of the hometown of user -->
    <asp:TextBox ID="txbx_location_id" runat="server" />
    <asp:TextBox ID="txbx_location_name" runat="server" />
</div>



<script type="text/javascript">
    $(document).ready(function () {
        // --------------------------------------------------------------------------------------------------------------------------------------
        // -- 
        // -- object of type matrix-manager will handle the stuff
        // -- 
        // --------------------------------------------------------------------------------------------------------------------------------------
        var matrix = new MtrxMngr();

        //
        // handler if selection-div was pressed
        //
        $("div[id*='selct_div_']").click(function (event) {
            // remove before-selection
            $('#CoPlaBottom_txbx_selected_function').val('');
            var divclicked = String(this.id);
            var rbrcTyp = divclicked.split('_')[2];
            //alert(rbrcTyp)
            $('#CoPlaBottom_txbx_selected_function').val(rbrcTyp);

            // remove before-selection
            $('#CoPlaBottom_txbx_tagforitem').val('');
            $('#CoPlaBottom_txbx_itemname').val('');
            $('select[id*="lsbx_"]').html('');                  // clean-up the previsious data in the selects for taging
            $('div[id*="slct_div_"]').hide();                   // hide all divs containing an 

            // console.log("selection div was clkicked  !" + divclicked);

            $("div[id*='dsplydiv_']").hide();
            switch (divclicked) {
                case "selct_div_economy":
                    $('#dsplydiv_economy').show();
                    break;
                case "selct_div_leisure":
                    $('#dsplydiv_leisure').show();
                    break;
                case "selct_div_society":
                    $('#dsplydiv_society').show();
                    break;
                case "selct_div_viewlist":
                case "selct_div_viewmap":
                    $('#dsplydiv_location').show();
                    break;
                case "selct_div_create_item":
                    break;
                case "selct_div_jobmarket":
                    break;

                default:
                    break;
            }
        });

        $("#btn_select_rubrcfinished").click(function (event) {
            $("#dsplydiv_selectrubric").hide();
            $("#dsplydiv_location").show();
            $("#dsplydiv_read_or_create").show();
        });

        //
        // handler if cancel was clicked
        //
        $("input[id*='btn_cancel_']").click(function (event) {
            //alert(String(this.id));
            $("div[id*='dsplydiv_']").hide();
            $('#dsplydiv_main').show();
            $("html, body").animate({ scrollTop: 0 }, 200);
        });

        // --------------------------------------------------------------------------------------------------------------------------------------
        // -- 
        // -- add the click-event-handler for the selects 
        // -- 
        // --------------------------------------------------------------------------------------------------------------------------------------
        $("select[id*='lsbx_']").click(function (event) { matrix.handleSelection(event); });

        matrix.initItemArray();             // create the array with items and positioning informations
        matrix.fillUpInitial();

        hashListFromServer = []                 // used as datasource for the bootstrap-typeahead 'txbx_hashtag'

        /*
        *  handle autocomplete for hashtags
        *
        */
        $('#CoPlaBottom_txbx_hashtag').typeahead({
            source: function (query, process) {
                var ajxurl = nejobaUrl('./ajax/dataSource__hashtags.aspx?')

                if (hashListFromServer.length == 0) {
                    return $.get(ajxurl, { query: query }, function (data) {
                        hashListFromServer = JSON.parse(data).options;
                        return process(hashListFromServer);
                    });
                }
                else {
                    if (hashListFromServer[0].slice(0, 4).toLowerCase() == query.slice(0, 4).toLowerCase()) {
                        return hashListFromServer;
                    }
                    else {
                        return $.get(ajxurl, { query: query }, function (data) {
                            hashListFromServer = JSON.parse(data).options;
                            return process(hashListFromServer);
                        });
                    }
                }
            },
            minLength: 4,
            items: 5
        });
    });
</script>



</asp:Content>
