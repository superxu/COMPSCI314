'''
Created on 2015. 7. 13.

@author: Se-young Yu
@added and modified by Shupeng Xu. UPI: sxu487   Student ID: 8260026
'''

import datetime
import re
import math
from dateutil.relativedelta import relativedelta

class Parser:
    
    #Define variables in Java way
    def __init__(self):
        self.numberOfDays = 0 # Count number of Days passed

        self.startDate = datetime.date.today()
        self.endDate = datetime.date.today()    
        self.days = 0
        self.totalBytes = 0
        self.totalsuccessBytes = 0
        self.localvisits = 0
        self.remotevisits = 0
        self.localdata = 0
        self.remotedata = 0
        self.totalFiles = 0
        self.onceReqBytesCount = 0

        self.fileTypeDict = dict() # Contains file extension - file
                                                    # type information       
        
        self.responseCodeDict = dict()
        self.responseTypeDict =  dict()
        self.fileTypeCountDict = dict()
        self.fileTypeSizeDict = dict()
        self.objectCountDict = dict()

        self.initializeResponseCode()
        self.initializeResponseType()
        self.initializefileTypeCount()
        self.initializeFileType()
        self.initializefileTypeSize()
        self.initializeobjectCount()

    def initializeobjectCount(self):
        self.objectCountDict[""] = 0


    def initializefileTypeSize(self):

        self.fileTypeSizeDict["HTML"] = 0 
        self.fileTypeSizeDict["Images"] = 0 
        self.fileTypeSizeDict["Sound"] = 0 
        self.fileTypeSizeDict["Video"] = 0 
        self.fileTypeSizeDict["Formatted"] = 0 
        self.fileTypeSizeDict["Dynamic"] = 0 
        self.fileTypeSizeDict["Others"] = 0 


    def initializefileTypeCount(self):

        self.fileTypeCountDict["HTML"] = 0 
        self.fileTypeCountDict["Images"] = 0 
        self.fileTypeCountDict["Sound"] = 0 
        self.fileTypeCountDict["Video"] = 0 
        self.fileTypeCountDict["Formatted"] = 0 
        self.fileTypeCountDict["Dynamic"] = 0 
        self.fileTypeCountDict["Others"] = 0 


    def initializeResponseType(self):
        self.responseTypeDict[200] = 0 # successful
        self.responseTypeDict[304] = 0 # not modified
        self.responseTypeDict[302] = 0 # found
        # 4xx and 5xx unsuccessful, use -1
        self.responseTypeDict[-1] = 0

    def initializeResponseCode(self):
        self.responseCodeDict["Successful"] = 0
        self.responseCodeDict["Not Modified"] = 0
        self.responseCodeDict["Found"] = 0
        self.responseCodeDict["Unsuccessful"] = 0

    def initializeFileType(self) :
        # Define file types for each file       
        
        self.fileTypeDict["html"] = "HTML"
        self.fileTypeDict["htm"] = "HTML"
        self.fileTypeDict["shtml"] = "HTML"
        self.fileTypeDict["map"] = "HTML"        

        self.fileTypeDict["gif"] = "Images"
        self.fileTypeDict["jpeg"] = "Images"
        self.fileTypeDict["jpg"] = "Images"
        self.fileTypeDict["xbm"] = "Images"
        self.fileTypeDict["bmp"] = "Images"
        self.fileTypeDict["rgb"] = "Images"
        self.fileTypeDict["xpm"] = "Images"        

        self.fileTypeDict["au"] = "Sound"
        self.fileTypeDict["snd"] = "Sound"
        self.fileTypeDict["wav"] = "Sound"
        self.fileTypeDict["mid"] = "Sound"
        self.fileTypeDict["midi"] = "Sound"
        self.fileTypeDict["lha"] = "Sound"
        self.fileTypeDict["aif"] = "Sound"
        self.fileTypeDict["aiff"] = "Sound"

        self.fileTypeDict["mov"] = "Video"
        self.fileTypeDict["movie"] = "Video"
        self.fileTypeDict["avi"] = "Video"
        self.fileTypeDict["qt"] = "Video"
        self.fileTypeDict["mpeg"] = "Video"
        self.fileTypeDict["mpg"] = "Video"

        self.fileTypeDict["ps"] = "Formatted"
        self.fileTypeDict["eps"] = "Formatted"
        self.fileTypeDict["doc"] = "Formatted"
        self.fileTypeDict["dvi"] = "Formatted"
        self.fileTypeDict["txt"] = "Formatted"

        self.fileTypeDict["cgi"] = "Dynamic"
        self.fileTypeDict["pl"] = "Dynamic"
        self.fileTypeDict["cgi-bin"] = "Dynamic"    
    
    #Q1
    def calculate_averagereq(self, logFile):

        data = logFile.readlines()
        logFile.seek(0)#seek to first line in file
        firstline =  (logFile.readline())
        lastline =  (data[len(data)-1]) #-1 represents last item on list data
        contents = logFile.read()
        request_count = contents.count("GET")

        firstline_elements = firstline.split()
        lastline_elements = lastline.split()

        start_date = firstline_elements[3].replace('[', '')
        end_date = lastline_elements[3].replace('[', '')

        starttime = datetime.datetime.strptime(start_date, '%d/%b/%Y:%H:%M:%S')
        endtime = datetime.datetime.strptime(end_date, '%d/%b/%Y:%H:%M:%S')

        self.days = (endtime - starttime).days
        #print("difference = %s" % days)

        average_req = request_count / self.days
        print("Q1: requests per day = %.2f" % average_req)

    # Q2 
    def total_bytes(self, totalBytes):
        total_bytes = totalBytes/1024/1024
        print("Q2: total bytes = %d MB" %  total_bytes)     

    # Q3 
    def average_bytes(self, totalBytes):
        average_bytes = (totalBytes/1024/1024)/self.days
        print("Q3: average bytes per day = %d MB" % average_bytes)

    # Q4 
    def count_responsecode(self):
        totalcounts = 0
        print("Q4:")
        print("Response Type  :  Percentage")
        for key in self.responseCodeDict:
            totalcounts += self.responseCodeDict[key]

        for key in self.responseCodeDict:
            print("{0},  {1}".format(key , self.responseCodeDict[key]/totalcounts))

    # Q5
    def local_remote_visits(self):
        print("Q5: local visit times = %s, remote visit times = %s " % (self.localvisits, self.remotevisits))
    
    # Q6
    def local_remote_data(self):
        print("local data in bytes = %s, remote data in bytes = %s" % (self.localdata, self.remotedata))
        print("Q6: local data  = %.2f,  remote data = %.2f" % (self.localdata/self.totalBytes, self.remotedata/self.totalBytes));

    # Q7
    def filetype_request_rate(self):
        totalrequests = (self.localvisits + self.remotevisits)
        print("total successful requests = %s" % totalrequests)
        print("Q7: FileType : Percentage")
        for key in self.fileTypeCountDict:
            print("{0} ,  {1}".format(key, self.fileTypeCountDict[key]/totalrequests))

    # Q8 
    def filetype_size_rate(self):
        print("Q8: total successful bytes = %s" % self.totalsuccessBytes)
        for key in self.fileTypeSizeDict:
            print("{0} ,  {1}".format(key, self.fileTypeSizeDict[key]/self.totalsuccessBytes))

    # Q9
    def average_filesize(self):
    # total file size of each file type / file count of this file type
        print("Q9: ")
        for key in self.fileTypeCountDict:
            print(" %s  %s" % (key, math.ceil(self.fileTypeSizeDict[key]/self.fileTypeCountDict[key])))

    # Q10
    def objectReqOnce(self):
        print("Q10: ")
        once_count = 0
        total_count = self.localvisits + self.remotevisits

        for key in self.objectCountDict:
            if self.objectCountDict[key] == 1:
                once_count += 1

        print("once_count = %d total_count = %d"  % (once_count, total_count))
        print("1. percentage = %f" % (once_count/total_count))
        print("2. percentage = %f" % (self.onceReqBytesCount/self.totalsuccessBytes))


    # Read Each line from the log and process output    
    def parse(self, logFile):
        index = 0
 
        for line in logFile:
               
            # Skip to the next line if this line has an empty string
            if line is '': continue
            
            elements = line.split()
            sourceAddress = elements[0]
            timeStr = elements[3].replace('[', '')
            requestMethod = elements[5].replace('"','')
            requestFileName = elements[6].replace('"','')
            
            # Skip to the next line if this line contains not equal to 9 - 11 elements
            
            if not(len(elements) == 10 or len(elements) == 9 or len(elements) == 11):
                continue
                
            #If there is more than 1 element in user information, correct the index of
            #other elements
            timeStrIndex = 0
            
            for idx, val in enumerate(elements):
                timeStrIndex = idx-1
                if '-0600]'  == val : break 
            
            timeStr = elements[timeStrIndex].replace('[', '')
            requestMethod = elements[timeStrIndex+2].replace('"','')
            requestFileName = elements[timeStrIndex+3].replace('"','')
            self.endDate = datetime.datetime.strptime(timeStr, "%d/%b/%Y:%H:%M:%S")
              
            #If this line is the first or the last line, store date
            # information
            if index is 0: self.startDate = self.endDate
            
            responseCode = elements[len(elements) - 2]
            replySizeInBytes = elements[len(elements) - 1]
            
            #put HTTPversion as empty string if not exist
            if len(elements) <= 10: HTTPversion = elements[7]                
            else: HTTPversion = elements[6]
            
            if not ('HTTP' in HTTPversion or '1.0' in HTTPversion):
                HTTPversion = ""            
            
            ################## From Here ##################
            # Implement your parser here to generate statistics output      
        
            #print('{0} , {1} , {2}, {3} , {4} , {5} , {6}'.format(sourceAddress,timeStr,requestMethod,requestFileName,HTTPversion, responseCode, replySizeInBytes),end="")
           
            if replySizeInBytes.isdigit():
                self.totalBytes +=  int(replySizeInBytes)
                if responseCode == "200": 
                    self.totalsuccessBytes += int(replySizeInBytes)

            if not replySizeInBytes.isdigit(): continue;
            
            fileType = self.getFileType(requestFileName)
            if fileType in self.fileTypeCountDict:
                if responseCode == "200":
                    filecount = self.fileTypeCountDict[fileType]
                    filecount += 1
                    self.fileTypeCountDict[fileType] = filecount

                    filesize = self.fileTypeSizeDict[fileType] 
                    filesize += int(replySizeInBytes)
                    self.fileTypeSizeDict[fileType] = filesize

                    self.totalFiles += 1


            #print(' , {0}'.format(fileType))


            if responseCode.isdigit():
                rescode = int(responseCode)
                if rescode in self.responseTypeDict:
                    count = self.responseTypeDict[rescode]
                    count += 1
                    self.responseTypeDict[rescode] = count  
                else:
                    if responseCode.startswith('4') or responseCode.startswith('5'):
                        count = self.responseTypeDict[-1]
                        count += 1
                        self.responseTypeDict[-1] = count 
                  
            '''   
            # does not work, I think it's beacuse sourceAddress is string not IP(digits)      
            match_result = re.match(r"128\.233\.\d{1,3}$\.\d{1,3}$", sourceAddress)
            #print("match_result = %s IP = %s", (match_result, sourceAddress))
            if match_result:
                print("IP = %s", sourceAddress)
            '''

            if responseCode == "200":
                if ("usask.ca" in sourceAddress) or ("128.233." in sourceAddress):
                    # only count successful requests
                        self.localvisits += 1
                        if replySizeInBytes.isdigit():
                            self.localdata +=  int(replySizeInBytes)
                else:
                        self.remotevisits += 1
                        if replySizeInBytes.isdigit():
                            self.remotedata +=  int(replySizeInBytes)

                if requestFileName in self.objectCountDict:
                    count = self.objectCountDict[requestFileName]
                    count += 1
                    self.objectCountDict[requestFileName] = count
                else:
                    self.objectCountDict[requestFileName] = 1
                    self.onceReqBytesCount += int(replySizeInBytes)


        self.responseCodeDict["Successful"] = self.responseTypeDict[200]
        self.responseCodeDict["Not Modified"] = self.responseTypeDict[304]
        self.responseCodeDict["Found"] = self.responseTypeDict[302]
        self.responseCodeDict["Unsuccessful"] = self.responseTypeDict[-1]

        # Q2
        self.total_bytes(self.totalBytes)
        print("")
        # Q3
        self.average_bytes(self.totalBytes)
        print("")
        # Q4
        self.count_responsecode()
        print("")
        # Q5
        self.local_remote_visits()
        print("")
        # Q6
        self.local_remote_data()
        print("")
        # Q7
        self.filetype_request_rate()
        print("")
        # Q8
        self.filetype_size_rate()
        print("")
        # Q9
        self.average_filesize()
        print("")
        # Q10
        self.objectReqOnce()
        print("")
        #########################################
        
    
    
    def getFileType(self, URI):
        
        if URI.endswith('/') or URI.endswith('.') or URI.endswith('..'): return 'HTML'
        
        filename = URI.split('/')[-1]
        
        if '?' in filename: return 'Dynamic'
        
        extension = filename.split('.')[-1].lower()
        
        if extension in self.fileTypeDict:
            return self.fileTypeDict[extension]
        else : return 'Others'
        
    def checkResCode(self,code):
        if code == '200' : return 'Successful'
        if code == '302' : return 'Found'
        if code == '304' : return 'Not Modified'   
        return None
        
if __name__ == '__main__':
    logfile = open('UofS_access_log','r', errors='ignore')
    logParser = Parser()
    logParser.calculate_averagereq(logfile)
    print("")
    logfile_next = open('UofS_access_log','r', errors='ignore')
    logParser.parse(logfile_next)
    pass