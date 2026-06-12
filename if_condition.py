#1.
height = float(input("Enter height in meters: "))
weight = float(input("Enter weight in kilograms: "))
bmi = weight / (height ** 2)
if bmi >= 30:
    print("Obesity")
elif bmi >= 25:
    print("Overweight")
elif bmi >= 18.5:
    print("Normal")
else:
    print("Underweight")

#2.
Australia = ["Sydney", "Melbourne", "Brisbane", "Perth"]
UAE       = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"]
India      = ["Mumbai", "Bangalore", "Chennai", "Delhi"]

city = input("Enter a city name: ")

if city in Australia:
    print(city, "is in Australia")
elif city in UAE:
    print(city, "is in UAE")
elif city in India:
    print(city, "is in India")
else:
    print(city, "is not in our database")

#3.
Australia = ["Sydney", "Melbourne", "Brisbane", "Perth"]
UAE       = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman"]
India      = ["Mumbai", "Bangalore", "Chennai", "Delhi"]
def get_country(city):
    if city in Australia: return "Australia"
    elif city in UAE: return "UAE"
    elif city in India: return "India"
    else: return None
city1 = input("Enter the first city: ")
city2 = input("Enter the second city: ")
c1, c2 = get_country(city1), get_country(city2)
if c1 and c2 and c1 == c2:
    print("Both cities are in", c1)
elif c1 and c2:
    print("They don't belong to the same country")
else:
    print("One or both cities not found")