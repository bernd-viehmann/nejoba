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
        $('#txbx_hashtag').val('');
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
        var tgs = $('#txbx_hashtag').val();
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
