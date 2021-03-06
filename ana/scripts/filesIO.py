"""
============================
script: filesIO.py
============================
	date: 20170615 by Jianrong Deng
	purpose:
		handle input / output files
		various data I/O functions
	Input: input dir, date, time 
"""

import const
import pickle
import os

#==========================
def getDir (path=const.test_path_out, date=const.test_date, datatype=const.test_datatype): 
    """
    purpose: name scheme for net data (= raw - overscan - bias) file
    """
    dir =  path +'/' + date + '/' + datatype
    return dir
#==========================

#==========================
def getFilename (path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-sub_overscan-sub_bias', postfix = '.fit'): 
    """
    purpose: name scheme for net data (= raw - overscan - bias) file
    """
    filename =  path +'/' + date +'/' + datatype +'/' + det +'-' + time +'-' + tag + postfix
    return filename

#==========================
def setOutFilename(rawfile, d_tag='stat'):
    """
    purpose: set output filename using environment variables
    input: rawfile: filename of raw data
    output: output filename
    """

    # info from input filenames 
    d_path_in = os.environ['env_rawdata_onlypath'] # get environment variable 
    d_date = get_date(d_path_in) # get date
    d_type=get_datatype(d_path_in)
    d_det = get_det(rawfile)
    d_time = get_time(rawfile)

    # setup output file directory and names
    d_path_out = os.environ['env_path_out'] # get environment variable 
    os.system('mkdir -p {}'.format(getDir(path=d_path_out, date=d_date, datatype=d_type))) # create output directory if not already exists
    file_out = getFilename(path=d_path_out, date=d_date,det=d_det,time=d_time, tag = d_tag, postfix='.dat') 
    return file_out
#==========================

#==========================
def setFilename(infile, in_tag='stat.dat', out_tag='clusters.dat'):
    """
    purpose: set output filename using environment variables
    input: infile: the input filename
           in_tag: tag of the input file
           out_tag: tag of the output file
    output: output filename
    """

    in_len = len(infile)
    file_out = infile[0:in_len-len(in_tag)]
    file_out = file_out + out_tag 
    return file_out

#==========================


def getMaskFilename(path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-3sigma_mask', postfix = '.fit'): 
    """
    purpose: name scheme for 3sigma-mask file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename

#==========================
def getClusterFilename(path=const.test_path_out, date=const.test_date, datatype=const.test_datatype, det=const.test_det, time=const.test_time[0], tag = '-cluster', postfix = '.dat'): 
    """
    purpose: name scheme for 3sigma-mask file
    """
    filename =  path + date + datatype + det + time + tag + postfix
    return filename
#============================


#============================
def dumpPixelLists(file_out, pixelLists, DEBUG = const.DEBUG):
#============================
    """
    purpose: save pixel Lists to output file
    input :  filename and pixellist
    """
    # save list to output file
    try:
        with open(file_out, "wb") as data:
            pickle.dump(pixelLists, data)
    except IOError as err:
        print('File error: ', + str(err))
    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))

    if DEBUG: printPixelLists(pixelLists)

    return            
#============================

#============================
def loadPixelLists(file_out, DEBUG = const.DEBUG):
#============================
    """
    purpose: load pixel List from file
    input :  filename 
    output : pixellists

    """
    # save list to output file
    try:
        with open(file_out, "rb") as data:
            pixelLists  = pickle.load(data)
    except IOError as err:
        print('File error: ', + str(err))
    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))
    
    if DEBUG: printPixelLists(pixelLists)

    return pixelLists 
#============================

#============================
def printPixelLists(pixelLists, DEBUG = const.DEBUG_L2):
#============================
    """
    purpose: print candidate  pixel List 
    input :  pixelLists

    """
    print('number of images: ', len(pixelLists))
    for im in pixelLists: # loop through five images 
        print('number of candiate pixels (clusters) in the image: ', len(im))
        if DEBUG:
            for ip in im:
                print (ip[0], ip[1], int(ip[2]))
    return           
#============================


#============================
def dumpStat(file_stat, stat, DEBUG = const.DEBUG_L2):
#============================
    """
    purpose: save stat info (mean and sstd ) to output file
    input :  file_stat and data stat(mean and sstd)
    """
    try:
        with open(file_stat, "wb") as data:
            pickle.dump(stat, data)
    except IOError as err:
        print('File error: ', + str(err))

    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))

    if DEBUG:
             printStats (stat)
        
    return            
#============================


#============================
def loadStat(file_stat, DEBUG = const.DEBUG):
#============================
    """
    purpose: save stat info (mean and sstd ) to output file
    input :  file_stat and data stat(mean and sstd)
    """
    try:
        with open(file_stat, "rb") as data:
            stat = pickle.load(data)
    except IOError as err:
        print('File error: ', + str(err))

    except pickle.pickleError as perr:
        print('picklingerror:' + str(perr))
        
    if DEBUG:
             printStats (stat)

    return stat           
#============================


#============================
def printStats(stats):
#============================
    """
    purpose: print stat info (mean and sstd ) 
    input :  data stat(mean and sstd)
    """
    print ('image stat where [0-4] is real data, [5] is bias medium')
    for ist in range(len(stats)):
         print ('image :', ist, 'mean =',  stats[ist][0], ', sstd =', stats[ist][1])
    return 
#============================

#============================
def get_onlyrawfilenames(DEBUG=const.DEBUG_L2):	
    """
    purpose: get rawfilenames from environment variables
             
    """
    if DEBUG: # in debug mode, check if file exists
        os.system("${env_rawdata_onlypath:?}") # ${variable:?} check if the variable is set
        os.system("ls -l ${env_rawdata_onlypath:?}/${env_rawdata_onlyfilenames_0:?}")
        os.system("ls -l ${env_rawdata_onlypath:?}/${env_rawdata_onlyfilenames_1:?}")

    rawfiles=[]
    rawfiles.append( os.environ['env_rawdata_onlyfilenames_0'])
    rawfiles.append( os.environ['env_rawdata_onlyfilenames_1'])
    rawfiles.append( os.environ['env_rawdata_onlyfilenames_2'])
    rawfiles.append( os.environ['env_rawdata_onlyfilenames_3'])
    rawfiles.append( os.environ['env_rawdata_onlyfilenames_4'])

    return rawfiles
#============================

#============================
def get_rawfilenames(DEBUG=const.DEBUG_L2):	
    """
    purpose: get rawfilenames (with pathname) from environment variables
    output: rawfilenames with pathname
             
    """
    path= os.environ['env_rawdata_onlypath']
    rawfiles= get_onlyrawfilenames()
    for ir in range(len(rawfiles)):
        rawfiles[ir]=path + '/' + rawfiles[ir]
    return rawfiles
#============================


#============================
def get_det(filename):	
    """
    purpose: strip the time stamps from filenames
    """
    temp = filename.strip().split('-')
    det=temp[0]+'-' + temp[1]
    return det
#============================

#============================
def get_times(filenames):	
    """
    purpose: strip the time stamps from filenames
    """
    times = []
    for ifile in filenames:
        times.append(get_time(ifile))
    return times 
#============================

#============================
def get_time(filename):	
    """
    purpose: strip the time stamp from the filename
    """
    temp = filename.strip().split('-')
    return temp[2]
#============================

#============================
def get_date(pathname, DEBUG=const.DEBUG_L2):	
    """
    purpose: strip the date stamps from pathname
    """
    temp = pathname.strip().split('/')
    date = temp[3]
    if DEBUG: 
        print('pathname = ', pathname, '\t date =', date)
    return date
#============================

#============================
def get_datatype(pathname):	
    """
    purpose: strip the data type info from pathname
    """
    temp = pathname.strip().split('/')
    return temp[4]
#============================



#============================
class filename_rawdata:
    """
    purpose: filename class for rawdata 

    """
#============================
    def __init__(self, a_det, a_dType, a_date, a_times=[]):
        """
        purpose: initialization
        """
        self.det = a_det
        self.dType = a_dType
        self.date = a_date
        self.times = a_times
#============================

