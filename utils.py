import cv2

def apply_mosaic_to_head(image, xmin, ymin, xmax, ymax, mosaic_ratio=0.1):
    head_height = int((ymax - ymin) * 0.3)
    head_ymax = ymin + head_height
    head_region = image[ymin:head_ymax, xmin:xmax]

    if head_region.size == 0:
        return image

    small = cv2.resize(head_region, (max(1, int((xmax - xmin) * mosaic_ratio)), max(1, int(head_height * mosaic_ratio))), interpolation=cv2.INTER_LINEAR)
    mosaic = cv2.resize(small, (xmax - xmin, head_height), interpolation=cv2.INTER_NEAREST)

    image[ymin:head_ymax, xmin:xmax] = mosaic
    return image
