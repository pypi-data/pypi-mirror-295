import os
from bombcell.bombcell_matlab_script_template import bombcell_template_matlab_script


def get_bombcell_paths_str(session_mtd):
    ephysKilosortPath = f'{session_mtd.kilosort_dir}'
    ephysRawDir = f'{session_mtd.raw_traces_path}'
    ephysMetaDir = f'{session_mtd.raw_meta_path}'
    savePath = f'{session_mtd.kilosort_dir.parent / "bombcell"}'
    decompressDataLocal = f'{session_mtd.kilosort_dir.parent / "bombcell_ephys"}'

    matlab_paths_string = f"ephysKilosortPath = '{ephysKilosortPath}'; \n" \
                          f"ephysRawDir = dir('{ephysRawDir}'); \n" \
                          f"ephysMetaDir = dir('{ephysMetaDir}'); \n" \
                          f"savePath = '{savePath}'; \n" \
                          f"decompressDataLocal = '{decompressDataLocal}'; \n"

    return matlab_paths_string


def write_bombcell_matlab_script(s, bombcell_location="/nfs/nhome/live/slenzi/code/bombcell"):
    bombcell_paths = get_bombcell_paths_str(s)
    script_content = f"addpath(genpath('{bombcell_location}')); \n{bombcell_paths} \n {bombcell_template_matlab_script}"
    file_name = s.kilosort_dir.parent / "bc_quality_metrics.m"
    with open(file_name, "w") as file:
        file.write(script_content)
        os.chmod(file_name, 0o755)


def bombcell_placeholder(logs_path=None):
    print('running_bombcell...')

