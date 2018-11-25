import uuid

import ifcopenshell
from .models import Vector

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


def create_3d_grid(ifcfile,
                   section_xaxis=5,
                   section_yaxis=3,
                   section_zaxis=2):
    polylines = []
    xaxis_grids = []
    yaxis_grids = []
    dis_bw_sections = 10.0
    # Create grid in x-y plane

    # create x-axis lines
    vec1 = Vector(0.0, dis_bw_sections, 0.0)
    vec2 = Vector(dis_bw_sections * section_xaxis + dis_bw_sections, dis_bw_sections, 0.0)
    for i in range(section_yaxis):
        pt1 = ifcfile.createIfcCartesianPoint(vec1.get_tuple())
        pt2 = ifcfile.createIfcCartesianPoint(vec2.get_tuple())
        vec1.y += dis_bw_sections
        vec2.y += dis_bw_sections
        polyline = ifcfile.createIfcPolyLine((pt1, pt2,))
        grid_axis = ifcfile.createIfcGridAxis('x{}'.format(i),
                                          polyline, True)
        polylines.append(polyline)
        xaxis_grids.append(grid_axis)

    # create y-axis lines
    vec1 = Vector(dis_bw_sections, 0.0, 0.0)
    vec2 = Vector(dis_bw_sections, dis_bw_sections * section_yaxis + dis_bw_sections, 0.0)
    for i in range(section_xaxis):
        pt1 = ifcfile.createIfcCartesianPoint(vec1.get_tuple())
        pt2 = ifcfile.createIfcCartesianPoint(vec2.get_tuple())
        vec1.x += dis_bw_sections
        vec2.x += dis_bw_sections
        polyline = ifcfile.createIfcPolyLine((pt1, pt2,))
        grid_axis = ifcfile.createIfcGridAxis('y{}'.format(i),
                                          polyline, True)
        polylines.append(polyline)
        yaxis_grids.append(grid_axis)

    placement = create_ifclocalplacement(ifcfile)
    geometric_curve_set = ifcfile.createIfcGeometricCurveSet(polylines)
    geometric_representation_context = ifcfile.by_type('IfcGeometricRepresentationContext')[0]
    shape_representation = ifcfile.createIfcShapeRepresentation(
        ContextOfItems = geometric_representation_context,
        RepresentationIdentifier = 'FootPrint',
        RepresentationType = 'GeometricCurveSet',
        Items = polylines
    )
    product_definition_shape = ifcfile.createIfcProductDefinitionShape(
        Representations = (shape_representation, )
    )
    owner_history = ifcfile.by_type("IfcOwnerHistory")[0]
    grid = ifcfile.createIfcGrid(
        GlobalId = create_guid(),
        OwnerHistory = owner_history,
        Name = 'Axes',
        ObjectPlacement = placement,
        Representation = product_definition_shape,
        UAxes = xaxis_grids,
        VAxes = yaxis_grids
    )


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