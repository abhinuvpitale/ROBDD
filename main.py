from ROBDD import ROBDD,Apply_ROBDD
import time
# Init timer
start_time = time.time()
# Create the ROBDD object
ROBDD1 = ROBDD(1,switch=4)
# Display time taken for the object to be created
print('Time is '+str(time.time()-start_time))

# Satcount
count = ROBDD1.satCount()
print('Count of Satisfying Conditions is (SatCount) -> '+str(count))

# AnySat
anySatX = ROBDD1.anySat(None)
print('One of the satisfying conditions is (AnySat) -> '+str(anySatX))

# Restrict
ROBDD1.restrict(None,1,0)

# Create another ROBDD
ROBDD2 = ROBDD(3,switch=1)
ROBDD_Applied = Apply_ROBDD(3)

# Apply
ROBDD_Applied.apply('and',ROBDD1,ROBDD2)
print('End of Program!')