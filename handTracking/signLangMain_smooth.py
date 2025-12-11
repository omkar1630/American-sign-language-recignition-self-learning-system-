
import cv2
import time
import EntryPopUp
from handTrackingModule import HandDetector
from EntryPopUp import EntryPopUp
from AlphaToSign import AlphaToSign

ep=EntryPopUp()
ans=ep.getAns()

if ans=="cam":
    wCam,hCam=640,480

    cap=cv2.VideoCapture(0)
    cap.set(3,wCam)
    cap.set(4,hCam)

    pTime=0
    detector = HandDetector(min_detection_confidence=0.85)
    condition=True

    letter_buffer = []
    max_buffer_size = 20
    last_sign_time = time.time()
    previous_letter = ""
    stable_start_time = None
    required_hold_time = 0.5  # reduced hold time

    while condition:
        success,img=cap.read()
        img = cv2.flip(img, flipCode=1)
        img=detector.findHands(img)
        lmList=detector.findPosition(img,draw=False)
        condition=detector.condition

        if len(lmList)!=0:
            name = detector.signCondition()
            print(f"Predicted sign: {name}")

            current_time = time.time()
            if name and name != "else":
                if name.upper() != previous_letter:
                    stable_start_time = current_time
                    previous_letter = name.upper()
                elif stable_start_time and (current_time - stable_start_time) >= required_hold_time:
                    letter_buffer.append(name.upper())
                    letter_buffer = letter_buffer[-max_buffer_size:]
                    stable_start_time = None
                    last_sign_time = current_time
            elif current_time - last_sign_time > 5:
                letter_buffer = []
                previous_letter = ""
                stable_start_time = None

            joined = "".join(letter_buffer)
            cv2.putText(img, f"Signed: {joined}", (10, 420), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 2)

        cTime = time.time()
        fps = 1 / (cTime - pTime) if cTime != pTime else 0
        pTime = cTime

        cv2.putText(img, f"FPS: {int(fps)}", (400, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 255, 0), 3)
        cv2.imshow("Image",img)
        cv2.waitKey(1)

elif(ans=="ui"):
    alpha=AlphaToSign()

else:
    print("code exited")
