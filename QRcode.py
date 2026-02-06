import cv2
import numpy as np
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)
last_qr = None

print("pressione Esc para sair a qualquer momento")

while True:
    ret, frame = cap.read()
    if not ret:
        break # se a camera falhar, fechar

    decoded_objects = decode(frame) # módulo do pyzbar para decodificar o qrcode

    if decoded_objects:
        for obj in decoded_objects:
            data = obj.data.decode("utf-8")

            if data != last_qr: # controle pra ele não pintar a decodificação pra sempre
                print("--> Data: ", data) # printar no terminal o que o qr code diz
                last_qr = data

            points = obj.polygon # define objeto como poligono e relaciona os valores (x1,y1), (x2,y2), (x3,y3), (x4,y4) a ele.
            pts = np.array([(p.x, p.y) for p in points], dtype=np.int32) #converte a lista de pontos detectados pelo pyzbar pra uma matriz que vai ser lida pelo numpy
            pts = pts.reshape((-1, 1, 2)) # formata o array do numpy pra o padrão que o opencv consegue identificar (N, 1, 2) -> N = numero de pontos, 1 = contorno, 2 = x,y (N aqui é -1 pra calcular automaticamente)
            if len(points) > 4: # as vezes o pyzbar detecta mais de 4 pontos
                hull = cv2.convexHull(pts)
                cv2.polylines(frame, [hull], True, (0, 0, 255), 2) # identifica o menor poligono que encaixe os mais de 4 pontos
            else:
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2) # desenha as linhas ao redor do objeto 

            cv2.putText(frame, obj.data.decode("utf-8"), (pts[0][0][0], pts[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) #poe o texto
            

    cv2.imshow("Qrcode", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()