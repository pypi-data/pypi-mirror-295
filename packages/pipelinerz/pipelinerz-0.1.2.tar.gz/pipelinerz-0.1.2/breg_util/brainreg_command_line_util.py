import pathlib


def get_output_dir(
    mouse_id,
    data_dir,
):
    data_dir = pathlib.Path(data_dir)
    return data_dir / mouse_id / "histology"


def voxel_sizes(recipe_path):
    import yaml

    with open(str(recipe_path), "r") as stream:
        try:
            params = yaml.safe_load(stream)
            return params["VoxelSize"]
        except yaml.YAMLError as exc:
            print(exc)


def get_brain_path(
    mouse_id,
    brain_dir,
    channel_id="2",
):
    path = (
        pathlib.Path(brain_dir) / mouse_id / "stitchedImages_100" / channel_id
    )
    return path


def brainreg_command(mouse_id, mouse_dir, root_dir, serial2p_dir, function="brainreg", atlas="allen_mouse_10um", additional=None):
    input_path = get_brain_path(mouse_id, serial2p_dir)
    output_path = get_output_dir(mouse_dir, data_dir=root_dir) / atlas
    print(input_path)
    print(output_path)
    recipe_path = list(input_path.parent.parent.glob("recipe*"))[0]
    voxels = voxel_sizes(recipe_path)
    additional = f"--additional {input_path.parent / additional}" if additional is not None else ""
    cmd = f"{function} {input_path} {output_path} {additional} -v {voxels['Z']} {voxels['X']} {voxels['Y']} --orientation psr --atlas {atlas}"
    return cmd


def brainreg_commandline(
    mouse_id, mouse_dir, root_dir, brain_dir, function="brainreg", atlas="kim_mouse_10um", logs_path=None, additional=None
):
    command = brainreg_command(mouse_id, mouse_dir, root_dir, brain_dir, function=function, atlas=atlas, additional=additional)
    # subprocess.run(command,
    #                executable="/bin/bash",
    #                shell=True,
    #                )
