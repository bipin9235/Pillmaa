from typing import List, Optional
from pydantic import BaseModel, Field

class DrugDosageFrequency(BaseModel):
    frequency_type: str = Field(
        description="Frequency of dosage (e.g., daily, every 8 hours, as needed)."
    )
    time_of_day: Optional[str] = Field(
        default="Not Mentioned",
        description="Specific time of day for dosage (e.g., morning, afternoon, bedtime)."
    )
    condition: Optional[str] = Field(
        default="Not Mentioned",
        description="Condition for taking medicine (e.g., if fever occurs, after meal, before meal)."
    )

class Medicine(BaseModel):
    drug_name: str = Field(
        description="Name of prescribed medicine along with its strength (e.g., 500mg, 10ml)."
    )
    dose: str = Field(
        description="Exact dose prescribed (e.g., 1 capsule, 5ml syrup, 2 tablets)."
    )
    duration: str = Field(
        description="Duration of medication (e.g., 5 days, 2 weeks, 3 months)."
    )
    drug_dosage_frequency: DrugDosageFrequency = Field(
        description="Structured dosage frequency details."
    )

class PrescriptionModel(BaseModel):
    medicines: List[Medicine]