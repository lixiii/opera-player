import os, glob 

input("Run this in the correct mp4/flv directory ONLY! Press enter to continue...")

m = sorted(glob.glob("*.mp4"))
with open("lists.txt","a") as f:
    for e in m:
        name = e.split(".")[0] + ".mp4" 
        # os.rename(e,name) 
        print(f"Renaming {e}")
        f.write(name + "<--" + e + "\n")


