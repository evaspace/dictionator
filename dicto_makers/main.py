import sys
import os
import re
from generator import DictionaryGenerator

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class MockColor:
        def __getattr__(self, name): return ""
    Fore = Style = MockColor()

def print_banner():
    banner = f"""
{Fore.CYAN} 

 @@@@@@@  @@@  @@@@@@@ @@@@@@@ @@@  @@@@@@  @@@  @@@  @@@@@@  @@@@@@@   @@@@@@  @@@@@@@  @@@@@@  @@@@@@@ 
 @@!  @@@ @@! !@@        @@!   @@! @@!  @@@ @@!@!@@@ @@!  @@@ @@!  @@@ @@!  @@@   @@!   @@!  @@@ @@!  @@@
 @!@  !@! !!@ !@!        @!!   !!@ @!@  !@! @!@@!!@! @!@!@!@! @!@!!@!  @!@!@!@!   @!!   @!@  !@! @!@!!@! 
 !!:  !!! !!: :!!        !!:   !!: !!:  !!! !!:  !!! !!:  !!! !!: :!!  !!:  !!!   !!:   !!:  !!! !!: :!! 
 :: :  :  :    :: :: :    :    :    : :. :  ::    :   :   : :  :   : :  :   : :    :     : :. :   :   : :
                                                                                                          
{Fore.YELLOW}  Custom Dictionary Generator - V2.0 (Strict Mode)
    """
    sys.stderr.write(banner + "\n")

def get_strict_input(label, prompt, examples, required=False, pattern=None, is_symbols=False):
    while True:
        sys.stderr.write(f"\n{Fore.GREEN}[+] {label}\n")
        sys.stderr.write(f"{Fore.WHITE}{prompt} (e.g., {examples})\n")
        user_input = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
        
        if not user_input or (is_symbols and user_input.lower() == "default"):
            if required:
                sys.stderr.write(f"{Fore.RED}[!] This field is required.\n")
                continue
            return []
        
        # Split by comma OR space
        items = re.split(r'[,\s]+', user_input)
        items = [item.strip() for item in items if item.strip()]
        
        if not items and required:
            sys.stderr.write(f"{Fore.RED}[!] Invalid input. Please provide at least one value.\n")
            continue
            
        if pattern:
            invalid = [i for i in items if not re.match(pattern, i)]
            if invalid:
                sys.stderr.write(f"{Fore.RED}[!] Invalid format for: {Fore.YELLOW}{', '.join(invalid)}\n")
                sys.stderr.write(f"{Fore.WHITE}[*] Expected format: {examples}\n")
                continue
        
        return items

def get_levels():
    while True:
        sys.stderr.write(f"\n{Fore.YELLOW}[?] Select Generation Levels (e.g., 1, 2, 5 or 1-5)\n")
        sys.stderr.write(f"{Fore.WHITE}1: Basic | 5: Complex | 10: Deep Hybridization\n")
        user_input = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
        
        levels = []
        try:
            if '-' in user_input:
                start, end = map(int, user_input.split('-'))
                levels = list(range(start, end + 1))
            else:
                levels = [int(l.strip()) for l in user_input.replace(',', ' ').split() if l.strip()]
            
            if all(1 <= l <= 10 for l in levels):
                return sorted(list(set(levels)))
            sys.stderr.write(f"{Fore.RED}[!] Levels must be between 1 and 10.\n")
        except ValueError:
            sys.stderr.write(f"{Fore.RED}[!] Invalid format. Use '1, 2, 5' or '1-5'.\n")

def main():
    print_banner()
    
    # 1. Collect Data
    data = {}
    data['words'] = get_strict_input("Base Words", "Keywords or names", "admin, user", required=True, pattern=r"^[a-zA-Z]+$")
    data['animals'] = get_strict_input("Animals", "Generic animal names", "cat, dog", pattern=r"^[a-zA-Z]+$")
    data['dates'] = get_strict_input("Dates", "Years or DDMM", "1990, 2024", pattern=r"^\d{2,4}$")
    data['places'] = get_strict_input("Locations", "Cities or regions", "london, paris", pattern=r"^[a-zA-Z0-9]+$")
    data['numbers'] = get_strict_input("Specific Numbers", "Significant numbers", "123, 7", pattern=r"^\d+$")
    data['symbols'] = get_strict_input("Special Characters", "Type 'default' for !, @, #, $, *, &", "!, @, #", pattern=r"^[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]+$", is_symbols=True)
    
    if not data['symbols']:
        data['symbols'] = ["!", "@", "#", "$", "*", "&"]
    
    data['conjunctions'] = ["&", "+", "-", "_", "@"]
    
    # 2. Select Levels
    levels = get_levels()
    
    # 3. Handle Directory
    sys.stderr.write(f"\n{Fore.YELLOW}[?] Target Directory Name (Enter to use '{data['words'][0]}')\n")
    folder_name = input(f"{Fore.CYAN}> {Style.RESET_ALL}").strip()
    if not folder_name:
        folder_name = data['words'][0]
    folder_name = re.sub(r'[^\w\s-]', '', folder_name).strip().replace(' ', '_')
    
    target_dir = os.path.join("target", folder_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        sys.stderr.write(f"{Fore.GREEN}[+] Directory '{folder_name}' created in target/.\n")
    
    # 4. Confirmation
    sys.stderr.write(f"\n{Fore.YELLOW}--- Ready to Generate ---\n")
    sys.stderr.write(f"{Fore.WHITE}Directory: {Fore.CYAN}target/{folder_name}\n")
    sys.stderr.write(f"{Fore.WHITE}Target Levels: {Fore.CYAN}{', '.join(map(str, levels))}\n")
    
    confirm = input(f"\n{Fore.WHITE}Confirm and start? (y/n): {Fore.CYAN}")
    if confirm.lower() != 'y':
        sys.stderr.write(f"{Fore.RED}[!] Aborted.\n")
        return

    # 5. Generation
    gen = DictionaryGenerator(data)
    for level in levels:
        file_path = os.path.join(target_dir, f"level_{level}.txt")
        count = 0
        try:
            with open(file_path, 'w') as f:
                sys.stderr.write(f"\n{Fore.YELLOW}[*] Generating Level {level}...\n")
                for pwd in gen.generate(level=level):
                    if pwd:
                        f.write(pwd + "\n")
                        count += 1
                        if count % 1000 == 0:
                            sys.stderr.write(f"\r    -> Generated: {count} words...")
                sys.stderr.write(f"\r    -> Final count: {count} words saved.          \n")
        except KeyboardInterrupt:
            sys.stderr.write(f"\n{Fore.RED}[!] Interrupted.\n")
            break

    sys.stderr.write(f"\n{Fore.GREEN}[+] SUCCESS: Files saved in target/{folder_name}/\n")


if __name__ == "__main__":
    main()
