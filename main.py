# SE usa cvzon 1.4.1
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# Abrir la camara y se configura el tamaño
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
colorR = (255, 0, 255) # Color default

cx, cy, w, h = 100, 100, 200, 200

# Detector de manos
detector = HandDetector(detectionCon=0.8,maxHands=1)


class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h =self.size

        # Si el dedo indice está dentro del rectangulo
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

rectList = []
for x in range(5):
    rectList.append(DragRect([x*250 + 150, 150]))

while True:
    # Encender la camara
    success, img = cap.read()

    # Se cambia la configuracion para el movimiento de las manos
    img = cv2.flip(img, 1)

    # Encontrar las manos
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # Se encontrará el dedo indice y cambiara el color de la caja
    if lmList:
        # Detecta la distancia entre el indice y el anular
        l, _, _ = detector.findDistance(8, 12, img, draw=False)
        print(l)
        # Si estan juntos va a mover la caja
        if l < 40:
            # La marca de la punta del dedo indice
            cursor = lmList[8]  # Tiene dos coordenadas x, y
            print(l)
            # Llamamos al metodo update
            for rect in rectList:
                rect.update(cursor)

    #Dibujar los rectangulos solidos
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
  # Construccion de las cajas
        cv2.rectangle(img, (cx - w//2, cy -h//2), (cx + w//2, cy + h//2), colorR, cv2.FILLED)
        cvzone.cornerRect(img, (cx - w//2, cy -h//2, w, h), 20, rt=0)


    # DIBUJAR TRANSPARENCIA

    #imgNew = np.zeros_like(img, np.uint8)
    #for rect in rectList:
    #    cx, cy = rect.posCenter
    #    w, h = rect.size
    #    cv2.rectangle(img, (cx - w//2, cy - h//2), (cx + w//2, cy + h//2), colorR, cv2.FILLED)
    #    cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)
#
    #out = img.copy()
    #alpha = 0.3
    #mask = imgNew.astype(bool)
    #out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    # Display
    #cv2.imshow("Image", out)

    cv2.imshow("Image", img)
    cv2.waitKey(1)