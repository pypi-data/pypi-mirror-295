import subprocess


def sync_raw_and_processed_data(
    raw_directory,
    processed_directory,
    mouse_id=None,
):
    """
    Runs rsync command from python to copy across necessary data from raw to processed directories. May require
    modification for use on Windows. Tested on Linux.

    :param raw_directory:
    :param processed_directory:
    :return:
    """
    if mouse_id is not None:
        raw_directory = raw_directory / str(mouse_id)
        processed_directory = processed_directory / str(mouse_id)

    print(f"transferring {raw_directory} to {processed_directory}")
    cmd = f"rsync -tvr --chmod=D2775,F664 --exclude='ephys' --exclude='*.avi' --exclude='*.imec*' --exclude='.mp4' {raw_directory}/* {processed_directory} --checksum --append-verify"
    p =subprocess.Popen(cmd, shell=True)
    p.wait()
