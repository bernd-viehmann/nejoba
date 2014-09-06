28.11. Arbeiten an der Loc-Definer-Klasse - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

Description:

In November 2013 a decsision was made. from now on nejoba will always use the same location. regardless where it was defined (in which webform),
the saystem will remeber users last choice and will display data for that location or will store new created articles for that location.

To make this possible the LocDefiner-class is responsible. it is used in every webform tha depends on locations and gets current location or stores 
a newly choosen location in the session-cache.

To make it easy the class stores the current used location in the session-cache. there is a dict in the userData-class which already have configuration 
for the session in the session-cache: 
	self.usrData             = page.Session['njbUsrDt'] to access to the session-cache with the user-datacurrent user-configuration
	self.usrData.userDict    = the dictionary with the available config for the current user-session

the LocDefiner-class will use 2 strings in the user-dict to alwas remeber what location we are currently working on :

	- self.usrData.userDict['LCDFNR_MONGOID'] : databse-ID (or a flag showing special state)
	- self.usrData.userDict['LCDFNR_SLCTSTR'] : select-string (stores users input)


	1. LCDFNR_MONGOID
	this string can have three different values 
		'50c2344b773e6f12e007556c' is the mongo-ID of the location nejoba is currently working on.

		'not available' is used if no loc-db-id is available. this is the case if all data (no country, selector = *) or all data 
		                of a country ('DE' for germany) is selected.

		'not found' is used if user tried to define a location (gave a name or postcode) but for the given input there was no entry in the database


	2. LCDFNR_SLCTSTR
	this string can have following values:
		'*|' this means all data should be selected. will not be filteres by location. corresponding LCDFNR_MONGOID-value : 'not available'

		'DE|' means a whole country should be selected. all items for germany for example. corresponding LCDFNR_MONGOID-value : 'not available'

		'DE|41836' user has selected a location by its postcode.example of corresponding LCDFNR_MONGOID-value : '50c2344b773e6f12e007556c'

		'DE|hückelhoven' user has selecteda location by the city-name. example of corresponding LCDFNR_MONGOID-value : '50c2344b773e6f12e007556c'

	the difference between 'DE|hückelhoven' and 'DE|41836':

	it makes a difference if user choose the postcode or the city-name.ifpostcode was choosen ('DE|41836') this postcode-location end the 
	neighbours in the area  will be selected.
	if the user chooses a city-name 'DE|hückelhoven' nejoba will get the first location with that name in the db and adds the neighbour-postcodeareas. 
	additionaly all locations with the same name in the same country will be added also. this is very usefull for big-citieslike Hamburg wherenot 
	all post-code-areas would be choosen if only the items inside the search-area would be added.










