from pathlib import Path

import tifffile
from magicgui import widgets
from ..utils.misc import (
    set_data_widget,
    overlap_roi,
    update_layer_in_viewer,
    show_layers_in_viewer,
)


def show_io_win(dtype="APS_tomo"):
    if dtype == "APS_tomo":
        vals = widgets.request_values(
            name={
                "annotation": Path,
                "label": "pick a tomo file",
                "options": {"mode": "r", "filter": "tomo data file (*.h5)"},
            },
            title="pick a tomo file from 3D XANES data series",
        )
        return vals


def mk_aps_cfg(fn_tplt, cfg, dtype="APS 3D XANES"):
    if dtype == "APS 3D XANES":
        tem = (
            cfg["io_data_structure_tomo"]["tomo_raw_fn_template"]
            .replace("{0}", fn_tplt)
            .replace("{1}", "{0}")
        )
        cfg["io_data_structure_tomo"]["tomo_raw_fn_template"] = tem
        cfg["io_data_structure_xanes3D"]["tomo_raw_fn_template"] = tem
        cfg["io_data_structure_xanes3D"]["xanes3D_recon_dir_template"] = "recon_" + str(
            Path(tem).stem
        )
        cfg["io_data_structure_xanes3D"]["xanes3D_recon_fn_template"] = (
            "recon_" + str(Path(tem).stem) + "_{1}.tiff"
        )
    elif dtype == "APS 2D XANES":
        # APS 2D XANES data files are saved in the same manner as APS 3D XANES; the naming schemes
        # in both 2D XANES and 3D XANES are same
        tem = (
            cfg["io_data_structure_xanes2D"]["xanes2D_raw_fn_template"]
            .replace("{0}", fn_tplt)
            .replace("{1}", "{0}")
        )
        cfg["io_data_structure_xanes2D"]["xanes2D_raw_fn_template"] = tem
    return cfg


_XANES_RE_SPECTRA = []


def get_ref_spectra_choices(ComboBox):
    global _XANES_RE_SPECTRA
    return _XANES_RE_SPECTRA


class lcf_cfg_gui:
    def __init__(self, parent=None):
        self.parent_obj = parent
        self._ref_dict = {}

        self.ref_fn = widgets.FileEdit(
            mode="r",
            filter="(*.dat);;(*.txt);;(*.asc)",
            name="ref spec",
        )
        self.ref_spec_name = widgets.LineEdit(
            value="", label="spec name", enabled=False
        )
        self.add_ref = widgets.PushButton(text="add spec", enabled=False)
        self.spec_table = self.save_items = widgets.Select(
            choices=get_ref_spectra_choices, name="ref spectra"
        )
        self.rm_ref = widgets.PushButton(text="remove spec", enabled=False)
        layout = widgets.VBox(
            widgets=[
                self.ref_fn,
                self.ref_spec_name,
                self.add_ref,
                self.spec_table,
                self.rm_ref,
            ]
        )
        self.gui = widgets.Dialog(
            widgets=[
                layout,
            ]
        )

        self.ref_fn.changed.connect(self._ref_fn)
        self.add_ref.changed.connect(self._add_ref)
        self.rm_ref.changed.connect(self._rm_ref)

        self.rtn = self.gui.exec()

    def _ref_fn(self):
        if (self.ref_fn.value is None) or (not self.ref_fn.value.exists()):
            self.ref_spec_name.enabled = False
            self.add_ref.enabled = False
            self.rm_ref.enabled = False
            self.spec_table.enabled = False
        else:
            self.ref_spec_name.enabled = True
            self.add_ref.enabled = True
            self.rm_ref.enabled = True
            self.spec_table.enabled = True

    def _add_ref(self):
        if (self.ref_fn.value is None) or (not self.ref_fn.value.exists()):
            pass
        else:
            n_refs = len(list(self._ref_dict.keys()))
            if not self.ref_spec_name.value:
                name = f"ref_{len(list(self._ref_dict.keys())) + 1}"
            else:
                name = self.ref_spec_name.value
            self._ref_dict[name] = {"path": self.ref_fn.value}
            tem = list(self.spec_table.choices)
            tem.append(name)
            global _XANES_RE_SPECTRA
            _XANES_RE_SPECTRA = list(set(tem))
            self.spec_table.reset_choices()

    def _rm_ref(self):
        global _XANES_RE_SPECTRA
        _XANES_RE_SPECTRA = list(self.spec_table.choices)
        tem = self.spec_table.value
        print(tem)
        for ii in tem:
            _XANES_RE_SPECTRA.remove(ii)
            self._ref_dict.pop(ii)
        self.spec_table.reset_choices()


