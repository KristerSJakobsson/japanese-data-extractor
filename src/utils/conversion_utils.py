from src.utils.number_conversion_utils import western_style_kanji_to_value
from src.extractor.models.PostalCode import PostalCode

HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000

FULL2HALF = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
FULL2HALF[0x3000] = 0x20

POSTAL_CODE_JAPANESE_SEPARATORS = ["の", "ノ", "之", "ﾉ"]


def full_width_string_to_half_width(full_width_string: str) -> str:
    """
    Convert full-width characters to half-width counterpart
    :param full_width_string: Some full-width string
    :return: Corresponding half-width string
    """
    return full_width_string.translate(FULL2HALF)


def half_width_string_to_full_width(half_width_string: str) -> str:
    """
    Convert half-width characters to full-width counterpart
    :param half_width_string: Some half-width string
    :return: Corresponding full-width string
    """
    return half_width_string.translate(HALF2FULL)


def parse_postal_code(postal_code: str) -> PostalCode:
    """
    Function used to convert postal code to default model
    :param postal_code: Some postal code, possibly formatted with kanji or full-width numbers
    :return: Correctly formatted postal code nnn-nnnn
    """
    converted_code = ""
    for japanese_separator in POSTAL_CODE_JAPANESE_SEPARATORS:
        if japanese_separator in postal_code:
            # Assume it's a japanese number
            pieces = postal_code.split(japanese_separator)
            converted_code = f"{western_style_kanji_to_value(pieces[0])}{western_style_kanji_to_value(pieces[1])}"
            break
    else:
        # Assume it's not a japanese number, contains only numbers and seperator
        for char in postal_code:
            if char.isnumeric():
                # Conversion turns full-width characters to half-width
                converted_code = converted_code + full_width_string_to_half_width(char)

    return PostalCode.from_string(postal_code=converted_code)
