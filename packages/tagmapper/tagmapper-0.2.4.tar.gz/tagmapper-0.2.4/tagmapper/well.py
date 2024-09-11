from typing import List
import pandas as pd

from tagmapper.attribute import Attribute
from tagmapper.connector import query


class Well:
    """
    Well class
    """

    _well_attributes = pd.DataFrame()

    def __init__(self, uwi):
        if isinstance(uwi, str):
            # assume data is UWI
            data = Well.get_well_attributes(uwi)
        elif isinstance(uwi, pd.DataFrame):
            data = uwi

        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a dataframe")

        if data.empty:
            raise ValueError("Input data can not be empty")

        # self.inst_code = data["STID_CODE"].iloc[0]
        # self.object_name = data["OBJECT_NAME"].iloc[0]
        # self.object_code = data["PDM.OBJECT_CODE"].iloc[0]
        self.uwi = data["Unique_Well_Identifier"].iloc[0]

        self.attributes = []
        for _, r in data.iterrows():
            self.attributes.append(Attribute(r.to_dict()))

    @classmethod
    def get_all_wells(cls):
        uwi = Well.get_uwis()
        well = []

        for u in uwi:
            well.append(Well(Well.get_well_attributes(u)))

        return well

    @classmethod
    def get_well(cls, inst_code: str, tag_no: str):
        return Well(Well.get_well_attributes(f"{inst_code}-{tag_no}"))

    @classmethod
    def get_well_attributes(cls, uwi: str = ""):
        if cls._well_attributes.empty:
            cls._well_attributes = query("select * from [dbo].[mapped_well_attributes]")

        if uwi:
            ind = cls._well_attributes["Unique_Well_Identifier"] == uwi
            return cls._well_attributes.loc[ind, :]
        else:
            return cls._well_attributes

    @staticmethod
    def get_uwis(facility: str = "") -> List[str]:
        d = Well.get_well_attributes()
        if facility:
            pass
        uwi = list(d["Unique_Well_Identifier"].unique())
        uwi.sort()
        return uwi
