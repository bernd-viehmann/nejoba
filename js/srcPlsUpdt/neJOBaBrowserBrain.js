// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   List Extractor Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is the client-entrance for the data. it handles the communication to the server-data-source
//   and stores the received itmes in a global array.
//
//   this class is the data-container for the client. it also handles the pagging of datat to display.
//   additionally there is a server-side sclicing. when the 
//
//
// IMPORTANT: The server sends his data-array backwards. so the Pages-array starts at the end of data.
//
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//         AjxParam = {};                                                            object to store the attributes for the AJAX-Parameter
//         AjxParam.UrlCache = '../wbf_activemap/dataSource__cache.aspx'             source-url for items from the cache
//         AjxParam.UrlMongo = '../wbf_activemap/dataSource__mongo.aspx'             source-url for items from the database
//
//         UrlParam = {};
//         UrlParam.ResultLength = typeof rsltLngth !== 'undefined' ? rsltLngth : 1000;        maximum amount of items that will be in the result-set of the AJAX Call
//         UrlParam.ItemType = typeof itemType !== 'undefined' ? itemType : 'list';  define what kind of items should be loaded. 
//                                                                                   map : we load map-marker-items. must have location-coordinates
//                                                                                   date : we load date-items. must have a valid 'from'-date
//                                                                                   list : load every item for displaying a list. this kind of item is not pre-filtered
//         UrlParam.Loc = undefined;                                                 location : '0|' for undefined; 'AT|' for country austria; 'DE|41836' for Hueckelhoven in germany
//         UrlParam.Tag = undefined;                                                 hashtags. if we have a rubric-definition it is the first item in aray
//         UrlParam.StartDate = undefined;                                           the search-date starting
//         UrlParam.EndDate = undefined;                                             the search-date ending
//         UrlParam.SrchMode = undefined;                                            search-mode can be 'AND' or 'OR'
//
//         IntParam
//         IntParam.PageLength = typeof pgLen !== 'undefined' ? pgLen : 100;        number of items that are send from the list-extractor to the client in one go
//         IntParam.PageActive = undefined;                                         ID of last loaded page ( page is the segment that is send to the projector-class )
//         UrlParam.SliceActive = 0;                                                remind on what slide on the server we are currently reading?
//         IntParam.CrsCmd = '';                                                    the CursorCommand controlls the load of the next item
//
//         Items  the list with all data that we have received until now. this is a list of data-items that came from server via AJAX
//
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//         serverSliceLoad()                        the function loads a part of the active slice on the server and copies this data into the member-array Items
//         getUrlParams()                           check if params were changed (reset class if so) and copy the user-input into the meber-attributes
//         prepareUrl()                             build the appropiet URL for AJAX request
//         clientPageSend()                         the functions is called to dispaly a new portion of data on the webform. it calls the receive-methode of the projector class
//         turnThePage(bool ForwardDirection)       change the page (stored in the local item-cache) to display
//         loadInitial()                            start data-load : reset class and take care of the new url-parameters 
//




/*
 *  ListExtractor
 *
 *  this class gets the data from the itam-app-cache with java-calls. it stores the 
 *  items in an array and is responsible for the paging of the received itmes.
 *  
 * constructor-parameter
 *  
 * itemType     = define typ of constructor (map/list/date)  the datasource-webform creates the JSON-items depending on thatz value (map-items need no date; list items need all
 * rsltLngth    = the number of items that will be returned by the AJAX data-source in a single call. these results will be stored in a 
 * pgLen        = the items that should be displayed once on the projector-page. this is internal and not send to server
 *
 * 18.07.2013  - bervie -   initial realese
 *
 */
