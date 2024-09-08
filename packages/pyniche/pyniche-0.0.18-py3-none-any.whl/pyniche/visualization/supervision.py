import numpy as np
import supervision as sv
import matplotlib.pyplot as plt


def vis_detections(
    image,
    detections=None,
    text="object",
    thickness=2,
    figsize=(20, 10),
    save=None,  # output path
):
    """
    img: PIL.Image for the annotation to be drawn on
    detections: sv.Detection
    text: text annotations, e.g., "balloon". If None, no text is drawn
    """
    color = sv.Color.blue()
    ann_bbox = sv.BoundingBoxAnnotator(
        thickness=thickness,
        color=color,)
    ann_text = sv.LabelAnnotator(
        text_position=sv.Position.BOTTOM_LEFT, 
        color=color,)

    if detections:
        # draw predictions
        att_frame_pred = ann_bbox.annotate(np.array(image), detections)
        if text:
            text_ann = [f"{text}" for _ in range(len(detections))]
            att_frame_pred = ann_text.annotate(
                att_frame_pred,
                detections,
                labels=text_ann,
            )
        plt.figure(figsize=figsize)

        if save:
            plt.imsave(save, att_frame_pred)
        else:
            plt.imshow(att_frame_pred)
        plt.close()
    else:
        # save image only
        plt.figure(figsize=figsize)
        plt.imshow(image)
        plt.savefig(save)
