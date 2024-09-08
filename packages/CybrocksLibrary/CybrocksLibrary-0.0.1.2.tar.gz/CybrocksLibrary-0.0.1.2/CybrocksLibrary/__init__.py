import time
import random

rltList = [
    'Loading...',
    'Hold Up...',
    'Getting the ammo...',
    'Putting down inconveniences...',
    '( -_•)▄︻テحكـ━一...',
    'gun  ̸̇̎/̸̄̿̅̎̎̅͆ ͆͆͆͆̔̿͞ ͆̅̿̄͞ ̿ ̄̇̿̚ ̎ ̎͆ ...',
    ':)...',
    'BIG CHUNGUS...',
    'Beans...',
    'The heavy is dead (˚0˚)...',
    'G was here...',
    'Sending carrier pigeons...',
    'Do not unplug the modem...',
    'Spawning sarcasm...',
    'Adjusting the flux capacitor...',
    'Downloading more RAM...',
    'Waiting for the dinosaurs to return...',
    'Making a sandwich...',
    'Summoning memes...',
    'Catching some Zs...',
    'Serving up fresh pixels...',
    'Teleporting bread...',
    'Brb, coffee break...',
    'Mining for bitcoins...',
    'Feeding the hamsters...',
    'Enabling god mode...',
    'Avoiding awkward small talk...',
    'Inserting cheesy joke...',
    'Ordering pizza...',
    'Building sandcastles...',
    'Cleaning up the internet...',
    'Barking at the server...',
    'Charging lazers...',
    'Spinning in circles...',
    'Testing gravity...',
    'Searching for meaning...',
    'Doing a little dance...',
    'Trying to find Waldo...',
    'Calling tech support...',
    'Moving some bytes...',
    'Crawling through the code...',
    'Baking cookies...',
    'Pressing random buttons...',
    'Blink twice if you\'re human...',
    'Testing the patience algorithm...',
    'Channeling Bob Ross...',
    'Clearing traffic jams...',
    'Calibrating personality...',
    'Rolling dice...',
    'Polishing the pixels...',
    'Reading the fine print...',
    'Unlocking the secrets...',
    'Poking the server...',
    'Watering the code...',
    'Making the impossible possible...',
    'Shuffling the data...',
    'Dealing with the gremlins...',
    'Tuning the algorithm...',
    'Sending virtual hugs...',
    'Feeding the virtual pets...',
    'Assembling the team...',
    'Counting stars...',
    'Sending love letters...',
    'Translating the bytes...',
    'Preparing the magic...',
    'Lifting the fog...',
    'Spinning up the engine...',
    'Searching for lost time...',
    'Untangling the web...',
    'Wrestling with bugs...',
    'Plucking the strings...',
    'Singing a lullaby...',
    'Fluffing the clouds...',
    'Training the algorithm...',
    'Chasing rainbows...',
    'Whistling a happy tune...',
    'Polishing the code...',
    'Mending the gaps...',
    'Getting the band back together...',
    'Launching confetti...',
    'Taming the wild variables...',
    'Baking virtual pies...',
    'Scribbling on the chalkboard...',
    'Transcending dimensions...',
    'Catching the last train...',
    'Finding the perfect meme...',
    'Refilling the ink...',
    'Adjusting the spotlight...',
    'Breaking the fourth wall...',
    'Harmonizing the bits...',
    'Patching the holes...',
    'Cracking the code...',
    'Playing hide and seek...',
    'Unleashing the creativity...',
    'Conducting the orchestra...',
    'Feeding the cosmic machine...',
    'Getting the jokes in line...',
    'Caring for the bytes...',
    'Throwing a digital party...',
    'Drawing the curtains...',
    'Blowing up balloons...',
    'Lighting up the fireworks...',
    'Spinning the wheel of fortune...',
    'Filling the virtual tank...',
    'Creating digital magic...',
    'Shaking the pixels...',
    'Unwrapping the gift...',
    'Bringing the code to life...',
    'Greasing the wheels...',
    'Drumming up excitement...',
    'Tickling the algorithm...',
    'Spinning the web...',
    'Weaving the story...',
    'Stirring the code...',
    'Brushing off the dust...',
    'Polishing the interface...',
    'Finding the lost key...',
    'Hunting for Easter eggs...',
    'Setting the stage...',
    'Climbing the virtual ladder...',
    'Turning the dials...',
    'Finding the missing piece...',
    'Making the magic happen...',
    'Building the dream...',
    'Catching the last pixel...',
    'Unveiling the secret...',
    'Riding the rollercoaster...',
    'Making it shine...',
    'Tuning the frequencies...',
    'Warming up the circuits...',
    'Whipping up some magic...',
    'Shaking off the bugs...',
    'Paddling through code...',
    'Inflating the pixels...',
    'Cooking up a storm...',
    'Turning up the volume...',
    'Arranging the stars...',
    'Sorting the data...',
    'Scrambling the bytes...',
    'Merging the pieces...',
    'Bridging the gaps...',
    'Hatching the plan...',
    'Spinning the threads...',
    'Brewing up some fun...',
    'Pepe the Frog is watching...',
    'Doge is cheering you on...',
    'Distracted Boyfriend is busy...',
    'Kermit is sipping tea...',
    'Grumpy Cat is unimpressed...',
    'This is fine... 🔥',
    'Nyan Cat is in space...',
    'Hide the Pain Harold is hiding...',
    'Arthur’s Fist is clenched...',
    'Expanding Brain is expanding...',
    'Rickrolling in progress...',
    'Success Kid is high-fiving...',
    'Mocking SpongeBob is mocking...',
    'Confused Nick Young is confused...',
    'Is this a pigeon? Yes...',
    'Drake Hotline Bling is uninterested...',
    'How About No is refusing...',
    'Overly Attached Girlfriend is waiting...',
    'Wojak is Wojacking...',
    'Roll Safe is thinking...',
    'Inhaling Seagull is flying...',
    'Kermit is plotting...',
    'DogeCoin to the moon...',
    'Philosoraptor is pondering...',
    'All the Feels...',
    'Trollface is trolling...',
    'Success Kid says thanks...',
    'C9 was here'
]


