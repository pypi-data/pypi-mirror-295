# raster_to_vector
convert GIS WMTS tile image to polygon and point using computer vision

### define your tile image request function
the function should cache images to speed up
```python
from raster_to_vector import GetTile

get_tile = GetTile('https://my-wmts/{z}/{y}/{x}')
```

### (lng lat zoom) to polygon
expand tile from given point until bounded by area
```python
from raster_to_vector import find_polygon_from_point

polygon = find_polygon_from_point(lng=120.67, lat=24.171, z=9, get_tile=get_tile)
print(polygon.wkt)
```

### find all text (lng lat) in bounded area
recognize text based on rapidocr-onnxruntime engine
```python
from raster_to_vector import find_text_in_area

found, queue = find_text_in_area(bound=polygon, z=9, get_tile=get_tile)
for point, text in found:
    print(text, point.wkt)
```

### convert raster to vector in bounded area
the algorithm will zoom in if the unknown area does not show text
```python
from raster_to_vector import find_polygon_in_area

results = find_polygon_in_area(bound=polygon, z=9, maxz=10, get_tile=get_tile)
for polygon, text in results:
    print(text, polygon.wkt)
```