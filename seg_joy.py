import pygame
import time
from typing import Iterator, List, Tuple, Union, Optional

# Códigos de evento (enum simples)
BTN_DOWN = 0      # (0, botao)        -> botão pressionado
BTN_UP   = 1      # (1, botao)        -> botão solto
LEFT_STK = 2      # (2, (x,y))        -> left stick contínuo
DPAD     = 3      # (3, (x,y))        -> D-pad (hat) -1/0/1
RIGHT_STK= 4      # (4, (x,y))        -> right stick contínuo

EventValue = Union[int, Tuple[int, int], Tuple[float, float]]
Event = Tuple[int, EventValue]

def init() -> bool:
    """Inicializa pygame e o primeiro joystick disponível."""
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        return False
    joy = pygame.joystick.Joystick(0)
    joy.init()
    return True

def shutdown() -> None:
    """Finaliza pygame/joystick."""
    try:
        pygame.joystick.quit()
    finally:
        pygame.quit()

def poll_events() -> List[Event]:
    """Coleta eventos discretos do joystick (botões e D-pad)."""
    out: List[Event] = []
    for e in pygame.event.get():
        if e.type == pygame.JOYBUTTONDOWN:
            out.append((BTN_DOWN, e.button))
        elif e.type == pygame.JOYBUTTONUP:
            out.append((BTN_UP, e.button))
        elif e.type == pygame.JOYHATMOTION:
            out.append((DPAD, e.value))  # (x,y) em {-1,0,1}
    return out

def _emit_stick(
    joy: pygame.joystick.Joystick,
    axes: Tuple[int, int],
    last: Tuple[Optional[float], Optional[float]],
    eps: float,
    min_interval: float,
    last_emit_time: float,
    code: int,
) -> Tuple[Optional[Event], Tuple[Optional[float], Optional[float]], float]:
    """Lê (x,y) de um par de eixos e decide se emite evento contínuo."""
    lx_idx, ly_idx = axes
    if joy.get_numaxes() <= max(lx_idx, ly_idx):
        return (None, last, last_emit_time)

    x = joy.get_axis(lx_idx)
    y = joy.get_axis(ly_idx)

    last_x, last_y = last
    now = time.time()
    first = (last_x is None or last_y is None)
    changed = (not first) and (abs(x - last_x) > eps or abs(y - last_y) > eps)
    spaced = (now - last_emit_time) >= min_interval

    if first or (changed and spaced):
        return ((code, (x, y)), (x, y), now)
    return (None, last, last_emit_time)

def event_stream(
    include_left_stick: bool = False,
    include_right_stick: bool = False,
    left_axes: Tuple[int, int] = (0, 1),
    right_axes: Tuple[int, int] = (2, 3),
    left_eps: float = 0.02,
    right_eps: float = 0.02,
    left_interval: float = 0.02,
    right_interval: float = 0.02,
    sleep_ms: int = 1,
) -> Iterator[Event]:
    """
    Gerador contínuo de eventos do joystick.

    Sempre produz:
      (BTN_DOWN, botao)
      (BTN_UP, botao)
      (DPAD, (x,y))

    Opcionalmente produz continuamente:
      (LEFT_STK,  (x,y))  se include_left_stick=True
      (RIGHT_STK, (x,y))  se include_right_stick=True

    Parâmetros:
      left_axes/right_axes   -> índices (x,y) dos eixos para cada stick.
                                Padrão comum SDL2/Xbox: left (0,1), right (3,4)
                                (em alguns sistemas pode ser (2,3) para o right)
      *_eps                  -> sensibilidade mínima para considerar mudança
      *_interval             -> intervalo mínimo (seg) entre emissões
      sleep_ms               -> descanso por iteração
    """
    if pygame.joystick.get_count() == 0:
        raise RuntimeError("Chame seg_joy.init() antes de usar event_stream().")

    joy = pygame.joystick.Joystick(0)

    last_left: Tuple[Optional[float], Optional[float]] = (None, None)
    last_right: Tuple[Optional[float], Optional[float]] = (None, None)
    last_left_emit = 0.0
    last_right_emit = 0.0

    while True:
        # Eventos discretos (botões e D-pad)
        for ev in poll_events():
            yield ev

        # Emissão contínua dos sticks
        if include_left_stick:
            ev, last_left, last_left_emit = _emit_stick(
                joy, left_axes, last_left, left_eps, left_interval, last_left_emit, LEFT_STK
            )
            if ev is not None:
                yield ev

        if include_right_stick:
            ev, last_right, last_right_emit = _emit_stick(
                joy, right_axes, last_right, right_eps, right_interval, last_right_emit, RIGHT_STK
            )
            if ev is not None:
                yield ev

        pygame.time.wait(sleep_ms)
