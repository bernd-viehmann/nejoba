// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
// MatrixManager is the class managing the rtubric-selection-matrixes
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
// --------------------------------------------------------------------------------------------------------------------------------------
// --  object to define the data-item in an array
// -- 
// -- 17-06-2013  bervie  initial realese
// --------------------------------------------------------------------------------------------------------------------------------------
function DataItem(Name, TagCode, PosAry) {
    this.ValStr    = Name              || null,                                        // the string shown in ui : 'Restaurant'
    this.TagCode   = TagCode           || null,                                        // the string used for tag-definition. will start with the Tag-Prefix
    this.PosArray  = new Array(PosAry) || new Array(null, null, null, null, null)      // the array with the position-information in the matrix
};


// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

/*
 *  MatrixManager : MtrxMngr
 *
 *  the matrix-manager class is used for managing the multi-list-box selection which 
 *  defines the type of an data-item for the nejoba pinn-board.
 *
 *  it is designed for a general usage and can be used for different 
 *  it reads the source for the matrix ( a string with tab-idents ) from a server-
 *  managed div and builds an array with positioning-information
 *
 *  
 *  
 */
function MtrxMngr() {
    try
    {
        // --------------------------------------------------------------------------------------------------------------------------------------
        // --  create the source-data-array from the source-text in the div
        // --  insert the first row into the list-boxes
        // -- 
        // -- 17-06-2013  bervie  initial realese
        // --------------------------------------------------------------------------------------------------------------------------------------
        this.initItemArray = function () {
            try {
                this.Elems = new Array();                                   // will store the data-itmes we have created after clickhandler was pressed.
                var SourceLines = this.matrixSource.split('\n');            // create an array with the lines as item
                var PosArray = new Array(null, null, null, null, null);     // the Array will store the position-info of every item
                var i = 0;
                var TabsBefore = 0;
                for (; i < SourceLines.length; ) {
                    var Name = SourceLines[i].replace(/^\s+|\s+$/g, '');
                    var NumOfTabs = SourceLines[i].split('\t').length - 1;
                    if (i > 0) {
                        TabsBefore = SourceLines[i - 1].split('\t').length - 1;
                    }
                    if (PosArray[NumOfTabs] == null) {
                        PosArray[NumOfTabs] = 0;
                    }
                    else if (NumOfTabs == TabsBefore) {
                        PosArray[NumOfTabs] = PosArray[NumOfTabs] + 1;
                    }
                    else if (NumOfTabs > TabsBefore) {
                        PosArray[NumOfTabs] = PosArray[NumOfTabs] + 1;
                    }
                    else if (NumOfTabs < TabsBefore) {
                        PosArray[NumOfTabs] = PosArray[NumOfTabs] + 1;
                        for (idx = NumOfTabs + 1; idx < PosArray.length; idx++) {
                            PosArray[idx] = null;
                        }
                    }
                    // convert the position-array into a string. will be used in the UI as VALUE for the select-option
                    var ValueString = this.tagPrefix;
                    for (idx = 0; idx < PosArray.length; idx++) {
                        if (PosArray[idx] != null) { ValueString += '_' + PosArray[idx].toString(); }
                    }
                    var copyArray = new Array();
                    for (var j = 0, len = PosArray.length; j < len; j++) { copyArray[j] = PosArray[j]; }
                    var Item = new DataItem(Name, ValueString, copyArray);
                    this.Elems[this.Elems.length] = Item;
                    i++;
                }
                for (var i = 0 ; i < this.Elems.length; i++) { var Name = this.Elems[i].ValStr; }
            }
            catch (err) {
                txt = "There was an error in the MtrxMngr.initItemArray\n\n";
                txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
                console.log(txt);
            }
        };


        // --------------------------------------------------------------------------------------------------------------------------------------
        // --  the function fills the first listbox with the items we have for it : position-array = ( i,null,null,null,null )
        // -- 
        // -- 17-06-2013  bervie  initial realese
        // --------------------------------------------------------------------------------------------------------------------------------------
        this.fillUpInitial = function () {
            try {
                $('select[id*="lsbx_"]').html('');                  // clean-up the previsious data in the selects for taging
                $('div[id*="slct_div_"]').hide();                   // hide all divs containing an 

                for (var i = 0; i < this.Elems.length; i++ ) {
                    var Position = this.Elems[i].PosArray.toString().split(',');

                    // if the first item in the array is a null-value the item should be added to the select
                    if (Position[1].length == 0) {
                        var option = '<option value=' + this.Elems[i].TagCode + '>' + this.Elems[i].ValStr + '</option>';
                        //console.log('add option to select : ' + option);
                        $("#lsbx_0").append(option);
                        }
                }
                $("#slct_div_0").show();
                return;
            }
            catch (err) {
                txt = "There was an error in the MtrxMngr.fillUpInitial\n\n";
                txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
                console.log(txt);
            }
        }


        // --------------------------------------------------------------------------------------------------------------------------------------
        // --  handleSelection is called every time a select-option was clicked
        // -- 
        // -- 18-06-2013  bervie  initial realese
        // --------------------------------------------------------------------------------------------------------------------------------------
        this.handleSelection = function (event) {
            try {
                var Tag = event['target'].value;
                var Name = event['target'].text;

                // copy the needed stuff into a server-control for saving
                $('#CoPlaBottom_txbx_tagforitem').val(Tag);
                $('#CoPlaBottom_txbx_itemname').val(Name);

                var SelectClicked = event['currentTarget'].id.split('_');

                // construct the name of the next select
                var SelIdNext = parseInt(SelectClicked[1]) + 1;
                var SelectNext = SelectClicked[0] + '_' + SelIdNext;
                var SlctNxtDivToDsply = 'slct_div_' + SelIdNext;
                //console.log('handleSelection : SelectNext = ' + SelectNext);

                // update follwing selects
                if (SelIdNext < 5) {
                    // select the following elements and clean the options in the select
                    $('select[id*="lsbx_"]:gt(' + (SelIdNext - 1) + ')').html('');
                    $('div[id*="slct_div_"]:gt(' + (SelIdNext - 1) + ')').hide();

                    // get the items belonging to the selcted option
                    for (var i = 0; i < this.Elems.length; i++) {
                        var SubTag = this.Elems[i].TagCode
                        if (SubTag.indexOf(Tag) == 0) {

                            var ItemsInSupTag = SubTag.split('_').length;
                            var ItemInTag = Tag.split('_').length;

                            // copy only the elements belonging to thje next select
                            if (ItemsInSupTag == ItemInTag + 1) {
                                var option = '<option value=' + this.Elems[i].TagCode + '>' + this.Elems[i].ValStr + '</option>';
                                //console.log('found item for next select : ' + this.Elems[i].ValStr + ' - ' + SubTag + ' - nxt box ' + SelectNext + ' - ' + option);
                                $('#' + SelectNext).append(option);
                            }
                        }
                    }
                    if ($('#' + SelectNext).html() != '') {
                        // $('#' + SelectNext).show();
                        $('#' + SlctNxtDivToDsply).show();
                    }
                }
            }
            catch (err) {
                txt = "There was an error in the MtrxMngr.fillUpInitial\n\n";
                txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
                console.log(txt);
            }
        }
        // # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    }

    catch(err)
    {
        txt = "There was an error in the MtrxMngr\n";
        txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
        //console.log(txt);
    };
}

// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


$(document).ready(function () {
    // --------------------------------------------------------------------------------------------------------------------------------------
    // -- 
    // -- object of type matrix-manager will handle the stuff
    // -- 
    // --------------------------------------------------------------------------------------------------------------------------------------
    var matrix = new MtrxMngr();

    // --------------------------------------------------------------------------------------------------------------------------------------
    // -- 
    // -- add the click-event-handlers for the image-buttons
    // -- 
    // --------------------------------------------------------------------------------------------------------------------------------------
    // $("img[id*='img_select']").click(function (event) {
    $("a[id*='CoPlaBottom_hyli_select']").click(function (event) {

        // remove before-selection
        $('#CoPlaBottom_txbx_tagforitem').val('');
        $('#CoPlaBottom_txbx_itemname').val('');

        //console.log("rubric selection changed!");
        $('select[id*="CoPlaBottom_hyli_"]').hide();
        //$('select[id*="lsbx_"]:gt(' + (SelIdNext - 1) + ')').html('').hide();


        var typeButtonPressed = String(this.id);
        //console.log( 'LINK pressed for rubric :' + typeButtonPressed );
        $('#CoPlaBottom_toggle_div').text(this.typeButtonPressed);     // define the type of item that should be used

        // tagPrefix         the prefix will define the type of item (annonce/initiative/ and stuff...) 
        // matrixSource      the var will contain the string-source used for creating the matrix in the list-boxes
        switch (typeButtonPressed) {
            case "CoPlaBottom_hyli_selectEvent":
                // matrix.tagPrefix = '§EVT';
                matrix.tagPrefix = 'EVT';
                matrix.matrixSource = $('#CoPlaBottom_date_event_div').text();
                break;

            case "CoPlaBottom_hyli_selectAnnonceType":
                // matrix.tagPrefix = '§ANO';
                matrix.tagPrefix = 'ANO';
                matrix.matrixSource = $('#CoPlaBottom_annonce_div').text();
                break;

            case "CoPlaBottom_hyli_selectInitiatives":
                // matrix.tagPrefix = '§INI';
                matrix.tagPrefix = 'INI';
                matrix.matrixSource = $('#CoPlaBottom_initiative_div').text();
                break;

            case "CoPlaBottom_hyli_selectBusiness":
                // matrix.tagPrefix = '§BUI';
                matrix.tagPrefix = 'BUI';
                matrix.matrixSource = $('#CoPlaBottom_business_div').text();
                break;

            case "CoPlaBottom_hyli_selectLocation":
                // matrix.tagPrefix = '§LOC';
                matrix.tagPrefix = 'LOC';
                matrix.matrixSource = $('#CoPlaBottom_location_div').text();
                break;

            default:
                matrix.tagPrefix = ''
                //console.log("unknown button pressed for itm-type definition!");
        }
        $("#dsplydiv_selectrubric").show();

        // --------------------------------------------------------------------------------------------------------------------------------------
        // -- 
        // -- add the click-event-handler for the selects 
        // -- 
        // --------------------------------------------------------------------------------------------------------------------------------------
        $("select[id*='lsbx_']").click(function (event) { matrix.handleSelection(event); });

        matrix.initItemArray();             // create the array with items and positioning informations
        matrix.fillUpInitial();
    });
});