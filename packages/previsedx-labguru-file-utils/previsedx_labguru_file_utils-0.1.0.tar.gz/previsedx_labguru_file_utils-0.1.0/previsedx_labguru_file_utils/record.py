from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Record(BaseModel):
    previse_lab_id: Optional[str] = Field(None, alias="Name *")
    date_of_birth: Optional[str] = Field(None, alias="Date of Birth")
    # date_of_birth: Optional[date] = Field(None, alias="Date of Birth")
    collection_date: Optional[str] = Field(None, alias="Collection Date")
    # collection_date: Optional[date] = Field(None, alias="Collection Date")
    # barretts_diagnosis: Optional[str] = Field(None, alias="Barrett's Diagnosis")
    barretts_diagnosis: Optional[str] = Field(None, alias="Diagnosis")
    specimen_id: Optional[str] = Field(None, alias="Specimen ID")
    segment_length: Optional[str | float] = Field(None, alias="Segment Length (cm)")
    gender: Optional[str] = Field(None, alias="Gender")
    date_received: Optional[str] = Field(None, alias="Date Received")
    # date_received: Optional[date] = Field(None, alias="Date Received")
    ordering_physician: Optional[str] = Field(None, alias="Ordering Physician")
    clinic: Optional[str] = Field(None, alias="Ordering Physician Clinic")
    medical_record_id: Optional[int] = Field(None, alias="Medical Record ID")
    patient_name: Optional[str] = Field(None, alias="Patient Name")
    address: Optional[str] = Field(None, alias="Ordering Physician Address")
    city_state_zip: Optional[str] = Field(
        None, alias="Ordering Physician City State Zip"
    )
    treating_provider: Optional[str] = Field(None, alias="Treating Provider")
    report_date: Optional[date] = Field(None, alias="Report Date")

    # @field_validator("date_received")
    # def validate_date_received(cls, v):
    #     return datetime.strptime(v, "%m/%d/%Y").date() if isinstance(v, str) else v

    # @field_validator("report_date")
    # def validate_report_date(cls, v):
    #     return datetime.strptime(v, "%m/%d/%Y").date() if isinstance(v, str) else v

    @field_validator("collection_date", "report_date", "date_received")
    def validate_collection_date(cls, v):
        if isinstance(v, str):
            return v
            try:
                return datetime.strptime(v, "%m/%d/%Y").date()
            except ValueError:
                try:
                    return datetime.strptime(v, "%Y-%m-%d").date()
                except ValueError:
                    try:
                        return datetime.strptime(v, "%Y-%m-%d 00:00:00").date()
                    except ValueError:
                        raise ValueError(
                            "date_received must be in 'MM/DD/YYYY' or 'YYYY-MM-DD' or 'YYYY-MM-DD 00:00:00' format"
                        )
        elif isinstance(v, date):
            return v
        else:
            return v

    # @field_validator("segment_length")
    # def validate_segment_length(cls, v):
    #     if math.isnan(v):
    #         return None  # Return None for NaN values
    #     elif isinstance(v, float):
    #         return str(v)  # Convert floats to strings
    #     return v

    # @field_validator("segment_length")
    # def validate_segment_length(cls, v):
    #     if v == "nan":
    #         return None
    #     if math.isnan(v):
    #         return None
    #     elif isinstance(v, float):
    #         return str(v)
    #     return v
