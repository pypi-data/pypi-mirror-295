import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS, Transformer
from vgrid.utils.geocode import mgrs

def create_utm_grid_old(minx, miny, maxx, maxy, cell_size, crs):
    # Calculate the number of rows and columns based on cell size
    rows = int((maxy - miny) / cell_size)
    cols = int((maxx - minx) / cell_size)
    
    # Initialize a list to hold grid polygons
    polygons = []
    
    for i in range(cols):
        for j in range(rows):
            # Calculate the bounds of the cell
            x1 = minx + i * cell_size
            x2 = x1 + cell_size
            y1 = miny + j * cell_size
            y2 = y1 + cell_size
            
            # Create the polygon for the cell
            polygons.append(Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)]))
    
    # Create a GeoDataFrame with the polygons and set the CRS
    grid = gpd.GeoDataFrame({'geometry': polygons}, crs=crs)
    
    return grid

def create_utm_grid(minx, miny, maxx, maxy, cell_size, crs):
    """
    Create a grid of square polygons within a specified bounding box using UTM coordinates.

    Parameters:
    - minx, miny, maxx, maxy: Bounding box coordinates in meters.
    - cell_size: Size of each grid cell in meters.
    - crs: Coordinate reference system in UTM (e.g., EPSG:32648).

    Returns:
    - grid: GeoDataFrame containing grid polygons with unique MGRS codes.
    """
    # Calculate the number of rows and columns based on cell size
    rows = int((maxy - miny) / cell_size)
    cols = int((maxx - minx) / cell_size)
    
    # Initialize lists to hold grid polygons and MGRS codes
    polygons = []
    mgrs_codes = []
    
    # Set up transformer to convert UTM to WGS84 (longitude, latitude)
    transformer = Transformer.from_crs(crs, CRS.from_epsg(4326), always_xy=True)
    
    for i in range(cols):
        for j in range(rows):
            # Calculate the bounds of the cell
            x1 = minx + i * cell_size
            x2 = x1 + cell_size
            y1 = miny + j * cell_size
            y2 = y1 + cell_size
            
            # Create the polygon for the cell
            polygon = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
            polygons.append(polygon)
            
            # Calculate the centroid of the polygon
            centroid = polygon.centroid
            
            # Convert the centroid coordinates from UTM to WGS84 (longitude, latitude)
            lon, lat = transformer.transform(centroid.x, centroid.y)
            
            # Convert the WGS84 coordinates to MGRS
            mgrs_code = mgrs.toMgrs(lat, lon,5)
            mgrs_codes.append(mgrs_code)
    
    # Create a GeoDataFrame with the polygons and MGRS codes, and set the CRS
    grid = gpd.GeoDataFrame({'geometry': polygons, 'mgrs': mgrs_codes}, crs=crs)
    
    return grid



# Define the bounding box in UTM coordinates (minx, miny, maxx, maxy) for the Northern Hemisphere
# Example for UTM zone 48N (EPSG:32648)
# bbox = (100000, 0, 900000, 9500000) # for the North 
# bbox = (100000, 100000, 900000, 10000000) # for the South 
bbox = (100000, 0, 900000, 10000000) #  # for both
cell_size = 100000  # Cell size in meters

# Create the grid with UTM CRS
epsg_code = 32648

crs = CRS.from_epsg(epsg_code)
grid = create_utm_grid(*bbox, cell_size, crs)

# Save the grid as a polygon shapefile
grid.to_file(f'utm_grid_{epsg_code}_polygons.shp')
