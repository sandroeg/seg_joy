# Seg_joy (Python + pygame)

Uma biblioteca simples em Python para capturar eventos de joystick/controle usando **pygame**.
Serve como modelo para estudo, ensino e futuros projetos.

## 🚀 Recursos
- Captura de:
  - Botões (pressionado/solto)
  - D-Pad (setas/direcional digital)
  - Left stick (analógico esquerdo)
  - Right stick (analógico direito)
- Interface limpa: eventos retornados como tuplas `(tipo, valor)`
- Configurável: deadzone, intervalo mínimo, mapeamento de eixos
- Compatível com Windows e Linux

## 📦 Instalação
```bash
git clone https://github.com/sandroeg/seg_joy.git
cd seg_joy
pip install -r requirements.txt
