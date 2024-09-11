import os
from pathlib import Path

import fire

from lmtracker.default_params import dlc_config_params
from lmtracker.transfer import sync_raw_and_processed_data
from lmtracker import process_DLC_output, video_processing

import pathlib
import numpy as np


def get_tracks_path(directory, config_dict, get_all_paths=False):
    fname = config_dict['DLC_fname']
    h5_files = list(directory.glob(f"{fname}"))

    if h5_files:
        if get_all_paths:
            return h5_files
        for f in h5_files:
            if "filtered" in str(f):
                return f
        return h5_files[0]

    return None


def save_npy_tracks(directory, config_dict):
    tracks_path = get_tracks_path(directory, config_dict)
    print(tracks_path)
    if tracks_path is not None:
        print(f"saving tracks to {tracks_path}")
        mouse_xy_tracks = process_DLC_output.process_DLC_output(
            str(tracks_path), config_dict
        )
        mouse_positions_x_path = str(tracks_path.parent / "dlc_x_tracks.npy")
        mouse_positions_y_path = str(tracks_path.parent / "dlc_y_tracks.npy")

        np.save(mouse_positions_x_path, mouse_xy_tracks["x"])
        np.save(mouse_positions_y_path, mouse_xy_tracks["y"])


def get_paths(source_path, video_file_name='camera', video_fmt='avi'):
    return source_path.rglob(f'*{video_file_name}.{video_fmt}')


def get_processed_path(path):
    derivatives_path = str(path).replace('rawdata', "derivatives")
    return Path(derivatives_path)


def process_behaviour(mouse_id: str,
                      rawdata_dir: str,
                      derivatives_dir: str,
                      track=False,
                      config_dict=dlc_config_params,
                      overwrite=False,
                      video_file_name='camera',
                      input_video_fmt='avi',
                      output_video_fmt='mp4',
                      label_video=False,
                      logs_path=None,
                      skip_video_processing=False,
                      ):
    raw_directory = pathlib.Path(rawdata_dir)
    processed_directory = pathlib.Path(derivatives_dir)

    raw_mouse_path = raw_directory / mouse_id
    processed_mouse_path = processed_directory / mouse_id

    if not skip_video_processing:
        assert(raw_mouse_path is not None)
        assert(processed_mouse_path is not None)

        sync_raw_and_processed_data(mouse_id=mouse_id,
                                    raw_directory=raw_directory,
                                    processed_directory=processed_mouse_path.parent)

        raw_paths = get_paths(raw_mouse_path,
                              video_file_name=video_file_name,
                              video_fmt=input_video_fmt)

        all_video_paths = list(raw_paths)
        print(f"all vid paths: {all_video_paths}")
        for path in all_video_paths:
            print(path)
            print(str(get_processed_path(path)).replace(input_video_fmt, output_video_fmt))
            video_processing.convert_avi_to_mp4(
                path,
                dest=Path(str(get_processed_path(path)).replace(input_video_fmt,
                                                                output_video_fmt)
                          ))

    processed_paths = get_paths(
                                processed_mouse_path,
                                video_file_name=video_file_name,
                                video_fmt=output_video_fmt
                                )

    for path in list(processed_paths):
        print('vidpath found:')
        print(path)
        if track:
            dlc_track_video(
                            pathlib.Path(str(path)),
                            config_dict=config_dict,
                            overwrite=overwrite,
                            label_video=label_video,
                            )


def dlc_track_video(
    vpath, config_dict, label_video=False, overwrite=False
):
    import deeplabcut

    directory = vpath.parent
    all_paths = get_tracks_path(
        directory, config_dict, get_all_paths=True
    )

    if not os.path.isdir(directory):
        os.mkdir(str(directory))

    tracks_path = get_tracks_path(directory, config_dict)
    BASE_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__))).parent
    CONFIG_PATH = BASE_DIR / config_dict['config_path']

    print(CONFIG_PATH)

    if not os.path.isfile(str(tracks_path)):
        deeplabcut.analyze_videos(CONFIG_PATH, [str(vpath)])

    if overwrite:

        if all_paths is not None:
            for p in all_paths:
                print(f"deleting... {str(p)}")
                os.remove(str(p))

        deeplabcut.analyze_videos(CONFIG_PATH, [str(vpath)])

    deeplabcut.filterpredictions(CONFIG_PATH, [str(vpath)])

    tracks_path = get_tracks_path(vpath.parent, config_dict)
    print(f"looking for track path: {tracks_path}")
    if tracks_path is not None:
        print(f"valid track path {tracks_path} processing and output")
        mouse_xy_tracks = process_DLC_output.process_DLC_output(
            tracks_path, config_dict
        )

        mouse_positions_x_path = directory / "dlc_x_tracks.npy"
        mouse_positions_y_path = directory / "dlc_y_tracks.npy"
        print(
            f"saving tracks to {mouse_positions_x_path} and {mouse_positions_y_path}"
        )
        np.save(str(mouse_positions_x_path), mouse_xy_tracks["x"])
        np.save(str(mouse_positions_y_path), mouse_xy_tracks["y"])

        if label_video:
            print("creating labeled video")
            labelled_vid = deeplabcut.create_labeled_video(
                CONFIG_PATH, [str(vpath)], save_frames=True
            )
            return mouse_xy_tracks, labelled_vid

    save_npy_tracks(directory, config_dict)


def main():
    fire.Fire(process_behaviour)


if __name__ == "__main__":
    main()



