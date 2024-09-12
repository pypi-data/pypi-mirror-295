import skvideo.io
import numpy as np
import napari
import os


def get_all_arena_images(mtd, video_fname='*camera.mp4', frame_idx=500):
    """
    saves an image for every video in the path list provided
    :param all_video_paths:
    :param out_dir:
    :return:
    """

    video_paths = mtd.root.rglob(video_fname)

    for vpath in list(video_paths):
        fpath_out = vpath.parent / "arena_frame.npy"
        if not os.path.isfile(fpath_out):
            img_idx = frame_idx
            videogen = skvideo.io.vreader(str(vpath))
            for frame, idx in zip(videogen, range(img_idx)):
                f = frame
            print(f'saving to .. {fpath_out}')
            np.save(fpath_out, np.mean(f, axis=2))


def curate_all(mtd):

    """
    tool for getting the arena outline

    :param root_dir:
    :param out_dir:
    :return:
    """
    data_paths = list(mtd.root.rglob('arena_frame.npy'))
    data_paths = [p for p in data_paths if not (p.parent / "box_corner_coordinates.npy").exists()]
    image = np.array([np.load(p) for p in data_paths])

    with napari.gui_qt():
        v = napari.Viewer(title="curate crop region")
        v.add_image(image)
        shapes_layer = v.add_shapes()

        @v.bind_key("b")
        def conv_to_b(v):
            for data in v.layers[-1].data:
                box_vertices = np.array([data[0], data[3], data[2], data[1]])
                for p in data_paths:
                    out_path = p.parent / "box_corner_coordinates.npy"
                    print(out_path)
                    np.save(str(out_path), box_vertices)

