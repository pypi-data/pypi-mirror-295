import os
import datasets
from pyniche.data.huggingface.detection import hf_to_coco, hf_to_yolo


def COLO(
    root: str,  # path to save the data folder
    format: str = "coco",  # "coco" or "yolo"
    config: str = None,  #
    resize: tuple = (640, 640),  # (width, height)
):
    if config is None:
        config = [
            "0_all",
            "1_top",
            "2_side",
            "3_external",
            "a1_t2s",
            "a2_s2t",
            "b_light",
            "c_external",
        ]
    format = format.upper()
    for c in config:
        print("[%d / %d] Downloading COLO %s" % (config.index(c) + 1, len(config), c))
        data = datasets.load_dataset(
            "Niche-Squad/COLO",
            c,
            download_mode="force_redownload",
        )
        if format == "COCO":
            hf_to_coco(
                data,
                os.path.join(root, c),
                classes=["cow"],
                size_new=resize,
            )
        elif format == "YOLO":
            hf_to_yolo(
                data,
                os.path.join(root, c),
                classes=["cow"],
                size_new=resize,
            )
