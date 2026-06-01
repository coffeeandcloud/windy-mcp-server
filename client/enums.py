from enum import Enum


class TempUnit(str, Enum):
    kelvin = "K"
    celsius = "°C"


class Model(str, Enum):
    # Weather models
    arome = "arome"
    arome_antilles = "aromeAntilles"
    arome_france = "aromeFrance"
    arome_reunion = "aromeReunion"
    icon = "icon"
    icon_d2 = "iconD2"
    icon_eu = "iconEu"
    gfs = "gfs"
    nam_conus = "namConus"
    nam_hawaii = "namHawaii"
    nam_alaska = "namAlaska"
    hrrr_conus = "hrrrConus"
    hrrr_alaska = "hrrrAlaska"
    can_hrdps = "canHrdps"
    # Wave models
    gfs_wave = "gfsWave"
    icon_wave = "iconWave"
    icon_eu_wave = "iconEuWave"
    can_rdwps_wave = "canRdwpsWave"
    # Air quality models
    cams = "cams"
    cams_eu = "camsEu"


class Parameter(str, Enum):
    # Temperature & humidity
    temp = "temp"
    dewpoint = "dewpoint"
    rh = "rh"
    # Pressure & height
    pressure = "pressure"
    gh = "gh"
    # Precipitation
    precip = "precip"
    snow_precip = "snowPrecip"
    conv_precip = "convPrecip"
    # Wind
    wind = "wind"
    wind_gust = "windGust"
    # Clouds & visibility
    lclouds = "lclouds"
    mclouds = "mclouds"
    hclouds = "hclouds"
    cbase = "cbase"
    visibility = "visibility"
    # Atmospheric
    cape = "cape"
    ptype = "ptype"
    weather_warnings = "weatherWarnings"
    # Wave
    waves = "waves"
    wind_waves = "windWaves"
    waves_power = "wavesPower"
    swell1 = "swell1"
    swell2 = "swell2"
    # Air quality
    aqi = "aqi"
    so2sm = "so2sm"
    dustsm = "dustsm"
    cosc = "cosc"
    go3 = "go3"
    no2 = "no2"
    pm10 = "pm10"
    pm2p5 = "pm2p5"
    # Pollen
    pollen_alder = "pollenAlder"
    pollen_birch = "pollenBirch"
    pollen_grass = "pollenGrass"
    pollen_mugwort = "pollenMugwort"
    pollen_olive = "pollenOlive"
    pollen_ragweed = "pollenRagweed"


class Level(str, Enum):
    surface = "surface"
    hPa1000 = "1000h"
    hPa950 = "950h"
    hPa925 = "925h"
    hPa900 = "900h"
    hPa850 = "850h"
    hPa800 = "800h"
    hPa700 = "700h"
    hPa600 = "600h"
    hPa500 = "500h"
    hPa400 = "400h"
    hPa300 = "300h"
    hPa200 = "200h"
    hPa150 = "150h"
