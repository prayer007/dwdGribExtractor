import requests
from collections import Iterable
import multiprocessing
from datetime import datetime, timezone, timedelta
from bz2 import decompress
import xarray as xr
import pandas as pd
import os
import glob
from pathlib import Path
import numpy as np


class ICON_D2:

    '''Class to retrieve ICON D2 data from opendata.dwd.de.
    The data is extracted from a nwp gribfile
    
    Parameters
    ----------
    locations : dict
        lat, lon in geographic coordinates as a dict for each location
        
            .. code-block::
                
                variables = ["aswdir_s", "aswdifd_s", "t_2m"]
                
    forecastHours : int
        The forecast hours for which the data is collected
    tmpFp : string
        The filepath to a folder where temporary files will be stored. This 
        is needed to extract data from grib2 files because with the used 
        libraries (eccodes, cfgrib) it is not possible to store the downloaded 
        grib files in memory (see https://github.com/ecmwf/cfgrib/issues/99 or 
                              https://github.com/ecmwf/eccodes-python/issues/25).
        If no path is given a default directory "tmp/icond2/" will be created.
        
    Properties
    ----------
    locations : dict
        The locations to forecast
    forecastHours : int
        The number of forecast hours
    currentRun : string
        The hours as string of the current run
    currentRunDateTime : datetime
        The init datetime of the current run
    '''   

    def __init__(self, locations, forecastHours, tmpFp = None):
        
        if tmpFp is None:
            
            p = "tmp/icond2/"
            
            self._tmpFp = p
            
            if not os.path.exists(p):
                os.makedirs(p)
            
        else:
            self._forecastHours = tmpFp
        
        self._forecastHours = forecastHours
        self._locations = locations
        self._src = "https://opendata.dwd.de/weather/nwp/icon-d2/grib/"
        self._currentRun = self._getCurrentRun(datetime.now(timezone.utc)) 
         
    
    @property
    def locations(self):
        return self._locations  


    @property
    def forecastHours(self, value):
        return self._forecastHours 
    
    
    @property
    def currentRun(self):
        return self._currentRun 
    
    
    def _getCurrentRun(self, now_utc):
        
        '''Gets the number of the current run by current time. 
        The latest run is fully available ~2h after initialisation.
        e.g. The 09 run will be finished at approx 11:00 UTC.
        
        Parameters
        ----------
        now_utc : datetime
            The current datetime
            
        Returns
        -------
        string
            The run hour as a string (00, 03, 06 ...)
        '''
        
        h = now_utc.hour
        run_hour = "00"
        
        if h >= 2:
            run_hour = "00"        
        if h >= 5:
            run_hour = "03"
        if h >= 8:
            run_hour = "06"        
        if h >= 11:
            run_hour = "09"
        if h >= 14:
            run_hour = "12"
        if h >= 17:
            run_hour = "15"
        if h >= 20:
            run_hour = "18"            
        if h >= 23 and h < 2:
            run_hour = "21"
        
        self._currentRun = run_hour     
        
        return run_hour
    
            
    def createDownloadUrl(self, var):

        '''Creates the download urls
        
        Parameters
        ----------
        var : string
            The variable name
            
        Returns
        -------
        list
            List with urls
        '''
        
        urls = []

        now_utc = datetime.now(timezone.utc)
        urlDate = now_utc.strftime("%Y%m%d") 

        url = "{src}{run}/{var}".format(src = self._src, var = var, run = self._currentRun) 
        
        hours = self._forecastHours
        
        if self._forecastHours is None:
            hours = 49
        
        for h in range(hours):
            
            hStr = str(h).zfill(2)
            fileName = "icon-d2_germany_regular-lat-lon_single-level_{ds}{run}_0{h}_2d_{var}.grib2.bz2".format(h = hStr,
                                                                                                      run = self._currentRun,
                                                                                                      var = var,
                                                                                                      ds = urlDate)
            filePath = "{url}/{fn}".format(url = url, fn = fileName) 
            
            urls.append(filePath)
    
        return urls
    
    
    def downloadAndExtractBzFile(self, url, destFp):

        '''Downloads the file from an url und extracts the content.
        
        Parameters
        ----------
        url : string
            The url for the file to download
        destFp : string 
            The path to save the file. Should be a tmp path.
        '''
        
        try:
            r = requests.get(url)
            if r.status_code == 200:
                with open(destFp, 'wb') as f:
                    f.write(decompress(r.content))
                
        except Exception as err:
            print("Could not get {url}: {err}".format(err = err, url = url))        


    def _getVarnameFromNcFile(self, ncFile):
        
        '''Extracts the nc intern weather variable name from the netCDF file
        
        Parameters
        ----------
        ncFile : xarray
            The netCDF file
            
        Returns
        -------
        string
            The nc intern weather variable name
        ''' 
        
        var = None
        
        for var in ncFile.variables:
            
            varDims = len(ncFile.variables[var].shape)
            
            if varDims >= 2:
                ncVarName = var
        
        return ncVarName


    def extractValuesFromGrib(self, fp, data):
        
        '''Extract the value from the grib file for the locations.
        
        Parameters
        ----------
        fp : string
            The filepath to the netCDF file
        data : pd.Series
            The series is given by reference and will be filled
            iteratively.
        '''   
        
        ncFile = xr.open_dataset(fp, engine='cfgrib')
        ncVarName = self._getVarnameFromNcFile(ncFile)
        stepValues = ncFile.step.values
        hasStepIndex = True
        
        if not isinstance(stepValues, Iterable):
            stepValues = [stepValues]
            hasStepIndex = False
                    
        for locName, coords in self.locations.items():
            
            lat = coords["lat"]
            lon = coords["lon"] 
        
            for step in stepValues:
                
                if hasStepIndex is True:
                    nearestPointVal = ncFile.sel(step = step,
                                                 latitude=lat, 
                                                 longitude=lon, 
                                                 method="nearest")[ncVarName].values
                else:
                    nearestPointVal = ncFile.sel(latitude=lat, 
                                                 longitude=lon, 
                                                 method="nearest")[ncVarName].values
                    
                dt_forecast = ncFile.time.values + step
                
                idx = "{n},{t},{de}".format(n = locName, t = ncFile.time.values, de = dt_forecast)
                
                data.loc[idx] = np.float32(nearestPointVal)
                
        os.remove(fp)
    
    
    def mainDataCollector(self, iterItem):

        '''Collects the data for all timesteps for one variable
        
        Parameters
        ----------
        iterItem : tuple
            Tuple with variable key and variable value
 
        Returns
        -------
        dict
            The collected data
        '''
        data = pd.Series()        
        
        urls = self.createDownloadUrl(iterItem) # url for one variable
        
        for url in urls:
    
            print("ICON data -> Processing file: {f}".format(f = url))                
    
            tmpfn = os.path.basename(url) # tmp file name
            tmpfn = Path(tmpfn).with_suffix('')
            tmpfp = "{p}/{tmpfn}".format(tmpfn = tmpfn, p = self._tmpFp) # tmp file path
            
            # Download the zip file and save it temporarely
            self.downloadAndExtractBzFile(url, tmpfp)
            
            # Extract values from grib file
            try:
                self.extractValuesFromGrib(tmpfp, data)
            except Exception as err:
                print("ERROR Can't extract values from grib file: {e}".format(e = err))
        

        idx_s = data.index.str.split(",")
        idx_t = [(list(x)[0], np.datetime64(list(x)[1]), np.datetime64(list(x)[2])) for x in idx_s]
        data.index = pd.MultiIndex.from_tuples(idx_t, names=["location", "dt_forecast_init", "dt_forecast"])
        
        data = data.rename(iterItem)

        return data
    
    
    
    def collectData(self, varList, cores = None):
        
        '''Collect the whole data. Will take a bit more time 
        because every grib file has to be downloaded, extracted 
        and opened seperately.
        
        Parameters
        ----------
        varList : list
            A list with variable names
            
            .. code-block:: python
            
                variables = ["aswdir_s", "aswdifd_s", "t_2m"]
        cores : int
            Number of cores to use. Default value is None. So no 
            multiprocessing is applied. On some windows machines 
            multiprocessing is problematic.
 
        Returns
        -------
        pd.DataFrame
            The data as an dataframe
        ''' 

    
        if cores is None:
            
            result = []
            
            for item in varList:
                res = self.mainDataCollector(item)  
                result.append(res)
              
        else:
            # Parallel processing of downloading and extracting grib data
            pool = multiprocessing.Pool()
            result = pool.map(self.mainDataCollector, varList)
            pool.close()
            pool.join()

        # Collect thte data
        data = pd.DataFrame()
        data = pd.concat(result, axis=1)

        # Sort data
        data = data.sort_values(["location", "dt_forecast"])

        # Remove all .idx files in the tmp folder
        path = "{tfp}/*grib*".format(tfp = self._tmpFp)
        fileList = glob.glob(path)

        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error while deleting file : ", filePath)
        
        return data        
        


