import keyboard
import pymem
import pymem.process
import time
from win32gui import GetWindowText, GetForegroundWindow
from multiprocessing import Process
from colorama import Fore, Back, Style

dwEntityList = (0x4DBD5CC)
dwForceAttack = (0x31EDB20)
dwLocalPlayer = (0xDA344C)
m_fFlags = (0x104)
m_iCrosshairId = (0x11438)
m_iTeamNum = (0xF4)
dwForceJump = (0x52673DC)
dwGlowObjectManager = (0x5305AE0)
m_iGlowIndex = (0x10488)
trigger_key = "shift"


def main():
    print(Fore.RED + "Skeptic has launched.")
    time.sleep(5)
    print(Fore.RED + '''
   _____ __              __  _     
  / ___// /_____  ____  / /_(_)____
  \__ \/ //_/ _ \/ __ \/ __/ / ___/
 ___/ / ,< /  __/ /_/ / /_/ / /__  
/____/_/|_|\___/ .___/\__/_/\___/  
              /_/                  
    CS:GO Build 1.0
                 Created By Authority
                                    github.com/lolcows
    ''')


            

def triggerbot():
    print(Fore.GREEN + "Triggerbot Enabled")
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    while True:
        if not keyboard.is_pressed(trigger_key):
            time.sleep(0.1)

        if not GetWindowText(GetForegroundWindow()) == "Counter-Strike: Global Offensive":
            continue

        if keyboard.is_pressed(trigger_key):
            player = pm.read_int(client + dwLocalPlayer)
            entity_id = pm.read_int(player + m_iCrosshairId)
            entity = pm.read_int(client + dwEntityList + (entity_id - 1) * 0x10)

            entity_team = pm.read_int(entity + m_iTeamNum)
            player_team = pm.read_int(player + m_iTeamNum)

            if entity_id > 0 and entity_id <= 64 and player_team != entity_team:
                pm.write_int(client + dwForceAttack, 6)

            time.sleep(0.006)

def esp():
    print(Fore.GREEN + "ESP Enabled")
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        
        for i in range(1, 32):  # Entities 1-32 are reserved for players.
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2:  # Terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(1))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(0))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)           # Enable glow

                elif entity_team_id == 3:  # Counter-terrorist
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(0))   # R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(0))   # G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1))  # B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x14, float(1))  # Alpha
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x28, 1)           # Enable glow
       


if __name__ == '__main__':
    main()
    proc1 = Process(target=triggerbot)
    proc1.start()
    proc2 = Process(target=esp)
    proc2.start()
