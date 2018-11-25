import uuid
import time
import tempfile

import ifcopenshell
from src.template import get_template
from src.helpers import (create_guid,
                         create_ifclocalplacement,
                         create_ifcaxis2placement,
                         create_ifcpolyline,
                         create_3d_grid)


filename="output.ifc"

# Write the template to a temporary file 
temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
template = get_template(
    filename=filename,
    timestamp=time.time(),
    timestring=time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time())),
    creator="Amritpal Singh",
    organization="Great Developer",
    application="IfcOpenShell",
    application_version="0.5",
    project_globalid=create_guid(),
    project_name="My project"
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
    RelatedObjects=(building,)
)

create_3d_grid(ifcfile, 10, 8)
ifcfile.write(filename)