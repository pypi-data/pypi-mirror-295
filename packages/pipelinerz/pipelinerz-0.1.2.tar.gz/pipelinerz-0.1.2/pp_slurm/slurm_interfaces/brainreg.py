from pp_slurm import slurm_functions
from pathlib import Path

from breg_util.brainreg_command_line_util import brainreg_command


def brainreg_slurm(mtd, additional=None):
    # This is a hack right now and passes the actually used command via the additional_string
    # command, the rest is more or less irrelevant.
    kwarg_dict = {
        "slurm_batch": True,
        "logs_path": Path(f"{mtd.mouse_dir}") / "logs",
        "mouse_id": f"{mtd.mouse_id}",
        "mouse_dir": f"{mtd.mouse_dir}",
        "root_dir": f"{mtd.root}",
        "function": "brainreg",
        "atlas": "kim_mouse_10um",
        "module_string": "brainglobe",
        "additional_string": brainreg_command(mtd.mouse_id,
                                              mtd.mouse_dir,
                                              mtd.root,
                                              mtd.serial2p_dir,
                                              function="brainreg",
                                              atlas="kim_mouse_10um",
                                              additional=additional),
    }
    slurm_functions.run_brainreg_slurm(**kwarg_dict)
