import subprocess, os, json, time, glob
status = {"folder":"mp4", "index":0,"pos_mm":0} # pos in minutes
player_dir = os.path.dirname(os.path.realpath(__file__))
media = {
    "mp4":sorted( glob.glob( os.path.join( player_dir, "media","mp4","*.mp4" ) ) ),
    "flv":sorted( glob.glob( os.path.join( player_dir, "media","flv","*.flv" ) ) )
}

def save_status():
    with open(os.path.join(player_dir,"status.json"), "w") as f:
        json.dump(status, f)

if __name__=="__main__":
    # initialisation check for status.json and create one if empty
    if os.path.isfile(os.path.join(player_dir,"status.json")) is not True: 
        with open(os.path.join(player_dir,"status.json"), "x") as f:
            json.dump(status, f) 
    else: 
        with open(os.path.join(player_dir,"status.json"), "r") as f:
            status = json.load(f)
        print(f"Loaded status from status.json, status={status}")

    # start playing from memory
    index = status["index"]
    folder = status["folder"]
    initial_pos = status["pos_mm"]
    media_path = os.path.join(player_dir, "media", media[folder][index])
    try: 
        process = subprocess.Popen(f"omxplayer -o hdmi -l 00:{initial_pos}:00 {media_path}".encode("gbk").split(), stdout=subprocess.PIPE)
        print("Running command ", f"omxplayer -o hdmi -l 00:{initial_pos}:00 {media_path}")
    except Exception as e: 
        print(e) 
    start_time = time.time()

    # routine
    while True: 
        if process.poll() is None: 
            # still playing 
            elapsed_mm = int( (time.time() - start_time) // 60 )
            pos_mm = initial_pos + elapsed_mm
            if status["pos_mm"] != pos_mm:
                status["pos_mm"] = pos_mm
                save_status() 
        else: 
            # finished media so increment and play next
            index += 1 
            if index >= len( media[folder] ):
                # swap folder 
                folder = "flv" if folder == "mp4" else "mp4"
                index = 0 
            status["folder"] = folder 
            status["index"] = index
            status["pos_mm"] = 0
            save_status()
            media_path = os.path.join(player_dir, "media", media[folder][index])
            try:
                process = subprocess.Popen(f"omxplayer -o hdmi -l 00:00:00 {media_path}".split(), stdout=subprocess.PIPE)
                print("Running command ", f"omxplayer -o hdmi -l 00:00:00 {media_path}")
            except Exception as e: 
                print(e)
            start_time = time.time()
            initial_pos = 0
        time.sleep(0.5)
