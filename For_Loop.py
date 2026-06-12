#1.
import random
rolls = []
count_six = 0
count_one = 0
consec_six = 0
for i in range(20):
    roll = random.randint(1, 6)
    rolls.append(roll)
    if roll == 6: count_six += 1
    if roll == 1: count_one += 1
    if i > 0 and roll == 6 and rolls[i-1] == 6:
        consec_six += 1

print("Rolls:", rolls)
print("Sixes:", count_six)
print("Ones:", count_one)
print("Consecutive 6s:", consec_six)

#2.
total = 100
done = 0
while done < total:
    done += 10
    print(f"You completed {done} jumping jacks!")
    if done == total:
        print("Congratulations! You completed the workout.")
        break
    tired = input("Are you tired? (yes/no): ").lower()
    if tired in ["yes", "y"]:
        skip = input("Skip remaining? (yes/no): ").lower()
        if skip in ["yes", "y"]:
            print(f"You completed a total of {done} jumping jacks.")
            break
    else:
        remaining = total - done
        print(f"{remaining} jumping jacks remaining!")