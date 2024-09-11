"""Mapchtete handling tiles."""

from __future__ import annotations

import logging
from functools import cached_property
from itertools import product

import numpy as np
from affine import Affine
from rasterio.enums import Resampling
from rasterio.features import rasterize, shapes
from rasterio.transform import from_bounds
from rasterio.warp import reproject
from shapely import clip_by_rect
from shapely.geometry import box, shape
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union
from tilematrix import Tile, TilePyramid
from tilematrix._conf import ROUND

logger = logging.getLogger(__name__)


class BufferedTilePyramid(TilePyramid):
    """
    A special tile pyramid with fixed pixelbuffer and metatiling.

    Parameters
    ----------
    pyramid_type : string
        pyramid projection type (``geodetic`` or ``mercator``)
    metatiling : integer
        metatile size (default: 1)
    pixelbuffer : integer
        buffer around tiles in pixel (default: 0)

    Attributes
    ----------
    tile_pyramid : ``TilePyramid``
        underlying ``TilePyramid``
    metatiling : integer
        metatile size
    pixelbuffer : integer
        tile buffer size in pixels
    """

    def __init__(self, grid=None, metatiling=1, tile_size=256, pixelbuffer=0):
        """Initialize."""
        TilePyramid.__init__(self, grid, metatiling=metatiling, tile_size=tile_size)
        self.tile_pyramid = TilePyramid(
            grid, metatiling=metatiling, tile_size=tile_size
        )
        self.metatiling = metatiling
        if isinstance(pixelbuffer, int) and pixelbuffer >= 0:
            self.pixelbuffer = pixelbuffer
        else:  # pragma: no cover
            raise ValueError("pixelbuffer has to be a non-negative int")

    def tile(self, zoom, row, col):
        """
        Return ``BufferedTile`` object of this ``BufferedTilePyramid``.

        Parameters
        ----------
        zoom : integer
            zoom level
        row : integer
            tile matrix row
        col : integer
            tile matrix column

        Returns
        -------
        buffered tile : ``BufferedTile``
        """
        tile = self.tile_pyramid.tile(zoom, row, col)
        return BufferedTile(tile, pixelbuffer=self.pixelbuffer)

    def tiles_from_bounds(self, bounds=None, zoom=None, batch_by=None):
        """
        Return all tiles intersecting with bounds.

        Bounds values will be cleaned if they cross the antimeridian or are
        outside of the Northern or Southern tile pyramid bounds.

        Parameters
        ----------
        bounds : tuple
            (left, bottom, right, top) bounding values in tile pyramid CRS
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        batch_by = "column" if batch_by == "col" else batch_by
        yield from self.tiles_from_bbox(box(*bounds), zoom=zoom, batch_by=batch_by)

    def tiles_from_bbox(self, geometry, zoom=None, batch_by=None):
        """
        All metatiles intersecting with given bounding box.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : generator
            generates ``BufferedTiles``
        """
        batch_by = "column" if batch_by == "col" else batch_by
        if batch_by:  # pragma: no cover
            for batch in self.tile_pyramid.tiles_from_bbox(
                geometry, zoom=zoom, batch_by=batch_by
            ):
                yield (self.tile(*tile.id) for tile in batch)
        else:
            for tile in self.tile_pyramid.tiles_from_bbox(geometry, zoom=zoom):
                yield self.tile(*tile.id)

    def tiles_from_geom(self, geometry, zoom=None, batch_by=None, exact=False):
        """
        Return all tiles intersecting with input geometry.

        Parameters
        ----------
        geometry : ``shapely.geometry``
        zoom : integer
            zoom level

        Yields
        ------
        intersecting tiles : ``BufferedTile``
        """
        batch_by = "column" if batch_by == "col" else batch_by
        if batch_by:
            for batch in self.tile_pyramid.tiles_from_geom(
                geometry, zoom=zoom, batch_by=batch_by, exact=exact
            ):
                yield (self.tile(*tile.id) for tile in batch)
        else:
            for tile in self.tile_pyramid.tiles_from_geom(
                geometry, zoom=zoom, batch_by=batch_by, exact=exact
            ):
                yield self.tile(*tile.id)

    def intersecting(self, tile):
        """
        Return all BufferedTiles intersecting with tile.

        Parameters
        ----------
        tile : ``BufferedTile``
            another tile
        """
        return [
            self.tile(*intersecting_tile.id)
            for intersecting_tile in self.tile_pyramid.intersecting(tile)
        ]

    def matrix_affine(self, zoom):
        """
        Return Affine object for zoom level assuming tiles are cells.

        Parameters
        ----------
        zoom : integer
            zoom level
        """
        if self.pixelbuffer:  # pragma: no cover
            raise ValueError(
                "Matrix Affine can only be created for pyramid without pixelbuffer."
            )
        return Affine(
            round(self.x_size / self.matrix_width(zoom), ROUND),
            0,
            self.bounds.left,
            0,
            -round(self.y_size / self.matrix_height(zoom), ROUND),
            self.bounds.top,
        )

    def to_dict(self):
        """
        Return dictionary representation of pyramid parameters.
        """
        return dict(
            grid=self.grid.to_dict(),
            metatiling=self.metatiling,
            tile_size=self.tile_size,
            pixelbuffer=self.pixelbuffer,
        )

    def without_pixelbuffer(self) -> BufferedTilePyramid:
        config_dict = self.to_dict()
        config_dict.update(pixelbuffer=0)
        return BufferedTilePyramid(**config_dict)

    @staticmethod
    def from_dict(config_dict):
        """
        Initialize TilePyramid from configuration dictionary.
        """
        return BufferedTilePyramid(**config_dict)

    def __repr__(self):
        return (
            "BufferedTilePyramid(%s, tile_size=%s, metatiling=%s, pixelbuffer=%s)"
            % (self.grid, self.tile_size, self.metatiling, self.pixelbuffer)
        )


class BufferedTile(Tile):
    """
    A special tile with fixed pixelbuffer.

    Parameters
    ----------
    tile : ``Tile``
    pixelbuffer : integer
        tile buffer in pixels

    Attributes
    ----------
    height : integer
        tile height in pixels
    width : integer
        tile width in pixels
    shape : tuple
        tile width and height in pixels
    affine : ``Affine``
        ``Affine`` object describing tile extent and pixel size
    bounds : tuple
        left, bottom, right, top values of tile boundaries
    bbox : ``shapely.geometry``
        tile bounding box as shapely geometry
    pixelbuffer : integer
        pixelbuffer used to create tile
    profile : dictionary
        rasterio metadata profile
    """

    def __init__(self, tile, pixelbuffer=0):
        """Initialize."""
        if isinstance(tile, BufferedTile):
            tile = TilePyramid(
                tile.tp.grid, tile_size=tile.tp.tile_size, metatiling=tile.tp.metatiling
            ).tile(*tile.id)
        Tile.__init__(self, tile.tile_pyramid, tile.zoom, tile.row, tile.col)
        self._tile = tile
        self.pixelbuffer = pixelbuffer
        self.buffered_tp = BufferedTilePyramid(
            tile.tp.to_dict(), pixelbuffer=pixelbuffer
        )

    @cached_property
    def left(self):
        return self.bounds.left

    @cached_property
    def bottom(self):
        return self.bounds.bottom

    @cached_property
    def right(self):
        return self.bounds.right

    @cached_property
    def top(self):
        return self.bounds.top

    @cached_property
    def height(self):
        """Return buffered height."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer).height

    @cached_property
    def width(self):
        """Return buffered width."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer).width

    @cached_property
    def shape(self):
        """Return buffered shape."""
        return self._tile.shape(pixelbuffer=self.pixelbuffer)

    @cached_property
    def affine(self):
        """Return buffered Affine."""
        return self._tile.affine(pixelbuffer=self.pixelbuffer)

    @cached_property
    def transform(self):
        """Return buffered Affine."""
        return self._tile.affine(pixelbuffer=self.pixelbuffer)

    @cached_property
    def bounds(self):
        """Return buffered bounds."""
        return self._tile.bounds(pixelbuffer=self.pixelbuffer)

    @cached_property
    def bbox(self):
        """Return buffered bounding box."""
        return self._tile.bbox(pixelbuffer=self.pixelbuffer)

    def get_children(self):
        """
        Get tile children (intersecting tiles in next zoom level).

        Returns
        -------
        children : list
            a list of ``BufferedTiles``
        """
        return [BufferedTile(t, self.pixelbuffer) for t in self._tile.get_children()]

    def get_parent(self):
        """
        Get tile parent (intersecting tile in previous zoom level).

        Returns
        -------
        parent : ``BufferedTile``
        """
        return BufferedTile(self._tile.get_parent(), self.pixelbuffer)

    def get_neighbors(self, connectedness=8):
        """
        Return tile neighbors.

        Tile neighbors are unique, i.e. in some edge cases, where both the left
        and right neighbor wrapped around the antimeridian is the same. Also,
        neighbors ouside the northern and southern TilePyramid boundaries are
        excluded, because they are invalid.

        # -------------
        # | 8 | 1 | 5 |
        # -------------
        # | 4 | x | 2 |
        # -------------
        # | 7 | 3 | 6 |
        # -------------

        Parameters
        ----------
        connectedness : int
            [4 or 8] return four direct neighbors or all eight.

        Returns
        -------
        list of BufferedTiles
        """
        return [
            BufferedTile(t, self.pixelbuffer)
            for t in self._tile.get_neighbors(connectedness=connectedness)
        ]

    def is_on_edge(self):
        """Determine whether tile touches or goes over pyramid edge."""
        return (
            self.left <= self.tile_pyramid.left
            or self.bottom <= self.tile_pyramid.bottom  # touches_left
            or self.right >= self.tile_pyramid.right  # touches_bottom
            or self.top >= self.tile_pyramid.top  # touches_right  # touches_top
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.pixelbuffer == other.pixelbuffer
            and self.buffered_tp == other.buffered_tp
            and self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"BufferedTile(zoom={self.zoom}, row={self.row}, col={self.col})"

    def __hash__(self):
        return hash(repr(self))


def count_tiles(
    geometry, pyramid, minzoom, maxzoom, init_zoom=0, rasterize_threshold=0
):
    """
    Count number of tiles intersecting with geometry.

    Parameters
    ----------
    geometry : shapely geometry
    pyramid : TilePyramid
    minzoom : int
    maxzoom : int
    init_zoom : int

    Returns
    -------
    number of tiles
    """
    if not 0 <= init_zoom <= minzoom <= maxzoom:  # pragma: no cover
        raise ValueError("invalid zoom levels given")
    # tile buffers are not being taken into account
    unbuffered_pyramid = BufferedTilePyramid(
        pyramid.grid, tile_size=pyramid.tile_size, metatiling=pyramid.metatiling
    )
    height = pyramid.matrix_height(init_zoom)
    width = pyramid.matrix_width(init_zoom)
    # rasterize to array and count cells if too many tiles are expected
    if width > rasterize_threshold or height > rasterize_threshold:
        logger.debug("rasterize tiles to count geometry overlap")
        return _count_cells(unbuffered_pyramid, geometry, minzoom, maxzoom)

    logger.debug("count tiles using tile logic")
    return _count_tiles(
        [
            unbuffered_pyramid.tile(*tile_id)
            for tile_id in product(
                [init_zoom],
                range(pyramid.matrix_height(init_zoom)),
                range(pyramid.matrix_width(init_zoom)),
            )
        ],
        geometry,
        minzoom,
        maxzoom,
    )


def _count_tiles(tiles, geometry, minzoom, maxzoom):
    count = 0
    for tile in tiles:
        # determine data covered by tile
        tile_intersection = geometry.intersection(tile.bbox)

        # skip if there is no intersection
        if not tile_intersection.area:
            continue

        # increase counter as tile contains data
        if tile.zoom >= minzoom:
            count += 1

        # if there are further zoom levels, analyze descendants
        if tile.zoom < maxzoom:
            # if tile is half full, analyze each descendant
            # also do this if the tile children are not four in which case we cannot use
            # the count formula below
            if tile_intersection.area < tile.bbox.area or len(tile.get_children()) != 4:
                count += _count_tiles(
                    tile.get_children(), tile_intersection, minzoom, maxzoom
                )

            # if tile is full, all of its descendants will be full as well
            else:
                # sum up tiles for each remaining zoom level
                count += sum(
                    [
                        4**z
                        for z in range(
                            # only count zoom levels which are greater than minzoom or
                            # count all zoom levels from tile zoom level to maxzoom
                            minzoom - tile.zoom if tile.zoom < minzoom else 1,
                            maxzoom - tile.zoom + 1,
                        )
                    ]
                )

    return count


def _count_cells(pyramid, geometry, minzoom, maxzoom):
    if geometry.is_empty:  # pragma: no cover
        return 0

    # for the rasterization algorithm we need to keep the all_touched flag True
    # but slightly reduce the geometry area in order to get the same results as
    # with the tiles/vector algorithm.
    left, bottom, right, top = geometry.bounds
    width = right - left
    height = top - bottom
    buffer_distance = ((width + height) / 2) * -0.0000001
    # geometry will be reduced by a tiny fraction of the average from bounds width & height
    geometry_reduced = geometry.buffer(buffer_distance)

    logger.debug(
        "rasterize polygon on %s x %s cells",
        pyramid.matrix_height(maxzoom),
        pyramid.matrix_width(maxzoom),
    )
    transform = pyramid.matrix_affine(maxzoom)
    raster = rasterize(
        [(geometry_reduced, 1)],
        out_shape=(pyramid.matrix_height(maxzoom), pyramid.matrix_width(maxzoom)),
        fill=0,
        transform=transform,
        dtype=np.uint8,
        all_touched=True,
    )

    # count cells
    count = raster.sum()

    # resample raster up until minzoom using "max" resampling and count cells
    for zoom in reversed(range(minzoom, maxzoom)):
        raster, transform = reproject(
            raster,
            np.zeros(
                (pyramid.matrix_height(zoom), pyramid.matrix_width(zoom)),
                dtype=np.uint8,
            ),
            src_transform=transform,
            src_crs=pyramid.crs,
            dst_transform=pyramid.matrix_affine(zoom),
            dst_crs=pyramid.crs,
            resampling=Resampling.max,
        )
        count += raster.sum()

    # return cell sum
    return int(count)


def snap_geometry_to_tiles(
    geometry: BaseGeometry, pyramid: BufferedTilePyramid, zoom: int
) -> BaseGeometry:
    if geometry.is_empty:
        return geometry
    # calculate everything using an unbuffered pyramid, because otherwise the Affine
    # object cannot be calculated
    unbuffered_pyramid = BufferedTilePyramid.from_dict(
        dict(pyramid.to_dict(), pixelbuffer=0)
    )

    # use subset because otherwise memory usage can crash the program
    left, bottom, right, top = geometry.bounds
    # clip geometry bounds to pyramid bounds
    left = max([left, unbuffered_pyramid.bounds.left])
    bottom = max([bottom, unbuffered_pyramid.bounds.bottom])
    right = min([right, unbuffered_pyramid.bounds.right])
    top = min([top, unbuffered_pyramid.bounds.top])
    lb_tile = unbuffered_pyramid.tile_from_xy(left, bottom, zoom, on_edge_use="rt")
    rt_tile = unbuffered_pyramid.tile_from_xy(right, top, zoom, on_edge_use="lb")
    snapped_left, snapped_south, snapped_east, snapped_north = (
        lb_tile.bounds.left,
        lb_tile.bounds.bottom,
        rt_tile.bounds.right,
        rt_tile.bounds.top,
    )
    width = abs(rt_tile.col - lb_tile.col) + 1
    height = abs(rt_tile.row - lb_tile.row) + 1
    out_shape = (height, width)
    transform = from_bounds(
        west=snapped_left,
        south=snapped_south,
        east=snapped_east,
        north=snapped_north,
        width=width,
        height=height,
    )
    raster = rasterize(
        [(geometry, 1)],
        out_shape=out_shape,
        fill=0,
        transform=transform,
        dtype=np.uint8,
        all_touched=True,
    )
    # recreate geometry again by extracting features from raster
    out_geom = unary_union(
        [
            shape(feature)
            for feature, _ in shapes(raster, mask=raster, transform=transform)
        ]
    )
    # if original pyramid contained a pixelbuffer, add it to the output geometry
    if pyramid.pixelbuffer:
        buffer_distance = pyramid.pixelbuffer * pyramid.pixel_x_size(zoom)
        return clip_by_rect(
            out_geom.buffer(buffer_distance, join_style="mitre"),
            pyramid.left - buffer_distance if pyramid.is_global else pyramid.left,
            pyramid.bottom,
            pyramid.right + buffer_distance if pyramid.is_global else pyramid.right,
            pyramid.top,
        )
    return out_geom
