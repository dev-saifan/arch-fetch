import os
import re
import shutil

def get_system_info():
    """Gathers system specs, dynamically fetching real RAM and CPU while keeping your layout."""
    # 1. Simplify the GPU name exactly as requested
    gpu_name = "integrated graphics"
    
    # 2. Extract clean WM Name (Drop trailing parentheses like (Wayland))
    wm_env = os.environ.get("XDG_CURRENT_DESKTOP", "Hyprland")
    if "(" in wm_env:
        wm_env = wm_env.split("(")[0].strip()

    # 3. Pull actual user metrics
    username = os.environ.get("USER", "user")
    hostname = os.uname().nodename if hasattr(os, "uname") else "linux"
    
    # Dynamically fetch real CPU model
    cpu_model = "Intel Pentium G2020 @ 2x 2.9GHz"
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if "model name" in line:
                    cpu_model = line.split(":")[1].strip()
                    break
    except Exception:
        pass

    # Dynamically fetch real RAM usage
    ram_str = "4225MiB / 5812MiB"
    try:
        mem_total = 0
        mem_available = 0
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem_total = int(line.split()[1])
                elif line.startswith("MemAvailable:"):
                    mem_available = int(line.split()[1])
        if mem_total > 0:
            total_mib = mem_total / 1024
            used_mib = (mem_total - mem_available) / 1024
            ram_str = f"{used_mib:.0f}MiB / {total_mib:.0f}MiB"
    except Exception:
        pass
    
    # Build the data block
    stats = [
        (f"{username}@{hostname}", ""), # Title line
        ("OS", "Arch Linux x86_64"),
        ("HOST", "BIOSTAR Group H61MGV (7.0)"),
        ("KER", "Linux 7.2.11-arch1-1"),
        ("SH", "bash 5.3.20"),
        ("DISP", "1366x768"),
        ("WM", wm_env),
        ("THM", "adw-gtk3-dark"),
        ("TERM", os.environ.get("TERM", "alacritty")),
        ("CPU", cpu_model),
        ("GPU", gpu_name),
        ("RAM", ram_str)
    ]
    return stats

def run_archfetch():
    # Fixed the raw logo block so every single line prints correctly
    raw_logo = """                   -`
           -`
     -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:
               -+oooooo+:
             `/:-:++oooo+:
            `/++++/+++++++:
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooosssso++osssssso+`
        .oossssso-````/ossssss+`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++.
     /ossssssss/        +ssssooo/-
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `
+/
 .`                                 `"""

 
    logo = raw_logo.splitlines()
    
    # ANSI Color Escapes for terminal presentation
    BLUE = "\033[1;34m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Fetch data blocks
    raw_data = get_system_info()
    
    # Grid Math: Find the widest part of your logo to place the text separator accurately
    logo_width = max(len(line) for line in logo)
    term_columns, _ = shutil.get_terminal_size((80, 24))
    
    max_text_width = term_columns - logo_width - 8
    max_lines = max(len(logo), len(raw_data))
    
    print("") # Leading buffer space
    
    for i in range(max_lines):
        if i < len(logo):
            logo_line = f"{BLUE}{logo[i]:<{logo_width}}{RESET}"
        else:
            logo_line = " " * logo_width
            
        data_line = ""
        if i < len(raw_data):
            key, val = raw_data[i]
            
            if not val:
                data_line = f"{BLUE}{BOLD}{key}{RESET}"
                if i + 1 < max_lines:
                    underline = "-" * len(key)
                    raw_data.insert(i + 1, (underline, "UNDERLINE"))
            elif val == "UNDERLINE":
                data_line = f"{key}"
            else:
                combined_len = len(f"{key:<5} ➜  {val}")
                if combined_len > max_text_width:
                    available_space = max_text_width - 5 - 5
                    val = val[:available_space] + "..."
                    
                data_line = f"{BLUE}{key:<5}{RESET} ➜  {val}"
                
        print(f" {logo_line}    {data_line}")
        
    print("") # Trailing buffer space

if __name__ == "__main__":
    run_archfetch()
