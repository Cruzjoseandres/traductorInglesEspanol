import cv2
import pytesseract
from googletrans import Translator
from gtts import gTTS
import pygame
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

cuadro = 100


def extraer_y_traducir_texto(frame, idioma_origen='eng', idioma_destino='es'):
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar texto según idioma origen (eng para inglés, spa para español)
    texto_extraido = pytesseract.image_to_string(gris, lang=idioma_origen).strip()
    print(f"📄 Texto en {'inglés' if idioma_origen == 'eng' else 'español'} detectado:\n", texto_extraido)

    if texto_extraido:
        traductor = Translator()
        try:
            traduccion = traductor.translate(texto_extraido,
                                            src='en' if idioma_origen == 'eng' else 'es',
                                            dest='es' if idioma_destino == 'es' else 'en')
            texto_traducido = traduccion.text

            print(f"\n🌐 Traducción al {'español' if idioma_destino == 'es' else 'inglés'}:\n", texto_traducido)

            # Leer la traducción
            tts = gTTS(text=texto_traducido, lang=idioma_destino)
            tts.save("voz_traducida.mp3")
            pygame.mixer.init()
            pygame.mixer.music.load("voz_traducida.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            os.remove("voz_traducida.mp3")
        except Exception as e:
            print(f"Error en la traducción: {e}")
            print("Consejo: Intenta instalar googletrans==4.0.0-rc1")
    else:
        print("⚠️ No se detectó texto legible.")


while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.rectangle(frame, (cuadro, cuadro), (640 - cuadro, 480 - cuadro), (0, 255, 0), 2)
    cv2.putText(frame, "t: ingles->español | e: español->ingles | ESC: salir", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Traductor de Texto en Vivo", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    elif key == ord('t'):  # Traducir de inglés a español
        roi = frame[cuadro:480 - cuadro, cuadro:640 - cuadro]
        extraer_y_traducir_texto(roi, idioma_origen='eng', idioma_destino='es')
    elif key == ord('e'):  # Traducir de español a inglés
        roi = frame[cuadro:480 - cuadro, cuadro:640 - cuadro]
        extraer_y_traducir_texto(roi, idioma_origen='spa', idioma_destino='en')

cap.release()
cv2.destroyAllWindows()