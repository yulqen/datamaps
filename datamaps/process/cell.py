from typing import Any, Union


class Cell:
    """
    Purpose of the Cell object is to hold data about a spreadsheet cell.
    They are used to populate a datamap cell_map and to write out data to
    a template.
    """
    def __init__(self,
                 cell_key: str,
                 cell_value: Any,
                 cell_reference: str,
                 template_sheet: str,
                 bg_colour: Union[str, None],
                 fg_colour: Union[str, None],
                 number_format: Union[str, None],
                 verification_list: Union[str, None],
                 r_idx: int=None,
                 c_idx: int=None
                 ) -> None:
        if cell_value:
            self.cell_value = cell_value
        else:
            self.cell_value = None
        self.cell_key = cell_key
        self.cell_reference = cell_reference
        self.template_sheet = template_sheet
        self.bg_colour = bg_colour
        self.fg_colour = fg_colour
        self.number_format = number_format
        self.verification_list = verification_list
        self.r_idx = r_idx
        self.c_idx = c_idx

    def __repr__(self) -> str:
        return ("<Cell: cell_key: {} cell_value: {} cell_reference: {} "
                "template_sheet: {}>".format(
                    self.cell_key,
                    self.cell_value,
                    self.cell_reference,
                    self.template_sheet))
