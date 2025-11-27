from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class MedicineForm(str, Enum):
    tablet = "tablet"
    syrup = "syrup"
    capsule = "capsule"
    injection = "injection"

class IntakeUnit(str, Enum):
    tablet = "tablet"
    capsule = "capsule"
    ml = "ml"
    drops = "drops"
class DoseFrequency(str, Enum):
    Daily='Daily'
    Monthly='Monthly'
    Weekly='Weekly'

class Schedule(BaseModel):
    dose_frequency_hours: int = Field(..., description="Hours between doses")
    dose_frequency: DoseFrequency
    administration_notes: Optional[str] = Field(None, description="Special instructions")

class Medicine(BaseModel):
    medicine_full_name: str = Field(..., description="Medicine name + strength")
    medicine_form: MedicineForm
    intake_quantity: int = Field(..., description="Units per intake")
    intake_unit: IntakeUnit
    course_lenght_days: int = Field(..., description="Course length in days")
    intake_schedule: Schedule
    prescribed_by: Optional[str] = None
    notes: Optional[str] = None

class Prescription(BaseModel):
    medicines: List[Medicine]