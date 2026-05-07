
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
    excavator_cycle: str 
    excavator_type: str 
    angle_of_swing: float 
    depth_of_cut: float 
    
    bucket_fill_factor: Optional[float] = 1.0
    volume_correction_factor: Optional[float] = 1.0
    efficiency_factor: Optional[float] = 1.0
    heaped_bucket_capacity: Optional[float] = None
    cycle_time: int 
    

    @computed_field
    @property
    def asd(self) -> Optional[float]:
        if self.angle_of_swing and self.depth_of_cut:
            return self.angle_of_swing * self.depth_of_cut
        return 1.0
    
    @computed_field
    @property
    def productivity(self) -> Optional[float]:
        if (self.total_cycle_time and self.total_cycle_time != 0) and self.actual_bucket_capacity:
            p = 3600 * self.bucket_fill_factor * self.asd * self.efficiency_factor * self.heaped_bucket_capacity  / (self.cycle_time *  self.volume_correction_factor)
            return p
        return None


class DozerRecord(EquipmentBase):
    dozer_cycle: str 
    dozer_blade_type: str 
    blade_width: float 
    blade_length: float 
    blade_height: float
    
    cycle_time: int 
    

    @computed_field
    @property
    def blade_load(self) -> Optional[float]:
        if self.blade_width and self.blade_length and self.blade_height:
            return self.blade_width * self.blade_length * self.blade_height
        return None
    
    @computed_field
    @property
    def productivity(self) -> Optional[float]:
        if (self.cycle_time and self.cycle_time != 0) and self.blade_load:
            p = 3600 * self.blade_load / (self.cycle_time)
            return p
        return None
    

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

    # print(truck.model_dump())