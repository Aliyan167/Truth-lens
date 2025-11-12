import os
import cv2
import logging
from . import detect_adapter

logger = logging.getLogger(__name__)

def process_video(input_path, output_path, frame_skip=1, resize=None, codec='mp4v'):
    """
    Reads input_path, runs detect_adapter.detect_frame on selected frames,
    writes annotated output to output_path (MP4).
    - frame_skip: process every nth frame (1 = every frame)
    - resize: (w, h) or None
    """
    cap = cv2.VideoCapture(str(input_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open input video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out_w, out_h = (w, h) if resize is None else resize

    fourcc = cv2.VideoWriter_fourcc(*codec)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = cv2.VideoWriter(str(output_path), fourcc, fps, (out_w, out_h))

    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % frame_skip == 0:
            if resize is not None and (out_w, out_h) != (frame.shape[1], frame.shape[0]):
                frame = cv2.resize(frame, (out_w, out_h))

            try:
                annotated = detect_adapter.detect_frame(frame.copy())
                if annotated is None:
                    annotated = frame
            except Exception as e:
                logger.error(f"Frame {idx} failed: {e}")
                annotated = frame

            if annotated.shape[0:2] != (out_h, out_w):
                annotated = cv2.resize(annotated, (out_w, out_h))
            writer.write(annotated)

        idx += 1
        if idx % 50 == 0:
            print(f"Processed {idx} frames...")

    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print(f"✅ Processing finished. Saved to {output_path}")
