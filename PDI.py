## INCOMPLETO

import cv2

print("pressione Esc para sair a qualquer momento")

cap = cv2.VideoCapture(0)
print("abriu?", cap.isOpened())
bg = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=255, # Sensibilidade do que ele pode detectar
    detectShadows=False # Permite que o algoritmo leia as sombras e não marque-as nem como fundo nem como foreground (eu acho)
) # função que aprende a cada x frames (nesse caso, 400), o que é fundo e o que não é

while True:
    ret, frame = cap.read()
    if not ret: # caso de algum erro
        print("error at reading the camera frame")
        break

    fg_mask = bg.apply(frame, learningRate=0) # Cria uma Foregroun Mask (distingue o que é objeto do que é o fundo)
    fg_mask = cv2.medianBlur(fg_mask, 5) # remove o ruido
    
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # encontra os contornos

    for c in contours:
        if cv2.contourArea(c) <1000: # se a area que for contornada for menor que 1000 pixels, não computar (elimina mosca que passa na frente da camera)
            continue
        
        x, y, w, h = cv2.boundingRect(c) # Calcula o x, y, largura e altura da Bbox (area que delimita o objeto)
        cv2.rectangle(
            frame,
            (x , y),
            (x+w, y+h),
            (0, 120, 120),
            1

        )

    cv2.imshow("video", frame)
    cv2.imshow('frame', fg_mask)

    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()