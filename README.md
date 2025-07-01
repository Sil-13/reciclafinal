Visão Geral da Solução com Múltiplos Servos
Código Python (no computador):

Manterá a comunicação serial com o Arduino.

Ao detectar as classes 'Metal', 'Plastic' ou 'Paper', enviará um caractere específico diferente para cada classe (ex: 'M' para Metal, 'P' para Plastic, 'R' para Paper).

A lógica de "cooldown" será mantida para garantir que apenas um movimento de servo ocorra por vez, aguardando o ciclo completo (abrir, esperar, fechar) antes de processar uma nova detecção.

Código Arduino (no Arduino Uno):

Declarará e controlará três objetos Servo.

Lerá os dados recebidos pela porta serial.

Quando receber o caractere correspondente a uma classe, movimentará o servo específico dessa classe para 70 graus, aguardará 5 segundos e o retornará à posição inicial (0 graus).




Principais Mudanças no Código Python:

servo_commands Dicionário: Um dicionário servo_commands foi adicionado para mapear os nomes das classes ('Metal', 'Plastic', 'Paper') para caracteres de comando ('M', 'P', 'R') que serão enviados ao Arduino.

Lógica de Cooldown Aprimorada: A variável action_in_progress e last_action_time garantem que, mesmo que múltiplas detecções ocorram, apenas um comando seja enviado por vez, e um novo comando só será enviado após o ciclo completo do servo anterior ter terminado (definido por COOLDOWN_TIME).

current_detection_to_act_on: Esta variável garante que, em caso de múltiplas detecções na mesma moldura, apenas a primeira detecção relevante acione um comando, evitando confusão.

command_char.encode('utf-8'): O caractere é codificado para bytes antes de ser enviado via serial.

Código para Arduino Uno (para 3 Servos)
Este código controlará os três servo motores.

Pinos a Usar no Arduino Uno:

Para cada servo motor, você precisará de um pino digital PWM. No Arduino Uno, os pinos PWM são 3, 5, 6, 9, 10 e 11.

Servo Metal: Conecte o pino de sinal ao Pino Digital 9.

Servo Plastic: Conecte o pino de sinal ao Pino Digital 10.

Servo Paper: Conecte o pino de sinal ao Pino Digital 11.

Fonte de Alimentação dos Servos:
Como antes, é altamente recomendado alimentar os servos externamente com uma fonte de 5V e GND comum com o Arduino, especialmente porque você terá três servos agora. Conecte o VCC de todos os servos à fonte externa de 5V e o GND de todos os servos ao GND da fonte externa E ao GND do Arduino.

Principais Mudanças no Código Arduino:

Três Objetos Servo: servoMetal, servoPlastic e servoPaper são declarados.

Pinos Dedicados: Cada servo é associado a um pino PWM diferente (pinMetal, pinPlastic, pinPaper).

switch Statement: Em vez de um simples if, um switch é usado para verificar qual caractere de comando foi recebido ('M', 'P', 'R') e chamar a função moveServo para o servo correspondente.

Função moveServo: Uma função auxiliar foi criada para encapsular a lógica de movimento (abrir, esperar, fechar), tornando o código mais limpo e reutilizável para cada servo.

Como Montar e Testar (para 3 Servos)
Conexões do Arduino:

Servo Metal: Sinal no Pino Digital 9.

Servo Plastic: Sinal no Pino Digital 10.

Servo Paper: Sinal no Pino Digital 11.

Alimentação dos Servos: Conecte o VCC (fio vermelho) de TODOS os servos a uma fonte de alimentação externa de 5V. Conecte o GND (fio marrom/preto) de TODOS os servos ao GND da fonte externa E ao GND do Arduino. Esta é uma etapa crucial para evitar sobrecarregar o Arduino.

Carregar o Código no Arduino:

Abra o IDE do Arduino.

Copie e cole o código do Arduino fornecido acima.

Selecione sua placa (Arduino Uno) e as portas seriais corretas em Ferramentas > Placa e Ferramentas > Porta.

Clique em "Carregar" para enviar o código para o Arduino.

Executar o Código Python:

Certifique-se de que o Arduino está conectado ao seu computador e que você substituiu 'COM3' no código Python pela porta serial correta do seu Arduino.

Execute o script Python.

Agora, ao detectar um objeto de "Metal", "Plastic" ou "Paper", o servo motor correspondente se moverá, esperará e retornará à posição inicial, aguardando uma nova detecção.
