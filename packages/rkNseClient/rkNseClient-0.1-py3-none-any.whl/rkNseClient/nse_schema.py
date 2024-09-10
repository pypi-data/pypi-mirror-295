from datetime import datetime
from pydantic import BaseModel, validator
from typing import List, Optional, Union

class BaseSchema(BaseModel):
    @validator('*')
    def strip_and_convert_none(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.lower() in ['na', 'nan', '', 'null', "-"]:
                return None
            return v
        else:
            return v
    
    @validator('*')
    def convert_to_datetime(cls, v):
        date_formats = [
            "%d-%b-%Y",    # 25-May-2023
            "%Y-%m-%d",    # 2023-05-25
            "%m/%d/%Y",    # 05/25/2023
            "%m-%d-%Y",    # 05-25-2023
            "%b %d, %Y",   # May 25, 2023
            "%B %d, %Y",   # May 25, 2023 (full month name)
            "%d %b %Y",    # 25 May 2023
            "%d %B %Y",    # 25 May 2023 (full month name)
            "%Y/%m/%d",    # 2023/05/25
            "%Y%m%d",      # 20230525
            "%d/%m/%Y",    # 25/05/2023
            "%d-%m-%Y",    # 25-05-2023
            "%Y.%m.%d",    # 2023.05.25
            "%d.%m.%Y",    # 25.05.2023
            "%m.%d.%Y",    # 05.25.2023
            "%m.%d.%y",    # 05.25.23
            "%m-%d-%y",    # 05-25-23
            "%d-%m-%y",    # 25-05-23
            "%Y%m%d%H%M%S",  # 20230525120000
            "%Y-%m-%dT%H:%M:%S",  # 2023-05-25T12:00:00
            "%Y-%m-%d %H:%M:%S",  # 2023-05-25 12:00:00
            "%Y-%m-%d %H:%M",     # 2023-05-25 12:00
            "%Y-%m-%d %I:%M:%S %p",  # 2023-05-25 12:00:00 PM
            "%Y-%m-%d %I:%M %p",     # 2023-05-25 12:00 PM
            "%d.%m.%y",    # 25.05.23 (with 2-digit year)
            "%m/%d/%y",    # 05/25/23 (with 2-digit year)
            "%m-%d-%y",    # 05-25-23 (with 2-digit year)
            "%d-%m-%y",    # 25-05-23 (with 2-digit year)
            # Add more date formats as needed
        ]
        if isinstance(v, str):
            for date_format in date_formats:
                try:
                    date_obj = datetime.strptime(v, date_format)
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    pass
        return v


class EquityInfoSchema(BaseSchema):
    symbol: Optional[str] = None
    nameOfCompany: Optional[str]
    series: Optional[str]
    dateOfListing: Optional[str]
    isinNumber: Optional[str]
    faceValue: Optional[int]
    marketLot: Optional[int]
    paidUpValue: Optional[int]