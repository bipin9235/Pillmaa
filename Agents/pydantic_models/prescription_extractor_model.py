from pydantic import BaseModel, Field
from typing import List

class DrugDosageFrequency(BaseModel):
    frequency_type: str = Field(
        description="Frequency of dosage (e.g., daily, every 8 hours, as needed)."
    )
    time_of_day: str = Field(
        description="Specific time of day for dosage (e.g., morning, afternoon, bedtime)."
    )
    condition: str = Field(
        description="Condition or reason for taking the medicine (e.g., for fever, for pain)."
    )

class Medicine(BaseModel):
    drug_name: str = Field(description="Name of prescribed medicine along with it's strength(e.g. mg/ml)")
    drug_dosage_frequency: DrugDosageFrequency = Field(
        description="Structured dosage frequency details."
    )
    drug_category: str = Field(description="Category of Drug.")

class PrescriptionModel(BaseModel):
    medicines: List[Medicine]

    
