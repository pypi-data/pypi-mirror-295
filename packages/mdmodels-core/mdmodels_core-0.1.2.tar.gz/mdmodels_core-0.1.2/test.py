from pydantic import BaseModel, Field
from pydantic_xml import BaseXmlModel, element

class MyModel(BaseXmlModel):
    name: str
    json_only_field: str = element(tag="jsonOnlyField")

# Example usage:
model_instance = MyModel(name="example", json_only_field="visible_in_json_only")

# To JSON (this will include 'json_only_field'):
print(model_instance.json())

# To XML (this will exclude 'json_only_field'):
print(model_instance.to_xml())
