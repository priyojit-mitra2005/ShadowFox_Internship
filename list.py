justice_league = ["Superman", "Batman", "Wonder Woman",
                  "Flash", "Aquaman", "Green Lantern"]
#1.
print("Members:", len(justice_league))
print(justice_league)
#2.
justice_league.append("Batgirl")
justice_league.append("Nightwing")
print("After recruitment:", justice_league)
#3.
justice_league.remove("Wonder Woman") 
justice_league.insert(0, "Wonder Woman") 
print("With new leader:", justice_league)
#4.
justice_league.remove("Superman") 
flash_idx = justice_league.index("Flash") 
justice_league.insert(flash_idx + 1, "Superman") 
print("Aquaman & Flash separated:", justice_league)
#5.
justice_league = ["Cyborg", "Shazam", "Hawkgirl",
                  "Martian Manhunter", "Green Arrow"]

print("New Justice League:", justice_league)
#6.
justice_league.sort()
print("Sorted league:", justice_league)
print("New leader (index 0):", justice_league[0])