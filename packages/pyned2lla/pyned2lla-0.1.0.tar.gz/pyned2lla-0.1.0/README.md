# pyned2lla - NED (North East Down) to LLA (Latitude Longitude Altitude) conversion for Python

## Example use

```python
import pyned2lla
import math

D2R = math.pi/180.0
R2D = 180.0/math.pi

wgs84 = pyned2lla.wgs84()

(lat0, lon0, alt0) = 47.992875, 7.853876, 281 # Schwabentor, Freiburg
(north, east, down) = 1650, 170, 20

(lat, lon, alt) = pyned2lla.ned2lla(lat0*D2R, lon0*D2R, alt0, north, east, down, wgs84)
print((lat*R2D, lon*R2D, alt)) # Institute of Biology I, Faculty of Biology, University of Freiburg
```

The above should print approximately `(48.00771378931424, 7.8561542926911985, 261.21592491399497)`.

## License

MIT license
