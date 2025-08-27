import seg_joy as sj

if __name__ == "__main__":
    if not sj.init():
        print("Nenhum joystick encontrado.")
        exit(1)

    try:
        # Ative os sticks conforme precisar; ajuste right_axes se seu SO/controle variar
        for tipo, valor in sj.event_stream(
            include_left_stick=True,
            include_right_stick=True        ):
            if tipo == sj.BTN_DOWN:
                print(f"Botão {valor} PRESSIONADO")
            elif tipo == sj.BTN_UP:
                print(f"Botão {valor} SOLTO")
            elif tipo == sj.DPAD:
                print(f"D-Pad: {valor}")  # (x,y) em {-1,0,1}
            elif tipo == sj.LEFT_STK:
                x, y = valor
                print(f"Left stick:  x={x:+.3f} y={y:+.3f}")
            elif tipo == sj.RIGHT_STK:
                x, y = valor
                print(f"Right stick: x={x:+.3f} y={y:+.3f}")

    finally:
        sj.shutdown()