def randomLoadingText(amount, minTime, maxTime, console):
    for i in range(amount):
        time.sleep(random.randint(minTime, maxTime))
        yield random.choice(rltList)

#for message in randomLoadingText(7, 1, 4, 'pc'): #test
#    print(message)  


import subprocess
import pyuac

def create_wifi_network(ssid, key):
    try:
        # Set up the hosted network
        subprocess.run(["netsh", "wlan", "set", "hostednetwork", "mode=allow", "ssid=" + ssid, "key=" + key], check=True)
        # Start the hosted network
        subprocess.run(["netsh", "wlan", "start", "hostednetwork"], check=True)
        print(f"Wi-Fi network '{ssid}' created and started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def stop_wifi_network():
    try:
        subprocess.run(["netsh", "wlan", "stop", "hostednetwork"], check=True)
        print("Wi-Fi network stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def main():
    ssid = "TOTALYNOTAFAKEWIFI"
    key = "E64"
    create_wifi_network(ssid, key)
    input("Press Enter to stop the Wi-Fi network...")
    stop_wifi_network()

def start_wifi_network():
    if not pyuac.isUserAdmin():
        return(pyuac.runAsAdmin())
    else:        
        return(main()) 

#start_wifi_network() #THIS IS FOR PRANKING ONLY!!!!!! YOU WILL NOT GET FRI WIFI FROM THIS!!! AND THIS IS VERY EXPIREMENTAL!!!
    
def setupUrsina(skyColor, ws, fov):
    import usrina
    window.color = color.rgb(skyColor)
    indra = Sky() #A Hindu God of the Sky, War, Rain & Thunder
    indra.color = window.color
    walk_speed = ws
    camera.fov = fov
    
def AHamster():
    return '''⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀⠀⢀⣀⣀⣀⣀⣀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⣴⣋⣩⣍⠹⠖⠉⠁⠀⠀⠀⠀⠈⠉⠓⠟⣉⣡⣭⡙⣷⠀⠀⠀⠀
    ⠀⠀⠀⣿⢸⣏⡾⠛⠀⢀⣀⡀⠀⠀⠀⠀⢀⣠⡄⠀⠉⢻⣜⡿⣸⡇⠀⠀⠀
    ⠀⠀⠀⢻⣾⣟⣀⡀⢀⣸⣦⠝⠀⠀⠀⠀⠺⣤⣞⡀⠀⣀⣽⣷⡿⠁⠀⠀⠀
    ⠀⣠⠖⠈⠀⠀⠀⠉⠛⠫⠿⡶⠒⢾⣶⠒⠲⠿⠟⠟⠋⠁⠀⠀⠉⠲⣤⠀⠀
    ⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣶⡞⠟⣶⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⠀
    ⣟⠀⠀⠀⠀⣀⢀⠀⠀⠀⠀⠘⢿⣏⣛⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
    ⣿⠀⠀⢠⡞⢫⠙⠦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠞⡹⢳⣆⠀⠀⣸⠇
    ⠘⣧⡢⠘⡏⠀⠀⠀⠱⠄⠀⠀⠀⠀⠀⠀⠀⠀⢀⠜⠀⠀⠀⠈⡅⢠⣾⠟⠀
    ⠀⠈⢻⡷⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⢲⣿⠉⠀⠀
    ⠀⠀⣼⠃⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⢿⠀⠀⠀
    ⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀
    ⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡇⠀⠀
    ⠀⠀⠹⣧⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠀⠀⠀⠀⠀
    ⠀⠀⠀⠙⣳⣭⣐⡂⢀⠀⠀⣀⣀⣀⣀⣀⣐⣀⠄⡀⠀⣀⣀⣤⣽⡟⠀⠀⠀
    ⠀⠀⠀⢸⣇⣀⣨⣽⡿⠿⠛⠉⠉⠉⠉⠉⠉⠙⠻⢿⣭⣄⣀⣨⡷⠀⠀⠀
    ⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠁⠀⠀⠀⠀'''

#print(Hamster()) #test :)
import curses
import random

def FunkyM(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(50)  # Speed up the game by decreasing the timeout
    
    # Constants
    screen_width = curses.COLS
    screen_height = curses.LINES
    arrows = ['←', '↓', '↑', '→']
    arrow_pos = screen_width - 10  # Start position of the arrow
    arrow_speed = 2  # Speed of the arrow
    arrow_speed_increase = 0.1  # Speed increase per successful press
    arrow_target = 5  # Reference position to hit the arrow (left side)
    acceptance_radius = 3  # Acceptable range around the target position
    score = 0
    high_score = 0
    total_attempts = 0
    successful_attempts = 0
    game_over = False
    rating_display_time = 10  # Duration to show the rating
    rating_message = ""  # Initialize empty rating message
    rating_timer = 0  # Timer to control how long to display the rating

    def get_random_arrow():
        return random.choice(arrows)

    def get_rating(diff):
        if abs(diff) <= 1:
            return "Sick"
        elif abs(diff) <= 2:
            return "OK"
        else:
            return "Crap"

    current_arrow = get_random_arrow()

    while not game_over:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Score: {score} | High Score: {high_score}")
        stdscr.addstr(1, 0, f"Press the '{current_arrow}' key when the arrow is at the reference position!")
        
        # Draw the moving arrow
        stdscr.addstr(screen_height // 2, int(arrow_pos), current_arrow)
        stdscr.addstr(screen_height // 2, int(arrow_target), '|')  # Reference position indicator
        
        # Display rating message if timer is active
        if rating_timer > 0:
            stdscr.addstr(screen_height // 2 + 2, screen_width // 2 - len(rating_message) // 2, rating_message)
            rating_timer -= 1  # Decrease the rating display timer
        
        # Refresh screen
        stdscr.refresh()

        # Move the arrow
        arrow_pos -= arrow_speed
        if arrow_pos < 0:
            # Arrow has moved off the screen
            game_over = True
            break
        
        key = stdscr.getch()

        # Check if the pressed key matches the current arrow
        key_map = {curses.KEY_LEFT: '←', curses.KEY_DOWN: '↓', curses.KEY_UP: '↑', curses.KEY_RIGHT: '→'}
        if key in key_map:
            key = key_map[key]

        # Check if the user pressed the correct key at the right time
        if key == current_arrow:
            total_attempts += 1
            diff = int(arrow_pos - arrow_target)
            if abs(diff) <= acceptance_radius:
                # Successful hit
                score += 1
                successful_attempts += 1
                arrow_speed += arrow_speed_increase
                rating_message = get_rating(diff)
                rating_timer = rating_display_time
                current_arrow = get_random_arrow()
                arrow_pos = screen_width - 10
            else:
                # Wrong timing, but still pressed the correct key
                rating_message = "Missed"
                rating_timer = rating_display_time
                current_arrow = get_random_arrow()
                arrow_pos = screen_width - 10
        elif key != -1:
            # Wrong key pressed, game over
            game_over = True

    accuracy = (successful_attempts / total_attempts * 100) if total_attempts > 0 else 0

    stdscr.clear()
    stdscr.addstr(screen_height // 2, screen_width // 2 - len("Game Over!") // 2, "Game Over!")
    stdscr.addstr(screen_height // 2 + 1, screen_width // 2 - len(f"Final Score: {score}") // 2, f"Final Score: {score}")
    high_score = max(score, high_score)
    stdscr.addstr(screen_height // 2 + 2, screen_width // 2 - len(f"High Score: {high_score}") // 2, f"High Score: {high_score}")
    stdscr.addstr(screen_height // 2 + 3, screen_width // 2 - len(f"Accuracy: {accuracy:.2f}%") // 2, f"Accuracy: {accuracy:.2f}%")
    stdscr.refresh()
    stdscr.getch()

def Funky():
    return(curses.wrapper(FunkyM))
#Funky()

fake_hacking_prompts = [
    "Establishing secure connection to remote server...",
    "Bypassing firewall security protocols...",
    "Injecting SQL payload into vulnerable database...",
    "Cracking 128-bit AES encryption...",
    "Decrypting intercepted data packets...",
    "Compiling exploit for buffer overflow vulnerability...",
    "Scanning network for open ports and vulnerabilities...",
    "Brute-forcing admin login credentials...",
    "Executing privilege escalation to obtain root access...",
    "Installing keylogger on target system...",
    "Spoofing MAC address to bypass network restrictions...",
    "Retrieving hashed passwords from compromised database...",
    "Initiating DDoS attack on target IP address...",
    "Uploading malware to target server...",
    "Exfiltrating confidential data from secured directory...",
    "Disabling security cameras and system logs...",
    "Evading detection by anti-virus software...",
    "Erasing all traces from server logs...",
    "Decrypting SSH key to gain access to remote machine...",
    "Dumping memory contents for analysis...",
    "Analyzing vulnerability in server's authentication system...",
    "Injecting reverse shell payload into server process...",
    "Decrypting intercepted VPN traffic...",
    "Phishing for credentials via compromised email...",
    "Bypassing two-factor authentication...",
    "Mapping network topology of target organization...",
    "Creating rogue access point to intercept traffic...",
    "Infiltrating dark web marketplaces for intel...",
    "Analyzing blockchain transactions for vulnerabilities...",
    "Modifying DNS records to redirect traffic...",
    "Monitoring real-time network traffic...",
    "Cloning RFID tags for unauthorized access...",
    "Fuzzing application input for hidden vulnerabilities...",
    "Exploiting zero-day vulnerability in software...",
    "Overwriting MBR to prevent system boot...",
    "Hijacking session tokens for admin privileges...",
    "Scraping social media for user metadata...",
    "Exploiting XSS vulnerability to inject malicious scripts...",
    "Intercepting and decrypting SSL/TLS communication...",
    "Modifying registry keys to maintain persistence...",
    "Compromising IoT devices on the network...",
    "Setting up remote access backdoor...",
    "Scanning for outdated software versions with known exploits...",
    "Executing ransomware payload on target system..."
]

def AFakeHackPrank():
    while True:
        time.sleep(random.uniform(0.05, 0.5))
        yield random.choice(fake_hacking_prompts)

def BFakeHackPrank():
    for message in AFakeHackPrank():
        try:
            from colorama import Fore
        except ImportError:
            print("Module 'colorama' not found. Please install it.")
        yield Fore.GREEN + message


def FakeHackPrank():
    for msg in BFakeHackPrank():
        print(msg)

#FakeHackPrank()
        
