
from pymrio.tools.iodownloader import (download_eora26,
                                       download_exiobase1,
                                       download_exiobase2,
                                       download_exiobase3,
                                       download_oecd,
                                       download_wiod2013,
)

import os
import requests
import shutil
from mario.log_exc.exceptions import WrongInput


def download_hybrid_exiobase(path):

    exiobase_files = {
        "MR_HUSE_2011_v3_3_18.csv":"https://zenodo.org/record/7244919/files/MR_HUSE_2011_v3_3_18.csv?download=1",
        "MR_HSUTs_2011_v3_3_18_FD.csv":"https://zenodo.org/record/7244919/files/MR_HSUTs_2011_v3_3_18_FD.csv?download=1",
        "MR_HSUP_2011_v3_3_18.csv":"https://zenodo.org/record/7244919/files/MR_HSUP_2011_v3_3_18.csv?download=1",
        "MR_HSUTs_2011_v3_3_18_extensions.xlsx":"https://zenodo.org/record/7244919/files/MR_HSUTs_2011_v3_3_18_extensions.xlsx?download=1",
        "metadata.xlsx": "https://zenodo.org/record/7244919/files/Classifications_v_3_3_18.xlsx?download=1",
    }

    if os.path.exists(path):
        shutil.rmtree(path)
    
    os.mkdir(path)


    for file,url in exiobase_files.items():
        file_path = f"{path}/{file}"

        response = requests.get(url)

        open(file_path, "wb").write(response.content)


def download_figaro(table,year,path,format=None):
    """Downloads a FIGARO table

    Parameters
    ----------
    table : str
        type of table ["SUT" or "IOT"]
    year : int
        the year of database range(2010,2022)
    path : str
        where to store data
    format : str, optional
        when IOT table is chosen, one of ["product by product","industry by industry"] assumptions should be chosen, by default None

    Raises
    ------
    WrongInput
        if invalid combinations are given
    """

    tables = ["IOT","SUT"]
    years = list(range(2010,2022))
    logics = ["product by product","industry by industry"]

    def build_url(table,format,year):

        urls = {
            "SUT":{
                "supply":"https://ec.europa.eu/eurostat/documents/51957/17979405/matrix_eu-ic-supply_23ed_{year}.csv",
                "use": "https://ec.europa.eu/eurostat/documents/51957/17979408/matrix_eu-ic-use_23ed_{year}.csv"
                },
            
            "IOT": {
                "prod-by-prod":"https://ec.europa.eu/eurostat/documents/51957/17979411/matrix_eu-ic-io_prod-by-prod_23ed_{year}.csv",
                "ind-by-ind":"https://ec.europa.eu/eurostat/documents/51957/17979414/matrix_eu-ic-io_ind-by-ind_23ed_{year}.csv",
            },

            # "extensions":{
            #     "employement":"https://ec.europa.eu/eurostat/documents/51957/17994554/EMPLOYMENTindicator64industries_23ed_{year}.xlsx",
            #     "value-added": "https://ec.europa.eu/eurostat/documents/51957/17987259/VAindicator64industries_23ed_{year}.xlsx",
            #     "carbon-footprint": "https://ec.europa.eu/eurostat/documents/51957/14504006/CO2footprint-2010-2021.zip/fc6fd913-a954-1af6-3485-4c4dcafb8bec?t=1709802335538",
            # }
            }
        
        if format == "carbon-footprint":
            return {format:urls[table][format]}
        

        return {format:urls[table][format].format(year=year)}

            
        
    urls = {}
    # for ff in ["employement","value-added","carbon-footprint"]:
    #     urls.update(**build_url("extensions",ff,year))
    # urls = {format:build_url("extensions",format).format(year=year) for format in }
    # urls["carbon-footprint"] = build_url("extensions","carbon-footprint")
    
    if table == "SUT":
        for ff in ["supply","use"]:
            urls.update(**build_url("SUT",ff,year))

        
    elif table == "IOT":
        if format is None:
            raise WrongInput("for IOT table, the format should be given. Acceptable options are:\n 1. prod-by-prod \n 2. ind-by-ind")
        urls.update(**build_url(table,format,year))
    
    if os.path.exists(path):
        shutil.rmtree(path)
    
    os.mkdir(path)


    for name,url in urls.items():

        if ".xlsx" in url:
            extension = ".xlsx"
        elif ".zip" in url:
            extension = ".zip"
        else:
            extension = ".csv"

        file = f"{name}_{year}{extension}"
        file_path = f"{path}/{file}"

        response = requests.get(url)

        open(file_path, "wb").write(response.content)

