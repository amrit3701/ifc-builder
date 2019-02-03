""" ifc_builder package."""

try:
    import ifcopenshell
except ModuleNotFoundError:
    raise (
        """ifcopenshell module not found. Install it by following
        http://www.ifcopenshell.org/python.html"""
    )
