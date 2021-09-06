from dwdGribExtractor.icon import ICON_D2
import numpy as np

def main():
    
    locationList = {     
        "Vienna": {
            "lat": 48.20,
            "lon": 16.37     
        },
        "Graz": {
            "lat": 47.07,
            "lon": 15.43     
        }
    }
    
    variables = ["aswdir_s", "aswdifd_s", "t_2m"]
    
    forecast = ICON_D2(locations = locationList, forecastHours = 3)
    #data = forecast.collectData(varList = variables, cores = None) # Disable multiprocessing
    data = forecast.collectData(varList = variables, cores = 4)
    
    
    #### Indexing one location
    loc = "Graz"
    result = data.loc[loc]
    result = data.loc[loc, "2021-09-06 06:15:00"]

    #### Indexing multiple locations
    loc = ["Graz", "Vienna"]
    result = data.loc[loc]
    
    #### Indexing one location with datetime condition
    loc = "Graz"
    mask = data.loc[loc].index.get_level_values(0) > np.datetime64('2021-09-06T06:15:00')
    mask = data.loc[loc].index.get_level_values(0).hour == 8
    result = data.loc[loc][mask]
    
    #### Indexing multiple locations with datetime condition
    loc = ["Graz", "Vienna"]
    mask = data.loc[loc].index.get_level_values(1) > np.datetime64('2021-09-06 06:15:00')
    mask = data.loc[loc].index.get_level_values(1).hour == 8
    result = data.loc[loc][mask]
    
    print(result)


if __name__ == "__main__":
    main()


