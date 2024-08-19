import cv2
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

buton_basildi = False
devam_etmek_istiyor = None

def el_hareketi_tanima(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
    
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
    
    if thumb_tip.y > thumb_ip.y and index_tip.y > index_mcp.y and \
       middle_tip.y > middle_mcp.y and ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y:
        return "taş"
    
    elif index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y and \
         ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y:
        return "makas"
    
    elif thumb_tip.y < thumb_ip.y and index_tip.y < index_mcp.y and \
         middle_tip.y < middle_mcp.y and ring_tip.y < ring_mcp.y and pinky_tip.y < pinky_mcp.y:
        return "kağıt"
    
    return "belirlenemedi"

def mouse_callback(event, x, y, flags, param):
    global buton_basildi, devam_etmek_istiyor
    if event == cv2.EVENT_LBUTTONDOWN:
        if 50 <= x <= 250 and 400 <= y <= 450:
            buton_basildi = True
            devam_etmek_istiyor = True
        elif 300 <= x <= 500 and 400 <= y <= 450:
            buton_basildi = True
            devam_etmek_istiyor = False

def tas_kagit_makas_goruntu():
    global buton_basildi, devam_etmek_istiyor

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while True:
            # Karşılama mesajı göster
            while True:
                success, image = cap.read()
                if not success:
                    break

                image = cv2.flip(image, 1)
                cv2.putText(image, "Tas Kagit Makas Oyununa Hos Geldiniz!", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(image, "Kurallar:", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, "1.Kamera karsisinda el hareketinizi yapin.", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, "2.ilk iki galibiyete ulasan kazanir.", (50, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, "3.Oyun sonunda devam etmek isteyip istemediginiz sorulacak.", (50, 250), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, "4.Cikmak icin ESC tusuna basin.", (50, 300), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(image, "Oynamak icin herhangi bir tusa basin...", (50, 400), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                cv2.namedWindow('Taş Kağıt Makas', cv2.WINDOW_NORMAL)
                cv2.resizeWindow('Taş Kağıt Makas', 854, 480)
                cv2.imshow('Taş Kağıt Makas', image)

                if cv2.waitKey(5) & 0xFF != 255:
                    break

            oyuncu_skoru = 0
            bilgisayar_skoru = 0

            cv2.setMouseCallback('Taş Kağıt Makas', mouse_callback)

            while cap.isOpened():
                print(f"Skor - Oyuncu: {oyuncu_skoru}, Bilgisayar: {bilgisayar_skoru}")
                start_time = time.time()
                son_hareket = "belirlenemedi"

                while time.time() - start_time <= 5:
                    success, image = cap.read()
                    if not success:
                        print("Kamera görüntüsü alınamıyor.")
                        break

                    image = cv2.flip(image, 1)
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_rgb)

                    remaining_time = int(5 - (time.time() - start_time))
                    cv2.putText(image, f"Kalan Sure: {remaining_time} saniye", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            hareket = el_hareketi_tanima(hand_landmarks)
                            if hareket != "belirlenemedi":
                                son_hareket = hareket

                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    cv2.imshow('Taş Kağıt Makas', image)

                    if cv2.waitKey(5) & 0xFF == 27:
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                if son_hareket == "belirlenemedi":
                    print("El hareketiniz tanımlanamadı. Lütfen tekrar deneyin.")
                else:
                    print(f"Sizin seçiminiz: {son_hareket}")
                    bilgisayar_secimi = random.choice(["taş", "kağıt", "makas"])
                    print(f"Bilgisayarın seçimi: {bilgisayar_secimi}")

                    if son_hareket == bilgisayar_secimi:
                        print("Bu tur berabere!\n")
                    elif (son_hareket == "taş" and bilgisayar_secimi == "makas") or \
                         (son_hareket == "kağıt" and bilgisayar_secimi == "taş") or \
                         (son_hareket == "makas" and bilgisayar_secimi == "kağıt"):
                        print("Bu turu kazandınız!\n")
                        oyuncu_skoru += 1
                    else:
                        print("Bu turu bilgisayar kazandı!\n")
                        bilgisayar_skoru += 1

                if oyuncu_skoru == 2 or bilgisayar_skoru == 2:
                    break

            print(f"Oyun Bitti! Skor - Oyuncu: {oyuncu_skoru}, Bilgisayar: {bilgisayar_skoru}")
            if oyuncu_skoru == 2:
                print("Tebrikler, oyunu kazandınız!")
            else:
                print("Bilgisayar oyunu kazandı!")

            while True:
                success, image = cap.read()
                if not success:
                    break

                image = cv2.flip(image, 1)

                # Kullanıcıya soru
                cv2.putText(image, "Devam etmek istiyor musunuz?", (50, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(image, (50, 400), (250, 450), (0, 255, 0), -1)
                cv2.putText(image, 'Evet', (100, 435), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.rectangle(image, (300, 400), (500, 450), (0, 0, 255), -1)
                cv2.putText(image, 'Hayir', (350, 435), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.imshow('Taş Kağıt Makas', image)

                if cv2.waitKey(5) & 0xFF == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    return

                if buton_basildi:
                    buton_basildi = False
                    break

            if devam_etmek_istiyor:
                bilgisayar_devam = random.choice([True, False])
                print(f"Bilgisayar oyuna devam etmek istiyor mu? {'Evet' if bilgisayar_devam else 'Hayir'}")

                if not bilgisayar_devam:
                    print("Bilgisayar oyuna devam etmek istemedi. Oyun bitti.")
                    break
            else:
                print("Kullanıcı oyuna devam etmek istemedi. Oyun bitti.")
                break

    cap.release()
    cv2.destroyAllWindows()

tas_kagit_makas_goruntu()
