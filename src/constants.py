"""
Constans for the proyect

All range constants are made like: [i, j] and not [i, j) as range() function performs.
"""
"""
////////////////////////////////////////////////////////////////////////////////////////////
- General
////////////////////////////////////////////////////////////////////////////////////////////
"""

K = 40 # Optical wavelenghts


"""
////////////////////////////////////////////////////////////////////////////////////////////
- Input
////////////////////////////////////////////////////////////////////////////////////////////
"""
# 2 <= N <= 200
N_BOUND_LOW = 2
N_BOUND_UPP = 200
N_BOUND_RANGE = range(N_BOUND_LOW, N_BOUND_UPP + 1)

# 1 <= M <= 1000
M_BOUND_LOW = 1
M_BOUND_UPP = 1000

# Number of channel conversions opp
# 0 <= P_i <= 20
CHANNEL_CONV_OPP_LOWER_BOUND = 0
CHANNEL_CONV_OPP_UPP_BOUND = 20

# The number of services initially running on the graph
# 1 <= J <= 5000

No_SERVICES_INIT_MIN = 1
No_SERVICES_INIT_MIN = 5000

# Service value
# 0 <= V <= 100.000

SERVICE_VALUE_MIN = 0
SERVICE_VALUE_MAX = 100_000
