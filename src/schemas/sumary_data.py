from pydantic import BaseModel


class SummaryData(BaseModel):
    device_id: str
    measure_type: str
    whole_value: int
    decimal_value: int
