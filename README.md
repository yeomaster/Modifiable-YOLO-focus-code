# Modifiable-YOLO-focus-code
This project was made to see if the bounding boxes that YOLO creates can be modified/changed on the fly.

With the advancement of YOLO many more objects can be identified with greater certainty. Yet many programs used in th current era, especially those in robotics, need to be modifiably as the task may change.
In this project I aim to use YOLO and various other libraries to create a computer vision program that can change the 'focus' / attention of the program to other items via voice command

libraries used:
- ultralytics (for YOLO)
- speech_recognition (for voice activation)
- cv2 = OpenCV (for connection to camera)
- threading (for running code in parallel)

how it works:
1. program establishes connection to libaries (note: speech_recognition needs online connection as it sends audio directly to google servers for translation/identification)
2. Lists out all items YOLO can identify (only say items out of this list)
3. user is asked to say one item from the list as the main 'focus' of the program
4. the program will now draw a GREEN bounding box around the item the user asked to focus on
5. other items are drawn in BLUE
6. if the user wants to change the focus, they are required to press 'f' on the keyboard and audiable say the new item.
7. once the new item is said, the focus will now change to said item
8. press 'q' to quit the program
