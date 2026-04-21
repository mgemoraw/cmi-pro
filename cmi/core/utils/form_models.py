
from pydantic import BaseModel, computed_field
from datetime import date, datetime, timedelta
from typing import Optional 


class EquipmentBase(BaseModel):
    date: date
    project_code: str
    data_collector: str 
    number_of_equipemnt_types: Optional[int]  = 1
    particular: str
    task_type: str 
    task_description: str
    soil_type: str 
    unit: str 



class TruckRecord(EquipmentBase):
    equipment_tag: str 
    truck_plate: str
    total_cycle_time: int | None
    actual_bucket_capacity: float | None


    @computed_field
    @property
    def productivity(self) -> Optional[float]:
        if (self.total_cycle_time and self.total_cycle_time != 0) and self.actual_bucket_capacity:
            return self.actual_bucket_capacity / self.total_cycle_time * 60*60
        return None
    

class ExcavatorRecord(EquipmentBase):
    pass 



if __name__ == "__main__":
    truck = TruckRecord(
        date= date(2026, 2, 15),
        project_code='01',
        data_collector="Mamush",
        number_of_equipemnt_types=3,
        equipment_tag='01',
        particular="some particular",
        task_type="Transportation",
        task_description="Transportation in Earth",
        soil_type="Earth",
        unit="m3",
        actual_bucket_capacity=14,
        truck_plate="B00498",
        total_cycle_time=250,
    )

    print(truck.model_dump())