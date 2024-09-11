import numpy as np
from geopandas import GeoDataFrame
from scipy.spatial import cKDTree

from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.proccessing.operations.geodesy import GeodesyOps


class SpatialAnalysis:
    @staticmethod
    def create_idw_surface(data_gdf: GeoDataFrame, attribute_name: str, ref_raster: RioRaster, k_neighbours=3,
                           power: int = 2):
        """
        Perform IDW interpolation over the area of interest considering k nearest neighbors.

        Parameters:
        - data_gdf (GeoDataFrame): GeoDataFrame containing the meteorological data points with their associated geometries.
          - The GeoDataFrame should include a 'geometry' column with Point geometries.
          - The parameter to be interpolated should be present as a column in this GeoDataFrame.


        - attribute_name (str): The name of the column in meteo_gdf that contains the values to be interpolated.
          - Default is 'precipitation_sum', but it can be any other numeric column in meteo_gdf.

        - ref_raster: The reference raster to be used for interpolating the data value

        - k_neighbours (int): The number of nearest neighbors to consider for the interpolation.
          - Default is 3, meaning the interpolation will be based on the three nearest neighbors.
          - Adjusting this can affect the smoothness and accuracy of the resulting surface.

        - power (int or float): The power parameter for IDW interpolation.
          - This controls the weighting of the distances. Higher values give more influence to closer points.
          - Default is 2, which is a commonly used value.

        Returns:
            - RioRaster object: Raster
        """
        if data_gdf.crs.to_epsg() != ref_raster.get_crs().to_epsg():
            data_gdf = data_gdf.to_crs(ref_raster.get_crs())
        # Extract coordinates and corresponding values
        coords = np.array([(geom.x, geom.y) for geom in data_gdf.geometry])
        values = data_gdf[attribute_name].values

        # Generate grid points within AOI bounds
        minx, miny, maxx, maxy = ref_raster.get_raster_extent()
        height, width = ref_raster.get_img_resolution()
        grid_x, grid_y = np.meshgrid(
            np.linspace(minx, maxx, width),
            np.linspace(miny, maxy, height)
        )
        grid_points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T

        # Perform IDW with k nearest neighbors
        tree = cKDTree(coords)
        # Determine the number of nearest neighbors to query
        k_neighbours = min(k_neighbours, len(values))  # Ensure k does not exceed the number of known values

        dist, idx = tree.query(grid_points, k=k_neighbours, p=2)

        # Calculate weights (inverse of distance, raised to the power)
        valid_mask = np.isfinite(dist)
        valid_weights = np.zeros_like(dist)
        valid_weights[valid_mask] = 1 / dist[valid_mask] ** power

        # Interpolate values (using weighted average of k nearest neighbors)
        weighted_values = valid_weights * values[idx]
        interpolated_values = np.sum(weighted_values, axis=1) / np.sum(valid_weights, axis=1)

        # Reshape the interpolated values back to grid format

        grid_values = interpolated_values.reshape((height, width))

        crs = data_gdf.crs  # CRS.from_epsg(4326)
        raster = ref_raster.rio_raster_from_array(grid_values)
        return raster
