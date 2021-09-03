from dwdGribExtractor.icon import ICON_D2

loc = {
    "lat": 47,
    "lon": 15     
}

variables = {
    "aswdir_s": { # the key is the subdirectory name to the variable in the ftp storage
        "ncInternVarName": "ASWDIR_S" # the value is the defined variable name  in the netCDF file
    },
    "aswdifd_s": {
        "ncInternVarName": "ASWDIFD_S"
    },
    "t_2m": {
        "ncInternVarName": "t2m"
    }  
}

forecast = ICON_D2(location = loc, forecastHours = 3)
data = forecast.collectData(varList = variables, cores = 4)



