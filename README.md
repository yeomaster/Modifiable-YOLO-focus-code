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





Korean:

이 프로젝트는 YOLO가 생성하는 바운딩 박스를 실시간으로 수정하거나 변경할 수 있는지를 확인하기 위해 제작되었습니다.

YOLO의 발전으로 더 많은 객체들을 높은 정확도로 식별할 수 있게 되었습니다. 하지만 현 시대에 사용되는 많은 프로그램들, 특히 로보틱스 분야에서는 작업이 변할 수 있기 때문에 수정 가능성이 요구됩니다. 본 프로젝트에서는 YOLO와 다양한 라이브러리를 활용하여 음성 명령을 통해 프로그램의 ‘초점(focus)’/관심 대상을 다른 객체로 바꿀 수 있는 컴퓨터 비전 프로그램을 구현하는 것을 목표로 합니다.

사용된 라이브러리:
- ultralytics (YOLO용)
- speech_recognition (음성 인식용)
- cv2 = OpenCV (카메라 연결용)
- threading (병렬 실행용)


작동 방식:
1. 프로그램은 라이브러리와 연결을 설정합니다. (참고: speech_recognition은 음성을 구글 서버로 직접 전송하여 번역/식별하므로 인터넷 연결이 필요합니다.)
2. YOLO가 식별할 수 있는 모든 객체를 나열합니다. (리스트에 있는 항목만 말해야 합니다.)
3. 사용자에게 리스트 중 하나를 말하도록 요청하며, 해당 객체가 프로그램의 주요 ‘초점’이 됩니다.
3. 프로그램은 사용자가 지정한 초점 객체 주위에 초록색 바운딩 박스를 표시합니다.
4. 그 외의 객체들은 파란색 박스로 표시됩니다.
5. 사용자가 초점을 바꾸고 싶을 경우, 키보드에서 ‘f’ 키를 누른 후 새로운 객체를 음성으로 말해야 합니다.
6. 새로운 객체가 인식되면, 프로그램의 초점이 해당 객체로 전환됩니다.
7. 프로그램을 종료하려면 ‘q’ 키를 누릅니다.
