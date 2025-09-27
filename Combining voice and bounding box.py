from ultralytics import YOLO # bounding box + item recognition 
import speech_recognition as sr # for voice recognition, connected to google (internet connection is REQUIRED)
import cv2 # camera
import threading  # for non-blocking voice capture 


# importing and downloading yolo v8 nano
model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0) # video capture, opening connection to the camers (0) by using a function inside cv2 called Video Capture
if not cap.isOpened(): # if you cant connect
    print("Camera open failed"); raise SystemExit # exit program before any catastrophic program

# YOLO class lists (case-insensitive matching)
items = list(model.names.values())                         # ["person", "bicycle", ...]
# model.names is a dictionary built into YOLO where the key is a class ID number (0, 1, 2, ... 79)
# key value == name of class that is mapped to the number (ie 0== person, 1 == bicycle)
# remember: dictionary in python == key: key value
# turns the values (not ID number, into a list)

items_lower = {name.lower(): name for name in items}       # {"person":"person", ...}
# for name in items == for each name in items
# why do we have name.lower(): name for name in items instead of just for name in items?
# -> because this is a *dictionary comprehension*: {key_expr : value_expr for var in iterable}
#    here key_expr = name.lower(), value_expr = name, iterable = items

print("Items that YOLO can focus on:")
print(", ".join(items)) # join all the items in the list and print them out so we can see what items the 
print()

# --- SpeechRecognition setup ---
r = sr.Recognizer() 
mic = sr.Microphone() 
# these two are classes in speech_recognition, both of them have different methods inside them that have different functions (used below)

# Calibrate once for background noise
with mic as source:
    # This opens the microphone (mic) as an audio source and assigns it to the variable source
    # 'with' means we use the file or function briefly, so we only use it once before closing it
    # This means: “open the microphone (mic) for listening, call it source, and when done, close it safely.”
    # the sound from the mic is now stored as 'source', which will only be stored within the 'with' 
    print("Adjusting for background noise, please wait...")
    r.adjust_for_ambient_noise(source, duration=1)
    # This tells the recognizer (r) to listen to the background noise for 1 second.
    # During that second, it measures the average volume of noise in the room (like fans, typing, or hums)
    # It then sets an energy threshold internally.
    # If a sound is below that threshold, it’s treated as noise and ignored.
    # If a sound is above the threshold, it’s treated as speech.

# Ask by voice until valid (blocking only at startup is fine)
while True:
    print("Say the item to focus (e.g., 'person', 'dog', 'car')...")
    with mic as source:
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            # This tells the Recognizer (r) to capture sound from the source (your mic, in this case)
            # source is the 'source of sound' ie what the mic hears
            # timeout = max number of seconds the system will wait until it hears us speaking, (ie overcome the energy threshold)
            # If you run the code and sit silent for 5 seconds → error
            # If you start speaking at 3 seconds → it records normally
            # phrase_time_limit = max length of recording, different from 'timeout' phrase_time_limit will only start once energy threshold is overcome
        except sr.WaitTimeoutError:
            # WaitTimeoutError is a specific error (exception class) from the speech_recognition library
            # it will occur if no voice is heard
            # except is here to allow for a safe exit in case sr.WaitTimeoutError occurs
            print("No speech detected, try again.")
            continue
    #this system essentially meanst to keep trying to listen until an audio is heard
    #if no audio is heard, try again (hence the 'continue')

    try:
        focus_in = r.recognize_google(audio, language="en-US").strip().lower()
        # takes the audio source the system just heard and sends it to google via the speech_recognition library
        # notifies the google servers that i am using standard american english
        # strip = removes any empyt space bars from the audio (more as a precaution than anything else)
        # lower = changes all words to lowercase to match the YOLO library lists
        
        print("You said:", focus_in)
        if focus_in in items_lower:
            # if item said in speech is found in the list of items in YOLO
            focus = items_lower[focus_in]  # canonical label
            # this becomes the 'focus' of the program (used later)
            break
        else:
            print("Error! Item does not exist. Try again.")
    except sr.UnknownValueError:
        print("Could not understand audio, try again.")
    except sr.RequestError as e:
        print(f"Speech API error: {e}")

print(f"Focus set to: {focus}")
print("Press 'q' to quit, 'f' to change focus.")

# --- Non-blocking voice change setup (threading) ---  
listening = False   # guard so we don't start multiple listeners at once
# sets listening to 'False' just in case listening was set to true for some reason earlier in the program
# listening is used later so we need to ensure that it is set to False for now, else we can have multiple sources of listening


#this function is to restart the listening part of the system whenever we want to change the focus
def voice_listener():                                 
    """Background thread: listen once and update `focus` if valid."""
    global focus, listening
    # sets focus amd listening as global variables

    with mic as source:
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            listening = False
            return

    try:
        spoken = r.recognize_google(audio, language="en-US").strip().lower()
        print("You said:", spoken)
        if spoken in items_lower:
            focus = items_lower[spoken]
            print(f"Focus changed to: {focus}")
        else:
            print("That’s not a YOLO item.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Speech API error: {e}")
    finally:
        listening = False  # allow future presses of 'f'



