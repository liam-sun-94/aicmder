


HEARTBEAT_LIVENESS = 5     # 3..5 is reasonable
HEARTBEAT_INTERVAL = 1.0   # Seconds

#  Paranoid Pirate Protocol constants
PPP_READY = b"\x01"      # Signals worker is ready
PPP_HEARTBEAT = b"\x02"  # Signals worker heartbeat



INTERVAL_INIT = 1
INTERVAL_MAX = 32


##############################
HEARTBEAT_INTERVAL = 10
# only for 3 times while losing receiving heartbeat
HEARTBEAT_LIVENESS = 3