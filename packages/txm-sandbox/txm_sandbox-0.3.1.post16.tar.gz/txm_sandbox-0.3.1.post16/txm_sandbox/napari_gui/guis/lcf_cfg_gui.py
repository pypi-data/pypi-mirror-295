from pathlib import Path
from magicgui import widgets, magicgui


_XANES_RE_SPECTRA = []


def get_ref_spectra_choices(ComboBox):
    global _XANES_RE_SPECTRA
    return _XANES_RE_SPECTRA


class lcf_cfg_gui:
    def __init__(self, parent=None):
        self.parent_obj = parent
        self.ref_fn = widgets.FileEdit(
            mode="r",
            filter=(
                ("*.dat"),
                ("*.txt"),
                ("*.asc"),
            ),
            name="ref spec",
        )
        self.add_ref = widgets.PushButton(text="add spec", enabled=False)
        self.spec_table = self.save_items = widgets.Select(
            choices=get_ref_spectra_choices, name="ref spectra"
        )
        self.rm_ref = widgets.PushButton(text="remove spec", enabled=False)
        layout = widgets.VBox(
            widgets=[self.ref_fn, self.add_ref, self.spec_table, self.rm_ref]
        )
        self.gui = widgets.Dialog(
            widgets=[
                layout,
            ]
        )
        self.rtn = self.gui.exec()
