from __future__ import division, print_function, absolute_import

# Conditional import machinery for fury
from dipy.utils.optpkg import optional_package

# Allow import, but disable doctests if we don't have fury
fury, have_fury, setup_module = optional_package('fury')

if have_fury:
    from dipy.viz import utils, vtk


def load_polydata(file_name):
    """Load a vtk polydata to a supported format file.

    Supported file formats are OBJ, VTK, FIB, PLY, STL and XML

    Parameters
    ----------
    file_name : string

    Returns
    -------
    output : vtkPolyData

    """
    # get file extension (type) lower case
    file_extension = file_name.split(".")[-1].lower()

    if file_extension == "vtk":
        reader = vtk.vtkPolyDataReader()
    elif file_extension == "fib":
        reader = vtk.vtkPolyDataReader()
    elif file_extension == "ply":
        reader = vtk.vtkPLYReader()
    elif file_extension == "stl":
        reader = vtk.vtkSTLReader()
    elif file_extension == "xml":
        reader = vtk.vtkXMLPolyDataReader()
    elif file_extension == "obj":
        try:  # try to read as a normal obj
            reader = vtk.vtkOBJReader()
        except Exception:  # than try load a MNI obj format
            reader = vtk.vtkMNIObjectReader()
    else:
        raise "polydata " + file_extension + " is not suported"

    reader.SetFileName(file_name)
    reader.Update()
    # print(file_name + " Mesh " + file_extension + " Loaded")
    return reader.GetOutput()


def save_polydata(polydata, file_name, binary=False, color_array_name=None):
    """Save a vtk polydata to a supported format file.

    Save formats can be VTK, FIB, PLY, STL and XML.

    Parameters
    ----------
    polydata : vtkPolyData
    file_name : string

    """
    # get file extension (type)
    file_extension = file_name.split(".")[-1].lower()

    if file_extension == "vtk":
        writer = vtk.vtkPolyDataWriter()
    elif file_extension == "fib":
        writer = vtk.vtkPolyDataWriter()
    elif file_extension == "ply":
        writer = vtk.vtkPLYWriter()
    elif file_extension == "stl":
        writer = vtk.vtkSTLWriter()
    elif file_extension == "xml":
        writer = vtk.vtkXMLPolyDataWriter()
    elif file_extension == "obj":
        raise Exception("mni obj or Wavefront obj ?")
    #    writer = utils.set_input(vtk.vtkMNIObjectWriter(), polydata)

    writer.SetFileName(file_name)
    writer = utils.set_input(writer, polydata)
    if color_array_name is not None:
        writer.SetArrayName(color_array_name)

    if binary:
        writer.SetFileTypeToBinary()
    writer.Update()
    writer.Write()
