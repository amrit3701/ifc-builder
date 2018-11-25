import uuid
import time
import tempfile
from config import *

import ifcopenshell
from src.template import get_template
from src.helpers import (create_guid,
                         create_ifclocalplacement,
                         create_ifcaxis2placement,
                         create_ifcpolyline,
                         create_3d_grid)



# Write the template to a temporary file 
temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
template = get_template(
    filename=FILE_NAME,
    timestamp=time.time(),
    timestring=time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(time.time())),
    creator=CREATOR,
    organization=ORGANISATION,
    application="IfcOpenShell",
    application_version="0.5",
    project_globalid=create_guid(),
    project_name=PROJECT_NAME
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
    Name=SITE_NAME, 
    ObjectPlacement=site_placement,
    CompositionType=SITE_COMP
)

building_placement = create_ifclocalplacement(ifcfile, relative_to=site_placement)
building = ifcfile.createIfcBuilding(
    GlobalId=create_guid(),
    OwnerHistory=owner_history,
    Name=BUILD_NAME,
    ObjectPlacement=building_placement,
    CompositionType=BUILD_COMP
)

ifcfile.createIfcRelAggregates(
    GlobalId=create_guid(),
    OwnerHistory=owner_history,
    RelatingObject=site,
    RelatedObjects=(building,)
)

create_3d_grid(ifcfile, 10, 8)
ifcfile.write(FILE_NAME)