# --- Main YOLO loop ---
while True:
    ok, frame = cap.read()
    if not ok:
        break
    # ok == True/False value that tells you if reading the frame worked
    # frame == the actual image from the camera (a NumPy array, e.g. 480x640x3)
    # cap.read == a function that grabs one frame from the VideoCapture object

    # Run YOLO and take the first (only) result
    res = model(frame, verbose=False)[0]
    # res (as in 'result')
    # model == calls/ accesses YOLO since as we equated model to yolo earlier
    # verbose == deactivates detailed message log on terminal
    # [0] ==  since we only have a list size that is a length of 1 (due to frame being a single image that is constantly being updated as a video) we only need to take the first image of the list (yolo can take multiple so you gotta clarify which one we're using here)

    # Draw detections
    for box in res.boxes:
        # this is where it gets tricky
        # res.boxes does three things:
        # 1. draws a box around an object it detects by plotting 4 coordinate points: x1,x2,y1,y2 
        # 2. give a confidence score of how certain it is in identify an object
        # 3. gives a classification for what the object is (e.g., 0 = person, 1 = bicycle, 2 = car, etc.)

   # 1) Get coordinates
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        # converts the cooridnates that the box receives into a python list, and then stores them in the coordinates x1,x2,y1,y2 (they are float values at this point)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # converts the coordinates into int values for the sake of simplicity
        

        # 2) Get confidence and class label
        conf = float(box.conf[0]) # store the confidence values of YOLO here (we use 0 here as this is the location of the image in the list created by ultralystic)
        cls_id = int(box.cls[0]) # store the confidence values of YOLO here
        label = res.names[cls_id] # this maps the class ID(which is a number) to the names such as 1 == person


        if label == focus:    
            # 4) Draw the rectangle + label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), thickness=2)
            # rectangle == creates a rectangle
            # Using the frame of the video given
            # one of the corners is (x1,y1), the other is (x2,y2)
            # the next three numbers is actually RGB values, So (0, 255, 0) = pure green
            # ofc, thickness of the box drawn can be modified
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, max(0, y1-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
            # This is for the text to appear on the top left of EACH bounding box
            # {label} {conf:.2f}" == add the label and the confidence score here with the later being 2 decimal points
            # (x1, max(0, y1-8)) == setting the position of text, starting at the x position of x1, and just a few pixels above the y1 position. max is needed here prevent negative numbers so that the text never dissapears over the top of the screen
            # note: cooridnates in pixels, and screens read right and DOWN, in contrast to the right and UP of graphs. Moreover, origin (0,0) is at the top LEFT of the screen
            # FONT_HERSHEY_SIMPLEX == font type
            # 0.6, (0,255,0), 2 == Font size, text colour green, thickness of text

        else: 
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), thickness=2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, max(0, y1-8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 2)

    cv2.imshow("YOLOv8n live (q=quit, f=change focus)", frame)
    # show the text as the title of the screen
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
        # for every 1 microsecond (essentiially a screen refresh) check if 'q' is pressed, if it is then break the for loop


    elif key == ord('f'):
        # Start background listener so the video loop doesn't freeze
        if not listening:
            # listeining is used here as a 'lock' of sorts
            # if listening is false then and ONLY then we activate the threading to follow (listeing to a new focus)
            # listeinig is set to false every time a new focus is assigned
            # if we did not do this then we would have multiple instances of treading occuring, which would just tank the system 
            listening = True
            # now set the listening variable to 'True' ie tell the system that we are indeed listening to a new word
            print(" Say the new focus item (e.g., 'person', 'dog', 'car')...")
            threading.Thread(target=voice_listener, daemon=True).start()
            # this is where threading becomes important
            # threading.Thread(...) == Creates a new thread object.
            # A thread is like a helper worker that can run code in parallel to the main loop
            # normally python runs one code at a time, but with 'threading' we can run the code AND the program at the same time
            # 
            # set the voice_listener function created earlier as target variable
            # note: 'target' is a required parameter in threading.Thread as it tells the thread, which function to run inside the thread.
            # It needs to be written this way to inform the thread that this is the function that it is going to run in the background
            # and no, we dont write the function call as voice_listener() like we normally would do as that would activate the function in the main program immediately
            # need to hand it over to the thread first, and then start it to make sure it runs in the background
            # daemon == true, This marks the thread as a daemon thread
            # being marked as a daemon essentially tells the program to shutdown this thread as well if the main program closes, thats it
            # .start() == once the thread recieves all the parameters it needs, it can start
        else:
            print("Already listening...")


# once the loop is broken, break connection to the camera and close all windows open
cap.release()
cv2.destroyAllWindows()
