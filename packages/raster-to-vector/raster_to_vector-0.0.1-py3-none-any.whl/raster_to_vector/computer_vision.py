import io, math, requests, numpy as np
from PIL import Image
from typing import Tuple, Callable, List
from rapidocr_onnxruntime import RapidOCR
from skimage import measure, filters
from skimage.morphology import binary_dilation, disk
from shapely.geometry import Polygon, Point

ocr = RapidOCR()


def ocr_xy_text(img) -> List[Tuple[float, float, str]]:
    results = ocr(img)[0] or []
    boxes = [
        (int(pos[0][0]), int(pos[0][1]), int(pos[2][0]), int(pos[2][1]), text)
        for pos, text, score in results
    ]
    points = [((x0 + x1) / 2, (y0 + y1) / 2, text) for x0, y0, x1, y1, text in boxes]
    return points


def lnglat_to_point(lng: float, lat: float, z: int) -> Tuple[float, float]:
    n = 2**z
    x = (lng + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x, y


def point_to_lnglat(x: float, y: float, z: int):
    n = 2**z
    lng = x / n * 360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lng, lat


def png_to_tile(png: Image.Image) -> np.ndarray:
    alpha = png.split()[-1]
    background = Image.new("RGB", png.size, (255, 255, 255))
    white_background = Image.composite(png, background, alpha).convert("L")
    mask = np.array(Image.eval(white_background, lambda x: 255 - x))
    return mask > filters.threshold_otsu(mask)


class GetTile:
    def __init__(self, url: str):
        self.cache = {}
        self.url = url

    def __call__(self, x, y, z):
        if (x, y, z) not in self.cache:
            url = self.url.format(x=x, y=y, z=z)
            png = Image.open(io.BytesIO(requests.get(url).content))
            self.cache[(x, y, z)] = png_to_tile(png)
        return self.cache.get((x, y, z))


def add_border(mask) -> np.ndarray:
    mask[:1, :] = 1
    mask[-1:, :] = 1
    mask[:, :1] = 1
    mask[:, -1:] = 1
    return mask


def remove_text(mask) -> np.ndarray:
    labeled = measure.label(mask)
    mask = np.zeros(mask.shape, dtype=bool)
    for region in measure.regionprops(labeled):
        if region.area < 256:
            continue
        mask[labeled == region.label] = 1
    return mask


def preview(bbox: Tuple[int, int, int, int], tile: np.ndarray):
    pass


def find_polygon_from_point(
    lng: float, lat: float, z: int, get_tile: Callable, preview=preview
) -> Polygon:
    x, y = lnglat_to_point(lng, lat, z)
    x, y = int(x), int(y)
    bbox = [x, y, x, y]
    for _ in range(8):
        prev = bbox.copy()
        mask = np.concatenate(
            [
                np.concatenate([get_tile(x, y, z) for y in range(bbox[1], bbox[3] + 1)])
                for x in range(bbox[0], bbox[2] + 1)
            ],
            axis=1,
        )
        preview(bbox, mask)
        mask = remove_text(mask)
        mask = binary_dilation(mask, disk(1))
        mask = add_border(mask)
        contours = measure.find_contours(mask)
        poly = Polygon()
        for contour in contours:
            poly = Polygon(
                [
                    point_to_lnglat(bbox[0] + px / 256, bbox[1] + py / 256, z)
                    for py, px in contour
                ]
            )
            if poly.contains(Point(lng, lat)):
                break
        miny, maxy, minx, maxx = (
            min(contour[:, 0]),
            max(contour[:, 0]),
            min(contour[:, 1]),
            max(contour[:, 1]),
        )
        if miny < 4:
            bbox[1] -= 1
        if maxy > mask.shape[0] - 4:
            bbox[3] += 1
        if minx < 4:
            bbox[0] -= 1
        if maxx > mask.shape[1] - 4:
            bbox[2] += 1
        if bbox == prev:
            return poly.simplify(1e-5)
    return Polygon()


def tile_xy_in_polygon(
    poly: Polygon, z: int
) -> Tuple[Tuple[int, int, int, int], List[Tuple[int, int]]]:
    l, t, r, b = poly.bounds
    l, t = lnglat_to_point(l, t, z)
    r, b = lnglat_to_point(r, b, z)
    bbox = (int(l), int(b), int(r), int(t))
    tiles = [
        (x, y)
        for x in range(bbox[0], bbox[2] + 1)
        for y in range(bbox[1], bbox[3] + 1)
        if poly.intersects(
            Polygon(
                [
                    point_to_lnglat(x, y, z),
                    point_to_lnglat(x + 1, y, z),
                    point_to_lnglat(x + 1, y + 1, z),
                    point_to_lnglat(x, y + 1, z),
                ]
            )
        )
    ]
    return bbox, tiles


def check_text(text: str) -> bool:
    return True


def find_text_in_area(
    bound: Polygon, z: int, get_tile: Callable, check_text=check_text, preview=preview
) -> Tuple[List[Point], List[Polygon]]:
    found, queue = [], []
    bbox, tiles = tile_xy_in_polygon(bound, z)
    mask = np.concatenate(
        [
            np.concatenate(
                [
                    (
                        get_tile(x, y, z)
                        if (x, y) in tiles
                        else np.zeros((256, 256), dtype=bool)
                    )
                    for y in range(bbox[1], bbox[3] + 1)
                ]
            )
            for x in range(bbox[0], bbox[2] + 1)
        ],
        axis=1,
    )
    preview(bbox, mask)
    xy_texts = ocr_xy_text(Image.fromarray(mask))
    point_texts = [
        (Point(point_to_lnglat(bbox[0] + px / 256, bbox[1] + py / 256, z)), text)
        for px, py, text in xy_texts
    ]
    mask = remove_text(mask)
    mask = binary_dilation(mask, disk(1))
    polys = [
        Polygon(
            [
                point_to_lnglat(bbox[0] + px / 256, bbox[1] + py / 256, z)
                for py, px in contour
            ]
        )
        for contour in measure.find_contours(mask)
    ]
    expanded_bound = bound.buffer(1e-3)
    for poly in polys:
        point, text = next(
            ((p, t) for p, t in point_texts if check_text(t) and poly.contains(p)),
            (None, None),
        )
        if bound.contains(point):
            found.append((point, text))
        elif expanded_bound.contains(poly):
            queue.append(poly)
    return found, sorted(queue, key=lambda x: x.area, reverse=True)


def find_polygon_in_area(
    bound: Polygon,
    get_tile: Callable,
    check_text=check_text,
    preview=preview,
    results=[],
    z=9,
    maxz=10,
) -> List[Tuple[Polygon, str]]:
    found, queue = find_text_in_area(
        bound=bound, z=z, get_tile=get_tile, check_text=check_text, preview=preview
    )
    for point, text in found:
        poly = find_polygon_from_point(
            lng=point.x, lat=point.y, z=z + 1, get_tile=get_tile, preview=preview
        ).simplify(1e-4)
        results.append((poly, text))
        print(text, "\n", poly.wkt)
    if z < maxz:
        for sub in queue:
            find_polygon_in_area(
                bound=sub,
                get_tile=get_tile,
                check_text=check_text,
                preview=preview,
                results=results,
                z=z + 1,
            )
    return results
