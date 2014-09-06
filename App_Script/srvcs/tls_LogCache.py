# ***********************************************************************************************************************************************
# ch_LogCache.py : class for temporary store the logging of the system (minimize disc I/O)
#                  this class stores the messages that should be logged in an array.
#                  if the array-length exeeds the defined number of maximum messages that should be cached 
#                  the class copies the stuff to the log-file
#                  the definition comes from the web.config file : WebConfigurationManager.AppSettings['logCacheCount']
#                  it is stored in self.logCacheCount
#                  with the function writeNow() the messages are all written to the log-file
#
#                  an exception are 'error'-Messages. The are written directly to the error-log-file
#
# 18.11.2011  - bervie -     initial realese
#   
# ***********************************************************************************************************************************************
from System.Web.Configuration import *
from time import *
import codecs
import traceback                           # for better exception understanding

class LogCache:
    '''
    LogCache Class: this class stores logging into the mem-cache instead of writing every peace to the disc when it exists
    except for the errors which are writte directly to disc
    '''

    # ***********************************************************************************************************************************************
    # constructor : creates a new instance in the application-cache if needed
    #
    # 19.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def __init__(self, appl):
        '''
        constructor gets the instance in application cache
        '''
        try:
            self.logFilePath = WebConfigurationManager.AppSettings['logFilePath']
            self.logFileName = WebConfigurationManager.AppSettings['logFileName']
            self.errorFilePath = WebConfigurationManager.AppSettings['errorFilePath']
            self.errorFileName = WebConfigurationManager.AppSettings['errorFileName']
            self.logLevelDef = WebConfigurationManager.AppSettings['logLevelDef']
            self.logCacheCount = int(WebConfigurationManager.AppSettings['logCacheCount'])
            self.logLevel = self.logLevelDef.index(   WebConfigurationManager.AppSettings['logLevel'] )     # the index of the log-definition defiens what must been logged. so we can decide in the web.config what should be logged and what not
            self.tmpLg = []         # the list of messages

            appl['njb_Log'] = self  # add instance to the application-cache
            self.w2lgMsg('Application started : new LogCache was created')
        except Exception,e:
            self.w2lgError(traceback.format_exc())

    def __call__(self):
        self.__init__()


    # ***********************************************************************************************************************************************
    # receive text-line for logging
    #
    # 19.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def recLine( self, line, level):
        '''function receives a new line for the message-block and writes it to the file if needed'''
        try:
            dayTag = strftime('%Y%m%d', localtime())
            timeTag = strftime('%H:%M:%S', localtime())

            str = unicode('{0:9s}| {1:5s} -   {2:s}'.format( timeTag, level[:4], line ) + '\n')

            # if it is an error it must be directly written to the error-log
            if (level == 'error' ):
                fInf = self.errorFilePath + '\\' + dayTag + self.errorFileName
                # file2Log = open( fInf, 'a' )
                file2Log = codecs.open( fInf, encoding='utf-8', mode='a')
                file2Log.write( str )
                file2Log.close()

            # messages can be written to the cache before saved in the file    
            else:
                # only log if the message should be written depending on curretn log-level
                current = self.logLevelDef.index( level ) 
                if current > self.logLevel:
                    return

                # if log should be done we collect a couple of lines before logging will be done%
                self.tmpLg.append(str)

                if( len(self.tmpLg) >= self.logCacheCount):
                
                    fInf = self.logFilePath + '\\' + dayTag + self.logFileName
                    # file2Log = open( fInf, 'a' )
                    file2Log = codecs.open(fInf,'a','utf-8')   # unicode support

                    for msg in self.tmpLg:
                        file2Log.write( msg )

                    file2Log.close()
                    self.tmpLg = None
                    self.tmpLg = []
        except Exception,e:
            self.w2lgError(traceback.format_exc())

    # ***********************************************************************************************************************************************
    # writeNow : write all messages to the log-file
    # function makers a flush-write of all data in the array to the disc. this function is called from the rmote-timer to store all th shit
    #
    # 26.11.2011    berndv  initial realese
    # ***********************************************************************************************************************************************
    def writeNow(self):
        '''this function writes all itmes from the message-cache to the file imediantly'''
        try:
            numOfMessages = len(self.tmpLg)
            dayTag = strftime('%Y%m%d', localtime())
            timeTag = strftime('%H:%M:%S', localtime())
        
            str = unicode('Flush-write to the message-file done. Number of messages in the cache :' + numOfMessages + ' at ' + timeTag)

            self.tmpLg.append(str)

            fInf = self.logFilePath + '\\' + dayTag + self.logFileName
            # file2Log = open( fInf, 'a' )
            file2Log = codecs.open( fInf, encoding='utf-8', mode='a')   # unicode support

            for msg in self.tmpLg:
                file2Log.write( msg )

            file2Log.close()
            self.tmpLg = None
            self.tmpLg = []
        except Exception,e:
            self.w2lgError(traceback.format_exc())


    # ***********************************************************************************************************************************************
    # write-to-log : 
    # different messages to error- or messagefile cached or directly in dependance of urgency. erroros are writte imediatly. messages
    # messages are written cached after a number of items are stored in an array. number can be configured in the web.config file : key="logCacheCount"
    # ***********************************************************************************************************************************************
    def w2lgError(self, msg ): self.recLine( unicode(msg) , 'error')
    def w2lgMsg(self, msg )  : self.recLine( unicode(msg) , 'message')
    def w2lgDbg(self, msg )  : self.recLine( unicode(msg) , 'debug')
    def w2lgDvlp(self, msg ) : self.recLine( unicode(msg) , 'develop')