function ListExtractor(itemType, rsltLngth, pgLen) {

    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    //
    // Member-Attributes
    //
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  

    // parameter for the server-communication
    this.AjxParam = {};                                                                 // object to store the attributes for the AJAX-Parameter
    // this.AjxParam.Tmplt = '../wbf_activemap/dataSource__cache.aspx'                  // source-url for items from the cache
    // this.AjxParam.Tmplt = './wbf_activemap/dataSource__cache.aspx'                   // source-url for items from the cache

    this.AjxParam.Tmplt = nejobaUrl('./wbf_activemap/dataSource__cache.aspx');          // source-url for items from the cache
    this.AjxParam.AjaxUrl = '';                                                          // source-url for items from the cache

    // URL-parameter will be send to the data-source-webform
    this.UrlParam = {};
    this.UrlParam.SliceActive = 0;                                                      // remind on what slide on the server we are currently reading?
    this.UrlParam.CrsCmd = '';                                                          // the cursor-command parameter is responsible for the start-positining of the read-cursor in the server-load-webform
                                                                                        // possible values
                                                                                        // '' (String.Empty)            we start at the beginning for a new slice. 
                                                                                        // '51f2ea6c773e6f0f5090d0cf'   the BSON-ID of the Item which was loaded last.
                                                                                        //                              cursor must be placed after this item
                                                                                        // 'end_of_data'                thie command means that the end of the database is reached. UI should create a message to the user
                                                                                        //
    this.UrlParam.ResultLength = typeof rsltLngth !== 'undefined' ? rsltLngth : 1500;   // maximum amount of items that will be in the result-set of the AJAX Call
    this.UrlParam.ItemType     = typeof itemType !== 'undefined' ? itemType : 'list';   // define what kind of items should be loaded. 
                                                                                        // map : we load map-marker-items. must have location-coordinates
                                                                                        // date : we load date-items. must have a valid 'from'-date
                                                                                        // list : load every item for displaying a list. this kind of item is not pre-filtered
    this.UrlParam.Loc        = undefined;                                               // location : '0|' for undefined; 'AT|' for country austria; 'DE|41836' for Hueckelhoven in germany
    this.UrlParam.Tag        = undefined;                                               // hashtags. if we have a rubric-definition it is the first item in aray
    this.UrlParam.StartDate  = undefined;                                               // the search-date starting
    this.UrlParam.EndDate    = undefined;                                               // the search-date ending
    this.UrlParam.SrchMode   = undefined;                                               // search-mode can be 'AND' or 'OR'

    // internal parameter and setings for the list-extractor
    this.IntParam = {};
    this.IntParam.PageActive    = 0;                                                    // ID of last loaded page ( page is the segment that is send to the projector-class )
    this.IntParam.PageLength    = typeof pgLen !== 'undefined' ? pgLen : 150;           // number of items that are send from the list-extractor to the client in one go

    // the data-container
    this.Items = [];            // the list with all data that we have received until now. this is a list of data-items that came from server via AJAX

    // bind the buttons to the handlers
    $('#foreward_in_list').click(function () {
        if ($('#foreward_in_list').hasClass('disabled') != true) {
            lstExtr.turnThePage('forward');
            $('#back_in_list').removeClass('disabled');
        }
    });

    $('#back_in_list').click(function () {
        if ($('#back_in_list').hasClass('disabled') != true ) {
            lstExtr.turnThePage('backward');
            $('#foreward_in_list').removeClass('disabled');
        }
    });


    // console.log('ListExtractor : attribute-values ITEM_TYPE ' + String(this.AjxParam.ItemType) + ' SLICE_LEN: ' + String(this.AjxParam.amount) + ' PAGE_LENGTH: ' + String(this.AjxParam.PageLen));

    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    //
    // control-functions the start an action. these functions are called from the projector class 
    //
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
     * loadInitial()
     *
     * the function is the main-event handler. it is called when the user press the search-button and from constructor.
     * resetz all data loaded yet and begins with a new server-load-process
     *
     * 18.07.2013  - bervie -   initial realese
     *
     */
    this.loadInitial = function () {
        console.log('ListExtractor.loadInitial called');

        // reset the internal params
        this.Items = [];
        this.IntParam.PageActive = 0;
        this.UrlParam.SliceActive = 0;
        this.UrlParam.CrsCmd = '';

        this.getUrlParams();
        this.turnThePage();
    }


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * resetSearchDialog()
    *
    * this is the click-event-handler for deleting the search-parameter-dialog
    *
    * 22.07.2013  - bervie -   initial realese
    *
    */
    this.clearSearchDialog = function () {
        console.log('ListExtractor.clearSearchDialog called ' );
        $("#CoPlaBottom_sel_country option[value='0']").attr('selected', true);
        $('#CoPlaBottom_txbx_postCode').val('');
        $("#CoPlaBottom_txbx_timeFrom").datepicker("setDate", null);
        $("#CoPlaBottom_txbx_timeTo").datepicker("setDate", null);
        $('#CoPlaBottom_txbx_hashtag').val('');
        $('#CoPlaBottom_txbx_tagforitem').val('');
        $('#CoPlaBottom_txbx_itemname').val('');

        return false;
    }


    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    //
    // STUFF for the the asynchronus data load
    //
    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * getUrlParams()
    *
    * check if params were changed (reset class if so) and copy the user-input into the meber-attributes
    * the URL string construction will be done in 'prepareUrl'-function
    *
    * returns false if nothing has been changed since last call. then the ListExtractor can go on with the existing data
    *
    */
    this.getUrlParams = function () {
        console.log('ListExtractor.getUrlParams called');

        // 1. at first users settings will be copied into local object
        //
        this.UrlParam['Loc'] = $('#CoPlaBottom_sel_country').val() + '|' + $.trim($('#CoPlaBottom_txbx_postCode').val());
        this.UrlParam['SrchMd'] = 'OR'

        var FromDate = $("#CoPlaBottom_txbx_timeFrom").datepicker("getDate");
        if (FromDate != null) {
            var from_date = String(FromDate.getDate());
            var from_month = String(FromDate.getMonth() + 1);
            var from_year = String(FromDate.getFullYear());
            this.UrlParam.StartDate = from_year + '-' + from_month + '-' + from_date;
        }
        else {
            this.UrlParam.StartDate = '';
        }
        var ToDate = $("#CoPlaBottom_txbx_timeTo").datepicker("getDate");
        if (ToDate != null) {
            var to_date = String(ToDate.getDate());
            var to_month = String(ToDate.getMonth() + 1);
            var to_year = String(ToDate.getFullYear());
            this.UrlParam.EndDate = to_year + '-' + to_month + '-' + to_date;
        }
        else {
            this.UrlParam.EndDate = '';
        }

        // the rubric and the tags given by user ( can also be ',auto, giraffe' if atarting rubric is missing
        var rubrc = $('#CoPlaBottom_txbx_tagforitem').val();
        var tgs = $('#CoPlaBottom_txbx_hashtag').val();
        tgs = tgs.toLowerCase();
        tgs = tgs.replace(/#/g, '');     // replace all '#' because they are incompatible for usage in an URL-Parameter
        
        this.UrlParam.Tags = rubrc + ',' + tgs;

        return;
    }

    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * prepareUrl()
    *
    * create the URL for the AJAX request
    * 
    *
    */
    this.prepareUrl = function () {
        console.log('ListExtractor.prepareUrl called');
        var ParamStng = '?';
        for (var name in this.UrlParam) {
            var val = this.UrlParam[name];
            if (val != null) { ParamStng += name + '=' + String(val) + '&'; }
        }
        this.AjxParam.AjaxUrl = this.AjxParam.Tmplt + $.trim(ParamStng.slice(0, -1));      // remove last '&'
        return ParamStng;
    }


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * serverSliceLoad()
    *
    * the function loads a part of the active slice on the server and copies this data into the member-array Items
    * here the ajax-magic is happening
    *
    * HINT : the instance of the ListExtractor MUST be named lstExtr
    *        the asyncron function that receives the data calls the ItemContainer like this:
    *        lstExtr.Items.push(newDataItem);
    *
    * 18.07.2013 - bervie - initial realese
    * 10.08.2013 - bervie - added warning if nothing was loaded
    *
    */
    this.serverSliceLoad = function () {
        console.log('ListExtractor.serverSliceLoad was called');
        $('#loadNwait').modal('show');
        this.prepareUrl();          // build a string with the AJAX-call-URL
        $.getJSON(this.AjxParam.AjaxUrl, function (jsonObj) {
            var amountItems = -1;
            $.each(jsonObj.items, function (idx, value) {
                lstExtr.Items.push(value);
                amountItems = idx;
            });
            console.log('Amount of items loaded from server : ' + (amountItems + 1));

            // store the config-parameters in the local vars
            lstExtr.UrlParam.SliceActive = jsonObj.config.SliceActive;
            lstExtr.UrlParam.CrsCmd = jsonObj.config.CrsCmd;

            console.log('configuration received from server :  ACTIVE-SLICE    ' + lstExtr.UrlParam.SliceActive);
            console.log('configuration received from server :  CRSR_OFFSET     ' + lstExtr.UrlParam.CrsCmd);
            console.log('configuration received from server :  len of array    ' + lstExtr.Items.length);
            console.log('configuration received from server :  first item      ' + lstExtr.Items[0]);

            // if we have an empty answer show 'no date' message else show the data
            if (lstExtr.Items[0]['_objectDetailID'] != undefined) {
                lstExtr.clientPageSend();
                $('#loadNwait').modal('hide');

                // todo: receive the map-configuration lat,lon,zoom {}["mapcnf"] 
            }
            else {
                $('#noDataFound').modal('show');
                $('#loadNwait').modal('hide');
                
                //$('#foreward_in_list').addClass('disabled');
                $('#back_in_list').addClass('disabled');
            }
            
        });
        return;
    }


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * turnThePage()
    *
    * handler for the arrow-button which change the currently displayed data
    *
    * 18.07.2013  - bervie -   initial realese
    *
    */
    this.turnThePage = function (direction) {
        console.log('ListExtractor.turnThePage called with DIRECTION : ' + String(direction));

        // the forward-button was pressed -> get the next items
        if (direction == 'forward') {
            // forward means to the left : page-index will be - 1
            // console.log('ListExtractor.turnThePage  TURN THE PAGE FORWARD    ->');
            this.IntParam.PageActive = this.IntParam.PageActive - 1;    // ! ! ! ! ! ! ! ! ! we get data from newer items to older. so forwar in UI means bachward in the list
        };

        // the backward-button was pressed -> go back in the JSON-client-list and display already displayed stuff
        if (direction == 'backward') {
            // console.log('ListExtractor.turnThePage  TURN THE PAGE BACKWARD   <-');
            if (this.IntParam.PageActive > 0) { $('#foreward_in_list').removeClass('disabled'); }       // disable the forward-button if we have reached the start-point
            this.IntParam.PageActive = this.IntParam.PageActive + 1;                                    // ! ! ! ! ! ! ! ! ! we get data from newer items to older. so backward in UI means forward in the list
        };

        // enable/disable buttons by the currentz active page 
        if (this.IntParam.PageActive == 0) {
            $('#foreward_in_list').addClass('disabled');
            $('#back_in_list').removeClass('disabled');
        }
        else {
            $('#foreward_in_list').removeClass('disabled');
            $('#back_in_list').removeClass('disabled');
        }

        // get the page-bounds to display only a part of the data we have.
        this.setPageBounds();
        var lastItemIndx = this.Items.length - 1;

        if (lastItemIndx < this.ItmLstLftIdx) {           // if we reached the end of local Items-List start a new load from the server
            if (this.UrlParam.CrsCmd == 'end_of_data') {
                // the left page index is bigger than the end of the item-array .
                // go back to last valid page
                // alert('Keine weiteren Daten vorhanden !');
                // ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
                $('#endOfDataReached').modal('show');

                console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                console.log('-NO MORE DATA - - WILL NOT BE DISPLAYED - - -  ');
                console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                console.log('ListExtractor.turnThePage - - - - - - - - - -  ');
                console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                console.log('  current page       : ' + String(this.IntParam.PageActive));
                console.log('  this.ItmLstLftIdx  : ' + String(this.ItmLstLftIdx));
                console.log('  this.ItmLstRgtIdx  : ' + String(this.ItmLstRgtIdx));
                console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                console.log('  ACTIVE-SLICE       : ' + this.UrlParam.SliceActive);
                console.log('  CRSR_OFFSET        : ' + this.UrlParam.CrsCmd);
                console.log('  length Items[]     : ' + String(this.Items.length));
                console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
                console.log('-NO MORE DATA - - WILL NOT BE DISPLAYED - - -  ');
                console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');

                this.IntParam.PageActive = this.IntParam.PageActive - 1;
                this.setPageBounds();

                return;
            }
            else {
                this.serverSliceLoad();
                return;
            }
        }

        // send the available data to the projector
        this.clientPageSend();

        console.log('ListExtractor.turnThePage - - - - - - - - - -  ');
        console.log('                          current page       : ' + String(this.IntParam.PageActive));
        console.log('                          this.ItmLstLftIdx  : ' + String(this.ItmLstLftIdx));
        console.log('                          this.ItmLstRgtIdx  : ' + String(this.ItmLstRgtIdx));
        console.log('                          ACTIVE-SLICE       : ' + this.UrlParam.SliceActive);
        console.log('                          CRSR_OFFSET        : ' + this.UrlParam.CrsCmd);
        console.log('                          length Items[]     : ' + String(this.Items.length));
        console.log('- - - - - - - - - - - - - - - - - - - - - - -  ');
    }


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
    * setPageBounds()
    *
    * this functions calculates the left and rigth border-indexes of a page by giving the page-index
    *
    */
    this.setPageBounds = function () {
        console.log('ListExtractor.setPageBounds called');
        this.ItmLstLftIdx = this.IntParam.PageActive * this.IntParam.PageLength;
        this.ItmLstRgtIdx = this.ItmLstLftIdx + this.IntParam.PageLength;
        //this.ItmLstRgtIdx = this.IntParam.PageActive * this.IntParam.PageLength + (this.IntParam.PageLength - 1);
        return;
    }


    /*  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *
     * clientPageSend()
     *
     * this functions creates the package of items that should be displayed and send it to the display()-function of the projector. it dependece on the projector what will be done with the 
     * data. if we have a map the projector will creater markers, if we have a item-list the projector will create a text-list
     *
     * HINT : be sure to give the projector-instance allways the rigth name. this function will just call projector.display( [ItemList] )
     *
     */
    this.clientPageSend = function () {
        console.log('ListExtractor.clientPageSend called');

        dsplyLst = this.Items.slice(this.ItmLstLftIdx, this.ItmLstRgtIdx);
        projector.display(dsplyLst);
        return;
    }


    this.showBookmark = function () {
        // create a link to the current view : asShown
        var pathname = window.location.pathname;
        this.getUrlParams();
        var asShown = pathname + this.prepareUrl();
        $('#extLinkDisplay').prop('href', asShown).prop('target', '_blank').text('Link derzeitige Ansicht');

        // create a link for showing user-items!!!WILL BE COMPLETED IN THE NEAR FUTURE !!!
        var UsrId = $('#CoPlaBottom_lbl_userId').text();
        // alert('UsrId' + UsrId);
        if (UsrId != '') {
            var forUsr = pathname + '?usrId=' + UsrId;
            $('#usrSpecfcItemLnk').prop('href', forUsr).prop('target', '_blank').text('Link zu deinen Beiträgen');
        }
    }


    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    this.loadInitial();         // kickstarter : get server-data initialy from the ajax-source
}






























// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   Debate-Projector Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is responsible for displaying the list of debates as text-table. it shows the items seperated on pages
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//   
//   
//   
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
// 
//
//
//
//


/*
*  DebateProjector
*
*  this class is responsible for displaying the items in the DB as table.view. it allows paging
*
* parameter : displayurl is the url that will be used to show the details of an item
*
* 28.06.2013 bervie initial realese
*
*/
function DebateProjector(dispUrl) {
    //
    // debate-list initialization 
    //

    // icons used for the markers
    //    this.iconswtch = { "§EVT": "./style/marker/waiting.png",
    //        "§ANO": "./style/marker/schreibwaren_web.png",
    //        "§INI": "./style/marker/family.png",
    //        "§BUI": "./style/marker/mine.png",
    //        "§LOC": "./style/marker/home-2.png"
    //    };

    //    this.stndrIcon = "./style/marker/text.png";
    //    this.displayUrl = dispUrl;

    this.iconswtch = {
        "§EVT": nejobaUrl("./style/marker/waiting.png"),
        "§ANO": nejobaUrl("./style/marker/schreibwaren_web.png"),
        "§INI": nejobaUrl("./style/marker/family.png"),
        "§BUI": nejobaUrl("./style/marker/mine.png"),
        "§LOC": nejobaUrl("./style/marker/home-2.png")
    };

    this.stndrIcon = nejobaUrl("./style/marker/text.png");
    this.displayUrl = nejobaUrl(dispUrl);

    this.printTmplt = ['        <div id="Div1">',
                        '            <div class="row span12 well">',
                        '                <div class="span11">',
                        '                    <h5>',
                        '                        <a href="§§URL_LINK_TARGET§§" target="_blank">§§URL_LINK_TEXT§§</a>',
                        '                    </h5>',
                        '                </div>',
                        '                <div class="span4">',
                        '                    <strong>Ersteller: </strong>§§NICKNAME§§<br />',
                        '                    <strong>erstellt am: </strong>§§CREATIONTIME§§<br />',
                        '                </div>',
                        '                <div class="span3">',
                        '                    <strong>vom: </strong>§§DATE_FROM§§<br />',
                        '                    <strong>bis: </strong>§§DATE_TILL§§<br />',
                        '                </div>',
                        '                <div class="span3">',
                        '                    <strong>Ort: </strong>§§LOCATIONNAME§§<br />',
                        '                </div>',
                        '            <br />',
                        '            </div>',
                        '        </div>'].join('\n');



    /*
    * function DebateProjector.defineItemIcon defines which marker-icon will be used for this item. 
    *
    * parameter : dataItem is the item to display
    *
    * 30.06.2013 bervie initial realese
    *
    */
    this.defineDebateIcon = function (dataItm) {
        // console.log('DebateProjector.defineDebateIcon was called');
        if (dataItm.tagZero == undefined) {
            return this.stndrIcon
        }

        if (dataItm.tagZero.length > 0) {
            var typ = dataItm.tagZero.split("_")[0];
            var icon = this.iconswtch[typ];
        }
        else {
            var icon = this.stndrIcon;
        }

        if (typeof icon === "undefined") icon = this.stndrIcon;
        return icon;
    }


    /*
    * display : this function is called from the ListExtractor. It creates the DIVs with the item-infos and writes it to the destination-DIV
    *
    * parameter :  ItemArray 
    *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
    *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
    *
    * 05.06.2013 bervie initial realese
    *
    */
    this.createItemDiv = function (val) {

        var rslt = this.printTmplt;

        // ´put the data inside the template
        rslt = rslt.replace("§§URL_LINK_TARGET§§", this.displayUrl + val._ID);
        rslt = rslt.replace("§§URL_LINK_TEXT§§", val.subject);
        rslt = rslt.replace("§§NICKNAME§§", val.nickname);
        rslt = rslt.replace("§§CREATIONTIME§§", val.creationTime);
        rslt = rslt.replace("§§DATE_FROM§§", val.from);
        rslt = rslt.replace("§§DATE_TILL§§", val.till);
        rslt = rslt.replace("§§LOCATIONNAME§§", val.locationname);

        return rslt;
    }


    /*
    * display : this function is called from the ListExtractor. It creates the DIVs with the item-infos and writes it to the destination-DIV
    *
    * parameter :  ItemArray 
    *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
    *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
    *
    * 05.06.2013 bervie initial realese
    *
    */
    this.display = function (itemArray) {

        // console.log('DebateProjector.display was called ');
        var divContent = '';

        $.each(itemArray, function (i, val) {
            // console.log('Number ' + String(i) + ' ; Subject : ' + val.subject);

            divContent += projector.createItemDiv(val);
        });
        $('#canvasforlist').html(divContent);


        return;
    }

};






























// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//   Map-Projector Class
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
//
//   The Class is responsible for displaying the stuff we have in the ListExtractor on the map. using openlayers with open-street-map
//
// member-attributes :
// ________________________________________________________________________________________________________________________________________________________________________________
//
//   
//   
//   
//
// member-functions :
// ________________________________________________________________________________________________________________________________________________________________________________
//
// addMarker
//
//
//
//

// global definitions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
// # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
AutoSizeAnchoredMinSize = OpenLayers.Class(OpenLayers.Popup.Anchored, { 'autoSize': true, 'minSize': new OpenLayers.Size(400, 200) });
AutoSizeFramedCloudMinSize = OpenLayers.Class(OpenLayers.Popup.FramedCloud, { 'autoSize': true, 'minSize': new OpenLayers.Size(400, 30) });
// # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

/*
*  MapProjector
*
*  this class gets data from the ListExtrctor-Class and displays it 
*  on the map with open-layers stuff. 
*
* parameter : displayurl is the url that will be used to show the details of an item
*
* 28.06.2013 bervie initial realese
*
*/
function MapProjector(dispUrl) {
    //
    // map initialization 
    //
    this.urls = ["http://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
                    "http://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
                    "http://c.tile.openstreetmap.org/${z}/${x}/${y}.png"];


    //this.iconswtch = {
    //    "§EVT": "./style/marker/waiting.png",
    //    "§ANO": "./style/marker/schreibwaren_web.png",
    //    "§INI": "./style/marker/family.png",
    //    "§BUI": "./style/marker/mine.png",
    //    "§LOC": "./style/marker/home-2.png"
    //};

    //this.stndrIcon = "./style/marker/text.png";
    //this.displayUrl = dispUrl;

    this.iconswtch = {
        "§EVT": nejobaUrl("./style/marker/waiting.png"),
        "§ANO": nejobaUrl("./style/marker/schreibwaren_web.png"),
        "§INI": nejobaUrl("./style/marker/family.png"),
        "§BUI": nejobaUrl("./style/marker/mine.png"),
        "§LOC": nejobaUrl("./style/marker/home-2.png")
    };

    this.stndrIcon = nejobaUrl("./style/marker/text.png");
    this.displayUrl = nejobaUrl(dispUrl);

    this.map = new OpenLayers.Map('map');

    this.wms = new OpenLayers.Layer.XYZ("OSM", this.urls, {
        transitionEffect: "resize", buffer: 4, sphericalMercator: true
    });

    this.markers = new OpenLayers.Layer.Markers("pinsOnMap");
    this.map.addLayers([this.wms, this.markers]);
    this.map.updateSize();

    var lonlat = new OpenLayers.LonLat(5.27, 45.82).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
    this.map.setCenter(lonlat);
    this.map.zoomTo(5);


    /**
    * Function: addMarker
    * Add a new marker to the markers layer given the following lonlat, popupClass, and popup contents HTML. Also allow specifying 
    * whether or not to give the popup a close box.
    * 
    * Parameters:
    * ll -              OpenLayers.LonLat       Where to place the marker
    * iconURL           String                  the URL to the marker-icon
    * popupClass -      OpenLayers.Class        Which class of popup to bring up when the marker is clicked.
    * popupContentHTML  String                  What to put in the popup
    * closeBox -        Boolean                 Should popup have a close box?
    * overflow -        Boolean                 Let the popup overflow scrollbars?
    *
    */
    this.addMarker = function (ll, iconURL, popupClass, popupContentHTML, closeBox, overflow) {
        var size = new OpenLayers.Size(32, 37);
        var offset = new OpenLayers.Pixel(-(size.w / 2), -size.h);
        var newIcon = new OpenLayers.Icon(iconURL, size, offset);

        var feature = new OpenLayers.Feature(this.markers, ll);
        feature.closeBox = closeBox;
        feature.popupClass = popupClass;
        feature.data.popupContentHTML = popupContentHTML;
        feature.data.overflow = (overflow) ? "auto" : "hidden";
        feature.data.icon = newIcon;

        var marker = feature.createMarker();

        var markerClick = function (evt) {
            for (var i = 0; i < projector.map.popups.length; i++) { projector.map.popups[i].hide(); }
            if (this.popup == null) {
                this.popup = this.createPopup(this.closeBox);
                projector.map.addPopup(this.popup);
                this.popup.show();
            } else {
                this.popup.toggle();
            }
            currentPopup = this.popup;
            OpenLayers.Event.stop(evt);
        };
        marker.events.register("mousedown", feature, markerClick);
        this.markers.addMarker(marker);
    }

    // *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  
    /*
    * function MapProjector.createHtmlPU creates the link that is shown in the PopUp
    *
    * parameter : dataItem is the item to display
    *
    * HINT: the function uses this.displayUrl to get the URL that will be used as detail-displayer
    *       this attribute is set in the constructor and set by the server. the url depends on if 
    *       user is logged in or not. 
    *       url is set in a hidden server-control
    *
    * 30.06.2013 bervie initial realese
    *
    */
    this.createHtmlPU = function (dataItm) {
        // console.log('MapProjector.createHtmlPU was called');
        var link = this.displayUrl + String(dataItm['_ID']);
        var rslt = '<h5><a href="' + link + '" target="_blank">' + String(dataItm['subject']) + '</a></h5>';

        return rslt;
    }


    /*
    * function MapProjector.defineMrkrIcon defines which marker-icon will be used for this item. 
    *
    * parameter : dataItem is the item to display
    *
    * 30.06.2013 bervie initial realese
    *
    */
    this.defineMrkrIcon = function (dataItm) {
        // console.log('MapProjector.defineMrkrIcon was called');
        if (dataItm.tagZero == undefined) {
            return this.stndrIcon
        }

        if (dataItm.tagZero.length > 0) {
            var typ = dataItm.tagZero.split("_")[0];
            var icon = this.iconswtch[typ];
        }
        else {
            var icon = this.stndrIcon;
        }

        if (typeof icon === "undefined") icon = this.stndrIcon;
        return icon;
    }


    /*
    * display : this function is called from the ListExtractor. It creates and display the markers on the map
    *
    * parameter :  ItemArray 
    *              the array contains all items that should be displayed. the items are chosen from the ListExtractor
    *              this projector-class has no logic for item-selection. it is only a dispaly-idiot
    *
    * 28.06.2013 bervie initial realese
    *
    */
    this.display = function (itemArray) {
        // console.log('MapProjector.display was called ');
        for (var i = 0; i < projector.map.popups.length; i++) { projector.map.popups[i].hide(); }       // 26.07.2013 remove all popups
        this.markers.clearMarkers();                                                                    // remove all markers
        $.each(itemArray, function (i, val) {
            // console.log('MapProjector.display : ' + String(i) + ' , SUBJECT : ' + String(val.subject));

            ll = new OpenLayers.LonLat(val.lon, val.lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
            popupClass = AutoSizeFramedCloudMinSize;
            popupContentHTML = projector.createHtmlPU(val);
            iconURL = projector.defineMrkrIcon(val);
            projector.addMarker(ll, iconURL, popupClass, popupContentHTML, true, true);
        });
        return;
    }
};






























// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
// MatrixManager is the class managing the rtubric-selection-matrixes
// ========================                            ================================================                            ================================================                            ================================================                            ================================================                            ================================================                            ========================
// --------------------------------------------------------------------------------------------------------------------------------------
// --  object to define the data-item in an array
// -- 
// -- 17-06-2013  bervie  initial realese
// --------------------------------------------------------------------------------------------------------------------------------------
function DataItem(Name, TagCode, PosAry) {
    this.ValStr = Name || null,                                        // the string shown in ui : 'Restaurant'
    this.TagCode = TagCode || null,                                        // the string used for tag-definition. will start with the Tag-Prefix
    this.PosArray = new Array(PosAry) || new Array(null, null, null, null, null)      // the array with the position-information in the matrix
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
    try {
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
                for (var i = 0; i < this.Elems.length; i++) { var Name = this.Elems[i].ValStr; }
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
                $('select[id*="lsbx_"]').html('');           // clean-up the previsious data in the selects for taging

                for (var i = 0; i < this.Elems.length; i++) {
                    var Position = this.Elems[i].PosArray.toString().split(',');

                    // if the first item in the array is a null-value the item should be added to the select
                    if (Position[1].length == 0) {
                        var option = '<option value=' + this.Elems[i].TagCode + '>' + this.Elems[i].ValStr + '</option>';
                        console.log('add option to select : ' + option);
                        $("#lsbx_0").append(option);
                    }
                }
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
                console.log('handleSelection : SelectNext = ' + SelectNext);

                // update follwing selects
                if (SelIdNext < 5) {
                    // select the following elements and clean the options in the select
                    $('select[id*="lsbx_"]:gt(' + (SelIdNext - 1) + ')').html('');

                    // get the items belonging to the selcted option
                    for (var i = 0; i < this.Elems.length; i++) {
                        var SubTag = this.Elems[i].TagCode
                        if (SubTag.indexOf(Tag) == 0) {

                            var ItemsInSupTag = SubTag.split('_').length;
                            var ItemInTag = Tag.split('_').length;

                            // copy only the elements belonging to thje next select
                            if (ItemsInSupTag == ItemInTag + 1) {
                                var option = '<option value=' + this.Elems[i].TagCode + '>' + this.Elems[i].ValStr + '</option>';
                                console.log('found item for next select : ' + this.Elems[i].ValStr + ' - ' + SubTag + ' - nxt box ' + SelectNext + ' - ' + option);
                                $('#' + SelectNext).append(option);
                            }
                        }
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

    catch (err) {
        txt = "There was an error in the MtrxMngr\n";
        txt += "Error description: " + err.message + "\n------------------------------------------------------------------------------------------------------------------------------------------------------------\n";
        console.log(txt);
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
    //$("a[id*='hyli_select']").click(function (event) {
    $("img[id*='img_select']").click(function (event) {

        // remove before-selection
        $('#CoPlaBottom_txbx_tagforitem').val('');
        $('#CoPlaBottom_txbx_itemname').val('');

        var typeButtonPressed = String(this.id);
        // alert(typeButtonPressed);
        $('#CoPlaBottom_toggle_div').text(this.typeButtonPressed);     // define the type of item that should be used

        // tagPrefix         the prefix will define the type of item (annonce/initiative/ and stuff...) 
        // matrixSource      the var will contain the string-source used for creating the matrix in the list-boxes
        switch (typeButtonPressed) {
            case "CoPlaBottom_img_selectEvent":
                // matrix.tagPrefix = '§EVT';
                matrix.tagPrefix = 'EVT';
                matrix.matrixSource = $('#CoPlaBottom_date_event_div').text();
                break;

            case "CoPlaBottom_img_selectAnnonceType":
                // matrix.tagPrefix = '§ANO';
                matrix.tagPrefix = 'ANO';
                matrix.matrixSource = $('#CoPlaBottom_annonce_div').text();
                break;

            case "CoPlaBottom_img_selectInitiatives":
                // matrix.tagPrefix = '§INI';
                matrix.tagPrefix = 'INI';
                matrix.matrixSource = $('#CoPlaBottom_initiative_div').text();
                break;

            case "CoPlaBottom_img_selectBusiness":
                // matrix.tagPrefix = '§BUI';
                matrix.tagPrefix = 'BUI';
                matrix.matrixSource = $('#CoPlaBottom_business_div').text();
                break;

            case "CoPlaBottom_img_selectLocation":
                // matrix.tagPrefix = '§LOC';
                matrix.tagPrefix = 'LOC';
                matrix.matrixSource = $('#CoPlaBottom_location_div').text();
                break;

            default:
                matrix.tagPrefix = ''
                console.log("unknown button pressed for itm-type definition!");
        }

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


