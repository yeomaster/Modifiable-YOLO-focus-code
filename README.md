# Modifiable-YOLO-focus-code
This project was made to see if the bounding boxes that YOLO creates can be modified/changed on the fly.

With the advancement of YOLO many more objects can be identified with greater certainty. Yet many programs used in th current era, especially those in robotics, need to be modifiably as the task may change.
In this project I aim to use YOLO and various other libraries to create a computer vision program that can change the 'focus' / attention of the program to other items via voice command

libraries used:
- ultralytics (for YOLO)
- speech_recognition (for voice activation)
- cv2 = OpenCV (for connection to camera)
- threading (for running code in parallel)

