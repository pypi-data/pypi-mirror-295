import fire
from magicgui import magicgui
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
from pathlib import Path
import warnings

from looming_spots.db.loom_trial_group import MouseLoomTrialGroup
from daq_loader.load import sync_raw_and_processed_data
from pp_slurm.slurm_interfaces.bombcell import bombcell_slurm
from pp_slurm.slurm_interfaces.brainreg import brainreg_slurm
from xpmtd.sorting_metadata import SortingMetadata
from pp_slurm.slurm_interfaces.sort import run_full_sorting_pipeline_on_mouse
from probe_loader.load_probe import extract_all_sync_channels
from pp_slurm.slurm_interfaces.track_mouse_dlc import track_mouse_slurm


def bombcell_all_sessions(mtd, overwrite=False):
    for s in mtd.sessions:
        if s.kilosort_dir:
            bombcell_slurm(s, overwrite)


@magicgui(
    rawdata_directory={"mode": "d"},
    derivatives_directory={"mode": "d"},
    mouse_ids={"widget_type": "Select", "choices": [], "allow_multiple": True},  # Multi-select
)
def pipeline_widget(
                    rawdata_directory=Path("/ceph/margrie/slenzi/2024/SC/rawdata/"),
                    derivatives_directory=Path("/ceph/margrie/slenzi/2024/SC/derivatives/"),
                    mouse_ids=[],
                    brainreg: bool = True,
                    behaviour: bool = True,
                    spikesorting: bool = True,
                    bombcell: bool = True,
                    tracking: bool = True,
):
    print(f"The following mouse IDs will now be analysed: {mouse_ids}")
    for mouse_id in mouse_ids:
        print(f"Processing mouse ID: {mouse_id}")

        mtd = SortingMetadata(mouse_id, root=derivatives_directory)
        if not mtd.mouse_dir.exists():
            warnings.warn("mouse directory not found")
            raise ValueError

        print("syncing data...")
        sync_raw_and_processed_data(mouse_id=mtd.mouse_id,
                                    raw_directory=rawdata_directory,
                                    processed_directory=derivatives_directory)

        if brainreg:
            print("brainreg job setup...")
            brainreg_slurm(mtd)

        if behaviour:
            print("processing behaviour nidaq data...")
            mtg = MouseLoomTrialGroup(mouse_id, processed_data_dir=derivatives_directory)

            print("extract sync channels...")
            extract_all_sync_channels(mtd)

        if tracking:
            print("tracking job setup...")
            track_mouse_slurm(mtd)

        if spikesorting:
            print("sorting job setup...")
            run_full_sorting_pipeline_on_mouse(mtd)

        if bombcell:
            print("running bombcell...")
            bombcell_slurm(mtd.sessions[-1], overwrite=True)
            bombcell_all_sessions(mtd, overwrite=True)


def load_experiment_directories(event=None):
    p = pipeline_widget.rawdata_directory.value
    if p is None:
        print("No directory selected")
        return
    paths = list(Path(p).glob("*"))
    mouse_ids = [path.stem for path in paths if path.is_dir()]
    print("Mouse IDs:", mouse_ids)
    pipeline_widget.mouse_ids.choices = mouse_ids  # Update choices with mouse IDs


pipeline_widget.rawdata_directory.changed.connect(load_experiment_directories)


def pipelinerz_gui():
    app = QApplication([])
    widget = pipeline_widget
    main_window = QWidget()

    layout = QVBoxLayout()
    layout.addWidget(widget.native)

    main_window.setLayout(layout)
    main_window.setWindowTitle("Pipeline Widget")
    main_window.show()

    app.exec_()


def main():
    fire.Fire(pipelinerz_gui())


if __name__ == "__main__":
    main()
