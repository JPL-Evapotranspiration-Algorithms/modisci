from os.path import join, abspath, dirname

import numpy as np
import rasters as rt

from modland import find_modland_tiles

def load_clumping_index(geometry: rt.RasterGeometry, resampling: str = "nearest") -> rt.Raster:
    tiles = find_modland_tiles(geometry.boundary_latlon.geometry)
    image = rt.Raster(np.full(geometry.shape, fill_value=np.nan, dtype=np.float32), geometry=geometry)

    for tile in tiles:
        filename = join(abspath(dirname(__file__)), f"{tile}.tif")
        tile_image = rt.Raster.open(filename)
        tile_image = rt.where(tile_image == 255, np.nan, tile_image).astype(np.float32)
        projected_tile_image = tile_image.to_geometry(target_geometry=geometry, resampling="nearest")
        image = rt.where(np.isnan(image), projected_tile_image, image)

    return image
