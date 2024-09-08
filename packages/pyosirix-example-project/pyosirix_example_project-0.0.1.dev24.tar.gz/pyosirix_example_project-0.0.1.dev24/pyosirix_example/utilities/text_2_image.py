from typing import Tuple

from PIL import Image, ImageDraw, ImageFont, ImageChops
import numpy as np
from numpy.typing import NDArray


class Text2Image:
    """ A class that creates a text image from a text string.

    Properties:
        max_shape (Tuple[int, int]): The maximum shape of the initial text image. Set to something
            large to avoid text clipping. Default is (5000, 5000).
    """

    def __init__(self, max_shape: Tuple[int, int] = None):
        if max_shape is None:
            max_shape = (5000, 5000)
        self.max_shape = max_shape

    @staticmethod
    def append_value_to_tuple(v, t: Tuple) -> Tuple:
        """ Appends a value to a tuple.

        Args:
            v: The value to append.
            t (Tuple): The tuple to append to.

        Returns:
            Tuple: The new tuple.
        """
        l = [x for x in t]
        l.append(v)
        return tuple(l)

    @staticmethod
    def pad_image(image: Image, pad: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> Image:
        """ Pad a Pillow image.

        Args:
            image (PIL.Image): Image to be padded.
            pad (Tuple[int, int, int, int]): Pad the image with this shape
                (left, right, top, bottom).

        Returns:
            PIL.Image: Padded image.
        """
        width, height = image.size
        left, right, top, bottom = pad
        new_width = width + left + right
        new_height = height + bottom + top
        new_image = Image.new(image.mode, (new_width, new_height))
        new_image.paste(image, (left, top))
        return new_image

    @staticmethod
    def trim_image(image: Image, bg_color: Tuple[int, int, int] = (0, 0, 0)) -> Image:
        """ Trim the border of a Pillow image.

        Args:
             image (PIL.Image): Image to be trimmed.
             bg_color (Tuple[int, int, int]): The background color of the image when in RGB mode.

        Returns:
            PIL.Image: Trimmed image.
        """
        if image.mode != 'RGB':
            zero_image = Image.new(image.mode, image.size)
        else:
            zero_image = Image.new(image.mode, image.size, bg_color)
        diff_image = ImageChops.difference(image, zero_image)
        bbox = diff_image.getbbox()
        if bbox:
            image = image.crop(bbox)
        return image

    @staticmethod
    def paste_image_in_image(image: Image, base_image: Image, mask_image: Image = None,
                             location: int = 1, scale: float = 0.2, offset: float = 0.05) -> Image:
        """ Paste one Pillow image in another.

        Args:
            image (Pillow.Image): The image to paste.
            base_image (Pillow.Image): Base image to paste within.
            mask_image (Pillow.Image): A binary mask for the image where zero-values will not be
                pasted. Default is None, in which case no masking will be applied.
            location (int): The location to paste the image:
                1: top-right (default)
                2: top-center
                3: top-left
                4: bottom-left
                5: bottom-center
                6: bottom-right
            scale (float): The proportion of `base_image` columns occupied by Image. Rows are
                automatically determined to ensure the aspect ratio of `image` is maintained.
                Must be > 0 and <= 1. Default is 0.2.
            offset (float): The amount to offset the image from the edge. Must be > 0 and < 1.

        Returns:
            Image: The pasted image.
        """
        if scale <= 0.0 or scale > 1.0:
            raise ValueError("Scale must be between 0 and 1.")

        if offset < 0.0 or offset > 1.0:
            raise ValueError("Offset must be between 0 and 1.")

        if mask_image is None:
            mask_image = Image.new("L", image.size, 255)

        columns, rows = image.size
        base_columns, base_rows = base_image.size

        # Calculate new rows/columns
        aspect_ratio = float(rows) / columns
        new_columns = int(scale * base_columns)
        new_rows = int(aspect_ratio * new_columns)

        # Determine the offset
        if location == 6:  # Bottom right
            offset_columns = base_columns - new_columns - int(offset * base_columns)
            offset_rows = base_rows - new_rows - int(offset * base_rows)
        elif location == 5:  # Bottom center
            offset_columns = int(base_columns / 2 - new_columns / 2)
            offset_rows = base_rows - new_rows - int(offset * base_rows)
        elif location == 4:  # Bottom left
            offset_columns = int(offset * base_columns)
            offset_rows = base_rows - new_rows - int(offset * base_rows)
        elif location == 3:  # Top left
            offset_columns = int(offset * base_columns)
            offset_rows = int(offset * base_rows)
        elif location == 2:  # Top center
            offset_columns = int(base_columns / 2 - new_columns / 2)
            offset_rows = int(offset * base_rows)
        elif location == 1:  # Top right
            offset_columns = base_columns - new_columns - int(offset * base_columns)
            offset_rows = int(offset * base_rows)
        else:
            raise ValueError("Location must be 1, 2, 3, 4, 5, 6")

        image_r = image.resize((new_columns, new_rows), Image.LANCZOS)
        mask_image_r = mask_image.resize((new_columns, new_rows), Image.NEAREST)
        base_image.paste(image_r, (offset_columns, offset_rows), mask_image_r)

        return base_image

    def paste_text_in_image(self, text: str, image: Image, location: int = 1, scale: float = 0.2,
                            offset: float = 0.05, remove_background: bool = False,
                            **kwargs) -> Image:
        """ Paste a text string within a Pillow image.

        Args:
            text (str): The text to be pasted.
            image (Pillow.Image): The image to be pasted.
            location (int): The text location (see `paste_image_in_image`).
            scale (float): The proportion of `base_image` columns occupied by the text
                (see `paste_image_in_image`).
            offset (float): The amount to offset the text from the edge
                (see `paste_image_in_image`).
            remove_background (bool): Whether to include the background. Default is False.
            kwargs (dict): Keyword arguments passed to `text_to_image`.

        Returns:
            Image: The pasted image.
        """
        kwargs["mode"] = image.mode  # Need to ensure it is correct.
        text_image = self.text_to_image(text, **kwargs)

        if remove_background:
            text_array = np.array(text_image)
            if image.mode == "F":
                if "bg_value" in kwargs:
                    bg_value = kwargs["bg_value"]
                else:
                    bg_value = 0
                mask_array = (text_array != bg_value) * 255
            else:
                if "bg_color" in kwargs:
                    bg_color = kwargs["bg_color"]
                else:
                    bg_color = (0, 0, 0)
                mask_array = 1 * (text_array[..., 0] != bg_color[0]) + \
                             1 * (text_array[..., 1] != bg_color[1]) + \
                             1 * (text_array[..., 2] != bg_color[2])
                mask_array = (mask_array > 0) * 255
            mask_image = Image.fromarray(mask_array.astype("uint8"), mode="L")
        else:
            mask_image = Image.new("L", image.size, 255)

        return self.paste_image_in_image(text_image,
                                         image,
                                         mask_image,
                                         location,
                                         scale,
                                         offset)

    def paste_text_in_array(self, text: str, array: NDArray, location: int = 1, scale: float = 0.2,
                            offset: float = 0.05, remove_background: bool = False,
                            **kwargs) -> NDArray:
        """ Paste a text string within a Numpy array.

        Args:
            text (str): The text to be pasted.
            array (NDArray): The array to be pasted.
            location (int): The text location (see `paste_image_in_image`).
            scale (float): The proportion of `base_image` columns occupied by the text
                (see `paste_image_in_image`).
            offset (float): The amount to offset the text from the edge
                (see `paste_image_in_image`).
            remove_background (bool): Whether to include the background. Default is False.
            kwargs (dict): Keyword arguments passed to `text_to_image`.

        Returns:
            NDArray: The pasted array.
        """
        if array.ndim == 3:
            if array.shape[-1] == 3:
                image = Image.fromarray(array, mode='RGB')
            elif array.shape[-1] == 4:
                image = Image.fromarray(array, mode='RGBA')
            else:
                ValueError("Last dimension of array must be 3 or 4.")
        elif array.ndim == 2:
            image = Image.fromarray(array.astype("float32"), mode='F')
        else:
            raise ValueError("Array must be 3 or 2 dimensional.")
        image = self.paste_text_in_image(text,
                                         image,
                                         location,
                                         scale,
                                         offset,
                                         remove_background,
                                         **kwargs)
        return np.array(image)

    def text_to_image(self, text: str, font_path: str = None, font_size: float = 40,
                      value: float = 1.0, color: Tuple[int, int, int] = (255, 255, 255),
                      bg_value: float = 0.0, bg_color: Tuple[int, int, int] = (255, 255, 255),
                      mode: str = "F", align: str = "left",
                      pad: Tuple[int, int, int, int] = (0, 0, 0, 0)) -> Image:
        """ Convert a text string into an image.

        Args:
            text (str): The text to be converted.
            font_path (str, optional): A path to a font file. Defaults to None in which case Arial
                is used.
            font_size (int, optional): A font size. Defaults to 40.
            value (float, optional): A value to use for the text if `mode` is greyscale.
                Defaults to 1.0.
            color (Tuple[int, int, int]): The color of the text if `mode` is rgb.
                Defaults to (255, 255, 255). Can be 4 elements if `mode` is RGBA, though not
                necessary.
            bg_value (float, optional): A value to use for the background if `mode` is greyscale.
                Defaults to 0.0.
            bg_color (Tuple[int, int, int]): The color of the background if `mode` is rgb.
                Defaults to (0, 0, 0). Can be 4 elements if `mode` is RGBA, though not necessary.
            mode (str, optional): One of "F" (greyscale), "RGB" or "RGBA". Default is "F".
            align (str, optional): One of "left", "center", or "right".
            pad (Tuple[int, int, int, int]): The pad size of the image (left, right, top, bottom).
                Defaults to (0, 0, 0, 0).

        Returns:
            PIL.Image: The text image.
        """
        if mode == "F":
            img = Image.new('L', self.max_shape, 0)
        elif mode == "RGB":
            color = color[0:3]  # Remove alpha if present.
            bg_color = bg_color[0:3]
            img = Image.new('RGB', self.max_shape, bg_color)
        elif mode == "RGBA":
            if len(color) == 3:
                color = self.append_value_to_tuple(255, color)  # Add alpha if not present.
            if len(bg_color) == 3:
                bg_color = self.append_value_to_tuple(255, bg_color)
            img = Image.new('RGB', self.max_shape, bg_color)
        else:
            raise ValueError("Mode must be F, RGB, or RGBA.")
        draw = ImageDraw.Draw(img)

        # Optional: Load a font, otherwise it will use the default font
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.truetype("Arial.ttf", font_size)

        # Add text to the image and trim
        if mode == "F":
            draw.multiline_text((0, 0), text, fill=255, font=font, anchor="la", align=align)
        else:
            draw.multiline_text((0, 0), text, fill=color, font=font, anchor="la", align=align)

        # Trim and pad the image
        img = self.trim_image(img, bg_color=bg_color)
        img = self.pad_image(img, pad)

        # Convert to float if greyscale
        if mode == "F":
            arr = np.array(img).astype("float32")
            arr = arr * value / 255
            arr[arr == 0] = bg_value
            img = Image.fromarray(arr, mode="F")

        # Return the binary image array
        return img
