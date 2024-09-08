# VisualShape3D

## About VisualShape3D

VisualShape3D is an easy-to-use Python wrapper of matplotlib, designed to facilitate the creation of 3D polygons for educational purposes. The package allows the user to create a view, add built-in shapes into it as they are built, and display them all together in the end.

VisualShape3D include three basic shapes: Point, PolyLine, and Polygon. To create a 3D shape, the user follows a two-step process: first, they create a 2D shape in the yz plane, and then they transform its reference point to a new position (X,Y,Z), with a new orientation (alpha, beta) of its facet. By default, the first vertex of a shape acts as its reference point.

In addition to these basic functions, VisualShape3D also offers the ability to calculate the intersection of a line with a polygon, as defined in both PolyLine and Polygon, in the hope that VisualShape3D becomes an easy-to-use tool.


## Core Features
- Three shapes : Point, Segment and Polygon.
- Its logic for 3D definition : creating a 2D shape first in working plane and then moving its referene point to a desired 3D position and rotating its normal vector of facet to a designated orientation.
- It can check whether or not a point is inside a segment or polygon, by their magic functions `__contains__` as overloaded for Segment and Polygon.
- `__hash__` and `__eq__`, also overloaded for Point, Segment and Polygon.
- `__neg__` overloaded for polygon when one wants to know the list of vertices on its other side.


## Requirements

* [Python](http://www.python.org) 3 
* Matplotlib is installed.

## Documentation

To be continued.

## Installation
```bash
pip install VisualShape3D
```

## Usage
```Python
import VisualShape3D.geometry as vs
import VisualShape3D.plotable as rd       

view = rd.OpenView()

W,H = 2.0,1.5
shape = vs.Shape('rectangle',W,H)
shape = shape.move(to = (2,0,0), by = (45,30))

line1 = vs.Polyline((0,0,0),(3,1.,2))
P = shape.intersect(line1)
if P is not None :
    lines = line1.broken_at(P)
    view.add_plot(shape,style = {'facecolor':'cornflowerblue', 'edgecolor':'navy','alpha':0.5})
    view.add_plot(lines,style={'color':'k','linewidth':2,'node':'visible'})
    view.show(hideAxes=True,origin=True)
```

## Update log
`1.0.7`  fix the bug of Shape_rectangleWithHole
`1.0.6`  Change the about VisualShape3D
`1.0.5`  Add "Modeling a house with shape" and "Building model" jupyter files


## License

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## Contact
heliqun@ustc.edu.cn
