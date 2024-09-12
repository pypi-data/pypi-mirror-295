from pp_slurm import slurm_functions
from pathlib import Path


def track_mouse_slurm(mtd, skip_video_processing=False):
    kwarg_dict = {
        "slurm_batch": True,
        "logs_path": Path(f"{mtd.mouse_dir}") / "logs",
        "mouse_id": f"{mtd.mouse_id}",
        "track": True,
        "overwrite": True,
        "video_file_name": "camera",
        "input_video_fmt": "avi",
        "output_video_fmt": "mp4",
        "label_video": False,
        "rawdata_dir": mtd.raw_mouse_dir.parent,
        "derivatives_dir": mtd.mouse_dir.parent,
        "module_string": "deeplabcut/2022-07-06",
        "additional_string": "export DLClight=True",
        "skip_video_processing": skip_video_processing,
    }
    slurm_functions.run_dlc_tracking_slurm(**kwarg_dict)
