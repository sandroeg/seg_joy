import seg_joy as sj

if __name__ == "__main__":
    if not sj.init():
        print("Nenhum joystick encontrado.")
        exit(1)

    try:
        for tipo, valor in sj.event_stream(include_left_stick=True, include_right_stick=True):
            print(tipo, valor)
    finally:
        sj.shutdown()
