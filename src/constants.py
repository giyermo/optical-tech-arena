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
M_BOUND_RANGE = range(M_BOUND_LOW, M_BOUND_UPP + 1)

# Number of channel conversions opp
# 0 <= P_i <= 20
CHANNEL_CONV_OPP_LOWER_BOUND = 0
CHANNEL_CONV_OPP_UPP_BOUND = 20
CHANNEL_CONV_OPP_UPP_RANGE = range(CHANNEL_CONV_OPP_LOWER_BOUND, CHANNEL_CONV_OPP_UPP_RANGE + 1)

# The number of services initially running on the graph
# 1 <= J <= 5000

NUM_SERVICES_INIT_MIN = 1
NUM_SERVICES_INIT_MAX = 5000
NUM_SERVICES_INIT_RANGE = range(NUM_SERVICES_INIT_MIN, NUM_SERVICES_INIT_MAX + 1)

# Service value
# 0 <= V <= 100.000

SERVICE_VALUE_MIN = 0
SERVICE_VALUE_MAX = 100_000
SERVICE_VALUE_RANGE = range(SERVICE_VALUE_MIN, SERVICE_VALUE_MAX + 1)

"""
////////////////////////////////////////////////////////////////////////////////////////////
- Scenarios
////////////////////////////////////////////////////////////////////////////////////////////
"""
# Number of failure
# 0 <= T_1 <= 30
T_1_MIN = 0
T_1_MAX = 30
# Failures
# 0 <= T_1 <= 60
T_2_MIN = 0
T_2_MAX = 60
