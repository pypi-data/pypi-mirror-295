from pathlib import Path

from bombcell.bombcell import write_bombcell_matlab_script
from pp_slurm import slurm_functions


def bombcell_slurm(s, overwrite=False):
    # This is a hack right now and passes the actually used command via the additional_string
    # command, the rest is more or less irrelevant.
    if not (s.kilosort_dir.parent / "bc_quality_metrics.m").exists() or overwrite:
        write_bombcell_matlab_script(s)
        kwarg_dict = {
            "slurm_batch": True,
            "logs_path": Path(f"{s.session_path_derivatives}") / "logs",
            "module_string": "matlab/R2022a",
            "additional_string": f'matlab -nodisplay -nosplash -nodesktop -r "run(\'{s.kilosort_dir.parent}/bc_quality_metrics.m\')"; exit;'
        }
        slurm_functions.run_bombcell_slurm(**kwarg_dict)
    else:
        print(f'session {s.session_path_derivatives} has been processed and overwrite set to: {overwrite}')
