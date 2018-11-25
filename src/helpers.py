import uuid

import ifcopenshell


O = 0., 0., 0.
X = 1., 0., 0.
Y = 0., 1., 0.
Z = 0., 0., 1.

create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)

def create_ifcaxis2placement(ifcfile,
                             point=O,
                             dir1=Z,
                             dir2=X):
    """ Creates an IfcAxis2Placement3D from Location, Axis and 
    RefDirection specified as Python tuples."""
    point = ifcfile.createIfcCartesianPoint(point)
    dir1 = ifcfile.createIfcDirection(dir1)
    dir2 = ifcfile.createIfcDirection(dir2)
    axis2placement = ifcfile.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

def create_ifclocalplacement(ifcfile,
                             point=O,
                             dir1=Z,
                             dir2=X,
                             relative_to=None):
    """ Creates an IfcLocalPlacement from Location, Axis and RefDirection,
    specified as Python tuples, and relative placement."""
    axis2placement = create_ifcaxis2placement(ifcfile,point,dir1,dir2)
    ifclocalplacement2 = ifcfile.createIfcLocalPlacement(relative_to,axis2placement)
    return ifclocalplacement2

def create_ifcpolyline(ifcfile,
                       point_list):
    """ Creates an IfcPolyLine from a list of points, specified as Python tuples."""
    ifcpts = []
    for point in point_list:
        point = ifcfile.createIfcCartesianPoint(point)
        ifcpts.append(point)
    polyline = ifcfile.createIfcPolyLine(ifcpts)
    return polyline


def get_attributes_and_its_type_of_ifc_entity(entity):
    """ Prints all the attributes and there type of given ifc entity."""
    ifc_entity = ifcopenshell.create_entity(entity)
    i = 0
    while True:
        try:
            print(ifc_entity.attribute_name(i),
                  ifc_entity.attribute_type(i))
            i += 1
        except:
            break