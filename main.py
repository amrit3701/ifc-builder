import uuid
import time
import tempfile

import ifcopenshell
from src.template import get_template
from src.helpers import (create_guid,
                         create_ifclocalplacement,
                         create_ifcaxis2placement,
                         create_ifcpolyline)


# IFC template creation
filename = "output.ifc"
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Amritpal Singh"
organization = "Great Developer"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), "Experimenting"

# Write the template to a temporary file 
temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
template = get_template(
    filename=filename,
    timestamp=timestamp,
    timestring=timestring,
    creator=creator,
    organization=organization,
    application=application,
    application_version=application_version,
    project_globalid=project_globalid,
    project_name=project_name
)
with open(temp_filename, "wb") as f:
    f.write(template)

ifcfile = ifcopenshell.open(temp_filename)
owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
project = ifcfile.by_type("IfcProject")[0]
context = ifcfile.by_type("IfcGeometricRepresentationContext")[0]

# IFC hierarchy creation
site_placement = create_ifclocalplacement(ifcfile)
site = ifcfile.createIfcSite(
    GlobalId=create_guid(), 
    OwnerHistory=owner_history,
    Name="Site", 
    ObjectPlacement=site_placement,
    CompositionType="COMPLEX"
)

building_placement = create_ifclocalplacement(ifcfile, relative_to=site_placement)
building = ifcfile.createIfcBuilding(
    GlobalId=create_guid(),
    OwnerHistory=owner_history,
    Name='Building',
    ObjectPlacement=building_placement,
    CompositionType="COMPLEX"
)

ifcfile.createIfcRelAggregates(
    GlobalId=create_guid(),
    OwnerHistory=owner_history,
    RelatingObject=site,
    RelatedObjects=[building]
)

ifcfile.write(filename)