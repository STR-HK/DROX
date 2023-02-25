from PIL import Image

def crop_image_by_aspect_ratio(
        imgpath,
        aspect_ratio = 1 / 1,
        width_base = True,
        height_base = False,
        vertical_align_top = False,
        vertical_align_middle = True,
        vertical_align_bottom = False,
        horizontal_align_left = False,
        horizontal_align_center = True,
        horizontal_align_right = False,
    ):

    img = Image.open(imgpath)
    width, height = img.size

    # if vertical_align_top:
