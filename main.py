import cv2
import numpy as np

net = cv2.dnn.readNet("yolov3.weights","yolov3.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)

classes = []
with open ("coco.names","r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]

cam = cv2.VideoCapture(0)

while(True):
    ret, frame = cam.read()
    img = cv2.resize(frame,None,fx=0.4,fy=0.4)
    height, width, channels = frame.shape
    
    blob = cv2.dnn.blobFromImage(frame,0.00392,(416, 416),(0,0,0),True, crop=False)

    for b in blob:
        for frame_blob in b:
            next
            #cv2.imshow("img", frame_blob)

    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.8:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                
                x = int(center_x - w /2)
                y = int(center_y - h /2)

                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)
    font = cv2.FONT_HERSHEY_COMPLEX
    for i in range (len(boxes)):
        if i in indexes:
            x,y,w,h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.rectangle(frame,(x,y-30),(x+(len(label)*20),y+5),(0,255,0),-1)
            cv2.putText(frame, label,(x,y-10),font,1,(0,0,0),1)
        
    cv2.imshow("image", frame)

    #cv2.imshow("frame",frame)
    cv2.waitKey(20) and 0xFF == ord("q")
       #break

cap.release()
cap.destroyAllWindows()
