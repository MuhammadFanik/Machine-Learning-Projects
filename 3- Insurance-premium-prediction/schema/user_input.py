from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Optional, Annotated
from config.city_tier import tier_1_cities, tier_2_cities



# Pydantic model: This validates all the incoming data before it touches your model
class UserInput(BaseModel):
    age: Annotated[int, Field(..., description="Age of the user in years", gt=0, lt=120)]
    weight: Annotated[float, Field(..., description="weight of the user in kgs", gt=0)]
    height: Annotated[float, Field(..., description="Height of the user in mtrs", gt=0, lt=2.7)]
    income_lpa: Annotated[float, Field(..., description="Income of the user in lacs per annum", gt=0)]
    smoker: Annotated[bool, Field(..., description="Is the user a smoker or not?")]
    city: Annotated[str, Field(..., description="The city that the user belongs to")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="occupation of the user")]


    # Computed fields are basically feature engineering inside pydantic model

    @field_validator("city")
    @classmethod
    def title_city(cls, v: str) -> str:
        v = v.strip().title()
        return v

    # Calculates BMI
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height**2)
        return bmi

    # Categorizes Lifestyle risk on their bmi and smoking habit
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    # Categorizes age groups
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    # Categorizes people in different tier cities
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3