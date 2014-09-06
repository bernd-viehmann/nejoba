#  Copyright (c) Microsoft Corporation. 
#
#  This source code is subject to terms and conditions of the Apache License, Version 2.0. A 
#  copy of the license can be found in the License.html file at the root of this distribution. If 
#  you cannot locate the  Apache License, Version 2.0, please send an email to 
#  dlr@microsoft.com. By using this source code in any fashion, you are agreeing to be bound 
#  by the terms of the Apache License, Version 2.0.
#
#  You must not remove this notice, or any other, from this software.

#from System.Web import HttpContext

def Application_Start():
    ' Code that runs on application startup'
    import sys
    sys.path.append(r'C:\ironpython27\Lib')

def Application_End():
    ' Code that runs on application shutdown'
    pass

def Application_Error(app, e): 
    ' Code that runs when an unhandled error occurs'
    pass

def Application_BeginRequest(app, e):
    ' Code that runs at the beginning of each request. used to handle short-url-requests.'

    # url_remapper
    #context = HttpContext.Current
    #logger = context.Application['njbLOG']
    #if logger is not None : logger.w2lgDvlp('Leberkaes mit Kn?ddeln !')



def Application_EndRequest(app, e):
    ' Code that runs at the end of each request'
    pass 
