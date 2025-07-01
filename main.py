import cv2
from ultralytics import YOLO
from scripts.mapping import material_mapping
import serial
import time

# --- Configuração Serial ---
# Substitua 'COM3' pela porta serial do seu Arduino (ex: '/dev/ttyACM0' no Linux, 'COM3' no Windows)
# Você pode verificar a porta no IDE do Arduino, em Ferramentas > Porta.
try:
    ser = serial.Serial('COM3', 9600, timeout=1) # 9600 é a taxa de baud rate, deve ser a mesma no Arduino
    print("Conexão serial estabelecida.")
    time.sleep(2) # Pequena pausa para a conexão serial se estabelecer completamente
except serial.SerialException as e:
    print(f"Erro ao abrir a porta serial: {e}")
    print("Certifique-se de que o Arduino está conectado e a porta COM está correta.")
    ser = None # Define ser como None para evitar erros posteriores

# Carrega o modelo treinado
model = YOLO("best.pt")

# Inicia a captura de vídeo pela webcam
cap = cv2.VideoCapture(0)

# Mapeamento de materiais para comandos de servo
servo_commands = {
    'Metal': 'M',
    'Plastic': 'P',
    'Paper': 'R'
}

# Variáveis para controlar o fluxo de comandos para o Arduino
action_in_progress = False
last_action_time = 0
# Tempo total para o servo abrir, esperar e fechar (5s de espera + tempo de movimento)
# Aumente um pouco para garantir que o ciclo anterior termine.
COOLDOWN_TIME = 6.5 # segundos

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    if not ret:
        break

    results = model(frame)
    current_detection_to_act_on = None # Armazena a primeira detecção válida para agir

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = model.names[int(box.cls)]
            material = material_mapping.get(label, "Outro")  # Pega o tipo de material

            conf = float(box.conf)
            if conf > 0.5:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{material} {conf * 100:.1f}%", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                # Se for uma das classes que controlam um servo e ainda não decidimos qual agir
                if material in servo_commands and current_detection_to_act_on is None:
                    current_detection_to_act_on = material # Prioriza a primeira detecção válida

    # Lógica para enviar comando ao Arduino
    if ser and current_detection_to_act_on:
        current_time = time.time()
        if not action_in_progress and (current_time - last_action_time > COOLDOWN_TIME):
            command_char = servo_commands[current_detection_to_act_on]
            try:
                ser.write(command_char.encode('utf-8')) # Envia o caractere específico para o Arduino
                print(f"Comando '{command_char}' enviado para o Arduino para: {current_detection_to_act_on}")
                action_in_progress = True
                last_action_time = current_time
            except serial.SerialException as e:
                print(f"Erro ao enviar comando serial: {e}")
                ser = None # Desconecta se houver erro
    elif action_in_progress and (time.time() - last_action_time > COOLDOWN_TIME):
        # Reseta o flag se o tempo de cooldown passou e nenhuma nova detecção válida foi processada
        action_in_progress = False


    cv2.imshow("Detecção", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()
    print("Conexão serial fechada.")