class opt_reg_roi_gui:
    def __init__(self, parent=None):
        self.parent_obj = parent
        self.opt_reg_roix = widgets.RangeSlider(
            name="reg roi x", value=[540, 740], enabled=True
        )
        self.opt_reg_roiy = widgets.RangeSlider(
            name="reg roi y", value=[540, 740], enabled=True
        )
        self.opt_reg_ref_sli = widgets.Slider(
            name="reg ref sli", value=540, enabled=True
        )

        if self.parent_obj._3dxanes_opt_reg_roi_old_val is None:
            set_data_widget(
                self.opt_reg_ref_sli,
                0,
                self.parent_obj.ref_sli.value,
                self.parent_obj.ref_sli.max,
            )
            set_data_widget(
                self.opt_reg_roix,
                0,
                list(self.parent_obj.auto_cen_roix.value),
                self.parent_obj.auto_cen_roix.max,
            )
            set_data_widget(
                self.opt_reg_roiy,
                0,
                list(self.parent_obj.auto_cen_roiy.value),
                self.parent_obj.auto_cen_roiy.max,
            )
        else:
            set_data_widget(
                self.opt_reg_ref_sli,
                self.parent_obj.rec_roiz.value[0],
                self.parent_obj._3dxanes_opt_reg_roi_old_val[4],
                self.parent_obj.rec_roiz.value[1],
            )
            set_data_widget(
                self.opt_reg_roix,
                0,
                list(self.parent_obj._3dxanes_opt_reg_roi_old_val[2:4]),
                self.parent_obj.auto_cen_roix.max,
            )
            set_data_widget(
                self.opt_reg_roiy,
                0,
                list(self.parent_obj._3dxanes_opt_reg_roi_old_val[0:2]),
                self.parent_obj.auto_cen_roiy.max,
            )

        layout = widgets.VBox(
            widgets=[self.opt_reg_roix, self.opt_reg_roiy, self.opt_reg_ref_sli]
        )
        self.gui = widgets.Dialog(
            widgets=[
                layout,
            ],
        )

        self.opt_reg_roix.changed.connect(self._opt_reg_roix)
        self.opt_reg_roiy.changed.connect(self._opt_reg_roiy)
        self.opt_reg_ref_sli.changed.connect(self._opt_reg_ref_sli)

        self.rtn = self.gui.exec()

    def __show_roi(self):
        if (self.parent_obj.rec_fntpl is not None) and (
            Path(
                str(self.parent_obj.rec_fntpl).format(
                    self.parent_obj.ref_scan_id.value,
                    str(self.opt_reg_ref_sli.value).zfill(5),
                )
            ).exists()
        ):
            overlap_roi(self.parent_obj.viewer, self, mode="ext_reg_roi")
            show_layers_in_viewer(
                self.parent_obj.viewer, ["xanes_raw_viewer", "ext_reg_roi"]
            )

    def _opt_reg_roix(self):
        self.__show_roi()

    def _opt_reg_roiy(self):
        self.__show_roi()

    def _opt_reg_ref_sli(self):
        sta = False
        try:
            update_layer_in_viewer(
                self.parent_obj.viewer,
                tifffile.imread(
                    str(self.parent_obj.rec_fntpl).format(
                        self.parent_obj.ref_scan_id.value,
                        str(self.opt_reg_ref_sli.value).zfill(5),
                    )
                ),
                "xanes_raw_viewer",
            )
            sta = True
        except Exception as e:
            self.op_status.value = (
                "Something is wrong. Please check terminal for more information."
            )
            print(f"{str(e)=}")
            sta = False

        if sta:
            self.__show_roi()
            rng = (
                self.parent_obj.viewer.layers["xanes_raw_viewer"].data.max()
                - self.parent_obj.viewer.layers["xanes_raw_viewer"].data.min()
            )
            self.parent_obj.viewer.layers["xanes_raw_viewer"].contrast_limits = [
                self.parent_obj.viewer.layers["xanes_raw_viewer"].data.min()
                + 0.1 * rng,
                self.parent_obj.viewer.layers["xanes_raw_viewer"].data.max()
                - 0.1 * rng,
            ]
            self.parent_obj.viewer.reset_view()


class ext_reg_params_gui:
    def __init__(self, parent=None):
        self.parent_obj = parent
        self.smth_krnl = widgets.LineEdit(
            value=self.parent_obj._reg_smth_krnl, label="smth krnl", enabled=True
        )
        self.chnk_sz = widgets.LineEdit(
            value=self.parent_obj._reg_chnk_sz, label="chunk size", enabled=True
        )
        layout = widgets.VBox(widgets=[self.smth_krnl, self.chnk_sz])
        self.gui = widgets.Dialog(
            widgets=[
                layout,
            ]
        )
        self.rtn = self.gui.exec()

    @property
    def smth_krnl_val(self):
        return float(self.smth_krnl.value)

    @smth_krnl_val.setter
    def smth_krnl_val(self):
        try:
            float(self.smth_krnl.value)
        except:
            self.smth_krnl.value = 1

        if float(self.smth_krnl.value) <= 0:
            self.smth_krnl.value = 1
        elif float(self.smth_krnl.value) > 5:
            self.smth_krnl.value = 5

    @property
    def chnk_sz_val(self):
        return int(self.chnk_sz.value)

    @chnk_sz_val.setter
    def chnk_sz_val(self):
        try:
            int(self.chnk_sz.value)
        except:
            self.chnk_sz.value = 5

        if int(self.chnk_sz.value) <= 0:
            self.chnk_sz.value = 5
        elif int(self.chnk_sz.value) > 20:
            self.chnk_sz.value = 20
