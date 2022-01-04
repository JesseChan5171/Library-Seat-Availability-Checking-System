import cv2
from imutils.video import VideoStream
from tensorflow.keras.models import load_model
import time
from detect_mask_video import detect_and_predict_mask
# detect_and_predict_mask module based on "https://github.com/balajisrinivas/Face-Mask-Detection"

cv2.startWindowThread()
vs = VideoStream(src=0).start()
prototxtPath = r"deploy.prototxt"
weightsPath = r"res10_300x300_ssd_iter_140000.caffemodel"

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model("mask_detector.model")

rec = []
rec_len = []


def output_stat(lenf):
    if len(rec) == 0:
        rec.append([start, lenf])
        rec_len.append(lenf)
    elif int(time.time()) - int(rec[-1][0]) > 10:
        rec.append([time.time(), lenf])
        rec_len.append(lenf)


start = time.time()
while (True):
    # Capture frame-by-frame

    frame = vs.read()
    lefy = frame.shape[0]
    lefx = frame.shape[1]

    # locs, preds, len_f = find_mask(frame)
    locs, preds, len_f = detect_and_predict_mask(frame, faceNet, maskNet)
    for (box, pred) in zip(locs, preds):
        # unpack the bounding box and predictions
        (x0, y0, x1, y1) = box
        (mask, withoutMask) = pred

        if mask > withoutMask:
            label = "Masked"
            color = (0, 255, 0)
        else:
            label = "No Mask"
            color = (0, 0, 255)

        cv2.putText(frame, label, (x0, y0 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (x0, y0), (x1, y1), color, 2)

    if len_f > 0:
        cv2.putText(frame, str(len_f), (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        print(len_f)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    output_stat(len_f)

cv2.destroyAllWindows()
cv2.waitKey(1)

print(rec)
