# ***********************************************************************************************************************************************
# GeoCalc : class is used to make all needed geogrphical calculation stuff
#
# geographic stuff based based on http://www.geonames.org/ 
#
# 13.12.2011  - bervie -     initial realese
# 
# !!! ToDO  !!!  ToDO   ToDO   ToDO   ToDO   ToDO   ToDO   ToDO   ToDO   ToDO  
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# replace this class by LocDefiner
# !!! ToDO  !!!  ToDO   ToDO   ToDO   ToDO   ToDO   ToDO   ToDO   ToDO   ToDO  
#
# ***********************************************************************************************************************************************
import math  
import traceback

class GeoCalc:
    '''
    GeoCalc Class: common functions to work with geographical information
    calculate distances, generate points and stuff like that
    '''
    # ***********************************************************************************************************************************************
    # constructor : the class will use the python math library and uses a spherical point of view to our planet
    #
    # 13.12.2011  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, page, lat, lon, rad = 6371.0 ):
        try:
            # rad is the radius of our homeplanet. so if you do not have any jobs to promote on mars you must not change this value
            self.Page = page
            self.log = page.Application['njb_Log']        # get the applicationwide logging mechanism
            # self.log.w2lgDvlp('GeoCalc - constructor was called !')
            self.lat = lat
            self.lon = lon
            self.radius = rad

        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # converting functions for RAD and degres
    #
    # 19.12.2011  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def toRad( self, number ): return float(number) * math.pi / 180.0
    def toDeg( self, number ): return float(number) * 180.0 / math.pi 
    

    # ***********************************************************************************************************************************************
    #
    # function distanceTo ( self, point ):
    #
    # Returns the distance from this point to the supplied point, in km 
    # (using Haversine formula)
    # 
    #  from: Haversine formula - R. W. Sinnott, "Virtues of the Haversine",
    #        Sky and Telescope, vol 68, no 2, 1984
    # 
    #  @param   {LatLon} point: Latitude/longitude of destination point
    #  @returns {Number} Distance in km between this point and destination point
    # 
    # 13.12.2011  - bervie -     initial realese
    # ***********************************************************************************************************************************************
    def distanceTo( self, point ):
        try:
            # self.log.w2lgDvlp('GeoCalc.distanceTo was called ')
            R = self.radius
            lat1 = math.radians(self.lat) 
            lon1 = math.radians(self.lon)
            lat2 = math.radians(point.lat)
            lon2 = math.radians(point.lon)
            dLat = lat2 - lat1
            dLon = lon2 - lon1

            a = math.sin(dLat/2.0) * math.sin(dLat/2.0) + math.cos(lat1) * math.cos(lat2) * math.sin(dLon/2.0) * math.sin(dLon/2.0)
            c = 2.0 * math.atan2( math.sqrt(a), math.sqrt(1.0-a))
            d = R * c

            return d
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())






    # ***********************************************************************************************************************************************
    #
    # destinationPoint(self, bearing , distnc):
    #
    # Returns the destination point from this point having travelled the given distance (in km) on the 
    # given initial bearing (bearing may vary before destination is reached)
    #
    #   see http://williams.best.vwh.net/avform.htm#LL
    #
    # @param   {Number} brng: Initial bearing in degrees
    # @param   {Number} dist: Distance in km
    # @returns {LatLon} Destination point
    #
    # 19.12.2011  -bervie-   initial realese
    #
    # ***********************************************************************************************************************************************
    def destinationPoint(self, bearing , distnc):
        try:
            dist = float(distnc)/self.radius  # convert dist to angular distance in radians
            brng = math.radians( bearing )

            lat1 = self.toRad( self.lat )
            lon1 = self.toRad( self.lon )

            lat2 = math.asin( math.sin(lat1) * math.cos(dist) + math.cos(lat1) * math.sin(dist) * math.cos(brng) )
            lon2 = lon1 + math.atan2( math.sin(brng) * math.sin(dist) * math.cos(lat1), math.cos(dist) - math.sin(lat1) * math.sin(lat2))
            lon2 = (lon2 + 3 * math.pi) % ( 2 * math.pi) - math.pi   # normalize to -180/+180 

            result = GeoCalc( self.Page, self.toDeg(lat2), self.toDeg(lon2) )
            return result
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    #
    # getAreaCorners(self, middle , length):
    #
    # The function returns the upper-left and lower-rigth corner of the area. For calculating this you have to tell the middle and the length 
    # of a tangent in the rectangle.
    #
    # param:
    # middle (GeoCalc) :        the middle of the rectangle
    # length           :        the half-length of the box-size in kilometer
    #
    # returns:
    # GeoCalc[]        :        an array with the top-left[0] and rigth-down[1]] points of the rectangle
    #
    #   see http://williams.best.vwh.net/avform.htm#LL
    #
    # 20.12.2011  -bervie-   initial realese
    #
    # ***********************************************************************************************************************************************
    def getAreaCorners(self, length):
        try:
            # self.log.w2lgDvlp('GeoCalc.getAreaCorners was called ')

            northwest = self.destinationPoint( 315.0 ,length )
            southeast = self.destinationPoint( 135.0 ,length )

            rslt = str(northwest.lat) + ';' + str(northwest.lon) + ';' + str(southeast.lat)  + ';' + str(southeast.lon)

            return rslt
        except Exception,e:
            self.log.w2lgError(traceback.format_exc())

