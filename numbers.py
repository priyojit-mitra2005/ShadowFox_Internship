#1.
def format_value(number, rep):
    return format(number, rep)

result = format_value(145, 'o')
print("Formatted result:", result)
print("Representation: Octal (base-8)")

#2.
pi     = 3.14
radius = 84           
water_per_sqm = 1.4  
area = pi * radius ** 2
total_water = area * water_per_sqm
print("Pond area:", area, "sq. meters")
print("Total water:", int(total_water), "liters")

#3.
distance = 490  
time_min = 7    
time_sec = time_min * 60 
speed = distance / time_sec
print("Distance :", distance, "meters")
print("Time     :", time_sec, "seconds")
print("Speed    :", int(speed), "m/s")