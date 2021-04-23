import cv2
import mediapipe as mp
# import dlib
import numpy
import math

from time import sleep
import pythonosc
from pythonosc import osc_message_builder
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import AsyncIOOSCUDPServer
# from pythonosc.dispa93her import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc import osc_server
import threading

rpi_ip = "192.168.167.93"
toMotors = 9995
# fromZigSim = 50001
client = SimpleUDPClient(rpi_ip, toMotors)  # Create client

rpi_ip2 = "192.168.167.133"
toMotors2 = 9999
# fromZigSim = 50001
client2 = SimpleUDPClient(rpi_ip2, toMotors2)  # Create client

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# def pAngle(val):
#   return (val - x1) / (x2 - x1)
#
# def tAngle(val):
#   return (val - y1) / (y2 - y1)

def send2motor(pAngle, tAngle):
  print("move: ", pAngle, tAngle)

def scaleBetween(unscaledNum, minAllowed, maxAllowed, min, max):
  if unscaledNum < min:
    unscaledNum = min
  if unscaledNum >= max:
    unscaledNum = max
  return ((maxAllowed - minAllowed) * (unscaledNum - min) / (max - min)) + minAllowed

# For webcam input:
cap = cv2.VideoCapture(1)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:

      #this is the data of how many hands, which side -- parsing to be determined
      # print('Handedness:', results.multi_handedness)

      for hand_landmarks in results.multi_hand_landmarks:
        # x1 = hand_landmarks.left()  # left point
        # y1 = hand_landmarks.top()  # top point
        # x2 = hand_landmarks.right()  # right point
        # y2 = hand_landmarks.bottom()  # bottom point

        #print all the points
        # print('All hand points')
        for id in range(1):
          mp_drawing.draw_landmarks(
              image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

          # x = hand_landmarks.landmark[0].x
          # y = hand_landmarks.landmark[0].y

          print ('ready')


          # print('pt',id, ' ', hand_landmarks.landmark[id].x, hand_landmarks.landmark[id].y)
          # id+=1
          # print('done hand points')
          #
          # # print only one point
          # print(
          #   f'Index finger normalised tip coordinates: (',
          #   f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x}, '
          #   f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y})'
          # )

          msg1 = []
          msg1 = osc_message_builder.OscMessageBuilder(address="/hand")
          msg1.add_arg(0)
          msg1.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
          msg1.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
          msg2 = []
          msg2 = osc_message_builder.OscMessageBuilder(address="/hand")
          msg2.add_arg(1)
          msg2.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
          msg2.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
          msg3 = []
          msg3 = osc_message_builder.OscMessageBuilder(address="/hand")
          msg3.add_arg(0)
          msg3.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
          msg3.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
          msg4 = []
          msg4 = osc_message_builder.OscMessageBuilder(address="/hand")
          msg4.add_arg(1)
          msg4.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
          msg4.add_arg(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)
          msg1 = msg1.build()
          client.send(msg1)
          sleep(0.2)
          msg2 = msg2.build()
          client.send(msg2)
          msg3 = msg3.build()
          client2.send(msg3)
          sleep(0.3)
          msg4 = msg4.build()
          client2.send(msg4)



    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
