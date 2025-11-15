import random
import cv2
import cvzone 
from cvzone.HandTrackingModule import HandDetector 
import time

# --------- Read total rounds from CLI argument (fallback to 3) ----------
import sys
import os

if len(sys.argv) > 1:
    try:
        totalRounds = int(sys.argv[1])
    except:
        totalRounds = 3
else:
    totalRounds = 3

currentRound = 1
# -----------------------------------------------------------------------

cap = cv2.VideoCapture(0) 
cap.set(3, 640)
cap.set(4, 480)
 
detector = HandDetector(maxHands=1)
 
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
imgAI = None
 
while True:

    # Stop automatically if rounds completed
    if currentRound > totalRounds:
        print("\nGame Finished!")
        print(f"Final Score → AI: {scores[0]}, Player: {scores[1]}")
        break

    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()
 
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]
 
    hands, img = detector.findHands(imgScaled)
 
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435),
                        cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
 
            if timer > 3:
                stateResult = True
                timer = 0
 
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
 
                    randomNumber = random.randint(1, 3)
                    imgAI_candidate = cv2.imread(f'Resources/{randomNumber}.png',
                                                 cv2.IMREAD_UNCHANGED)
                    if imgAI_candidate is not None:
                        imgAI = imgAI_candidate
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
 
                    # Player wins
                    if (playerMove == 1 and randomNumber == 3) or \
                       (playerMove == 2 and randomNumber == 1) or \
                       (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
 
                    # AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                       (playerMove == 1 and randomNumber == 2) or \
                       (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                    # ------------ NEW FEATURE: Move to next round ------------ #
                    currentRound += 1
                    # ---------------------------------------------------------- #

    imgBG[234:654, 795:1195] = imgScaled
 
    if stateResult and imgAI is not None:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
 
    # Scores
    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN,
                4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN,
                4, (255, 255, 255), 6)

    # ------------ NEW FEATURE: Show Round Number ------------ #
    cv2.putText(imgBG, f"Round {min(currentRound, totalRounds)} / {totalRounds}",
                (500, 120), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 4)
    # ---------------------------------------------------------- #

    cv2.imshow("BG", imgBG)
 
    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
 
    if key == ord('q'):
        break
 
    try:
        if cv2.getWindowProperty("BG", cv2.WND_PROP_VISIBLE) < 1:
            break
    except:
        pass
 
cap.release()
cv2.destroyAllWindows()
