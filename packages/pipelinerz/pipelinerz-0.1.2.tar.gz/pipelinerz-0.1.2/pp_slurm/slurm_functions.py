from pp_slurm.slurm import run_job


def run_dlc_tracking_slurm(**kwargs) -> None:
    """
    Run the entire DLC pipeline in a SLURM job.

    Parameters
    ----------
    kwargs : Dict
        Keyword arguments passed to
        looming_spots.tracking_dlc.track_mouse.process_behaviour

    Notes
    -----
    The import must occur here to avoid recursive imports.
    """
    from lmtracker.track_mouse import process_behaviour

    run_job(kwargs, process_behaviour, "Track Mouse DLC")


def run_sorting_slurm(**kwargs) -> None:
    """
    Run the swc_ephys sorting pipeline from within a SLURM job.

    Notes
    -----
    The import must occur here to avoid recursive imports.
    """
    from ..pipeline.sort import run_sorting

    run_job(kwargs, run_sorting, "Sorting")


def run_brainreg_slurm(**kwargs) -> None:
    """
    Run brainreg in a SLURM job.

    Parameters
    ----------
    kwargs : Dict
        Keyword arguments passed to
        looming_spots.tracking_dlc.track_mouse.process_behaviour

    Notes
    -----
    The import must occur here to avoid recursive imports.
    """
    from breg_util.brainreg_command_line_util import brainreg_commandline

    run_job(kwargs, brainreg_commandline, "register brain to atlas")


def run_bombcell_slurm(**kwargs) -> None:
    """
    Run bombcell in a SLURM job.

    Parameters
    ----------
    kwargs :

    Notes
    -----
    The import must occur here to avoid recursive imports.
    """
    from bombcell.bombcell import bombcell_placeholder

    run_job(kwargs, bombcell_placeholder, "run bombcell for quality")
