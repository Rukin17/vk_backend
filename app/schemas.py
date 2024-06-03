from pydantic import BaseModel, ConfigDict


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pass 


class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pass

