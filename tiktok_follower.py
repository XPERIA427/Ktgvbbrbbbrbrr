#!/data/data/com.termux/files/usr/bin/python3
"""
TIKTOK FOLLOWER TERMUX BRUTAL
Run langsung dari Termux Android
"""
import os
import sys
import json
import time
import random
import requests
from datetime import datetime
from colorama import Fore, Style, init
from prettytable import PrettyTable

# Initialize colorama
init(autoreset=True)

# Banner
def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(Fore.CYAN + """
╔══════════════════════════════════════════════════════╗
║ ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗      ║
║ ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝      ║
║    ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝       ║
║    ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗       ║
║    ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗      ║
║    ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝      ║
╠══════════════════════════════════════════════════════╣
║              TERMUX BRUTAL v2.0                      ║
║         TikTok Follower Auto Bot                     ║
║           Created by X - Quantum Signature           ║
╚══════════════════════════════════════════════════════╝
    """)

class TikTokFollowerTermux:
    def __init__(self):
        self.session_id = None
        self.headers = None
        self.proxies = []
        self.load_config()
        
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                self.proxies = config.get('proxies', [])
                print(f"[✅] Loaded {len(self.proxies)} proxies")
        except:
            self.proxies = []
            
        # Load session from file
        try:
            with open('session.txt', 'r') as f:
                for line in f:
                    if 'sessionid=' in line:
                        self.session_id = line.strip().split('sessionid=')[1]
                        break
        except:
            pass
            
        if self.session_id:
            self.headers = {
                'User-Agent': 'com.ss.android.ugc.trill/2613 (Linux; U; Android 10; en_US; Pixel 4; Build/QQ3A.200805.001; Cronet/58.0.2991.0)',
                'Cookie': f'sessionid={self.session_id}',
                'X-Tt-Token': '',
            }
            print(f"[✅] Session loaded: {self.session_id[:20]}...")
        else:
            print(f"[❌] No session found! Edit session.txt first")
            
    def check_session(self):
        """Check if session is valid"""
        if not self.session_id:
            return False
            
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/me/"
        
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status_code') == 0:
                    user = data.get('user', {})
                    print(f"[✅] Logged in as: {user.get('unique_id', 'Unknown')}")
                    print(f"[📊] Followers: {user.get('follower_count', 0)}")
                    return True
        except:
            pass
            
        return False
        
    def get_user_id(self, username):
        """Get user ID from username"""
        print(f"[🔍] Getting user ID for @{username}...")
        
        url = f"https://www.tiktok.com/api/user/detail/?uniqueId={username}"
        
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            data = r.json()
            
            user_id = data.get('userInfo', {}).get('user', {}).get('id')
            if user_id:
                print(f"[✅] User ID found: {user_id}")
                return user_id
            else:
                print(f"[❌] User not found")
                return None
                
        except Exception as e:
            print(f"[⚠️] Error: {e}")
            return None
    
    def follow_user(self, user_id, sec_uid=None):
        """Follow a user"""
        if not sec_uid:
            # Get sec_uid first
            sec_uid = self.get_sec_uid(user_id)
            if not sec_uid:
                return False
                
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/commit/follow/user/"
        
        data = {
            'user_id': user_id,
            'sec_user_id': sec_uid,
            'type': 1,  # 1 = follow, 2 = unfollow
            'from': 0,
            'channel_id': 3,
        }
        
        try:
            r = requests.post(url, headers=self.headers, data=data, timeout=10)
            response = r.json()
            
            if response.get('status_code') == 0:
                print(f"[✅] Follow successful")
                return True
            else:
                print(f"[❌] Follow failed: {response.get('status_msg')}")
                return False
                
        except Exception as e:
            print(f"[⚠️] Error: {e}")
            return False
    
    def get_sec_uid(self, user_id):
        """Get sec_uid for user"""
        url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/profile/other/?user_id={user_id}"
        
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            data = r.json()
            
            sec_uid = data.get('user', {}).get('sec_uid')
            return sec_uid
        except:
            return None
    
    def get_recommended_users(self, count=20):
        """Get recommended users to follow"""
        print(f"[🔍] Getting {count} recommended users...")
        
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/recommend/"
        
        params = {
            'count': count,
            'offset': 0,
            'version_code': '2613',
            'app_name': 'trill',
            'device_platform': 'android',
        }
        
        try:
            r = requests.get(url, headers=self.headers, params=params, timeout=10)
            data = r.json()
            
            users = []
            for user in data.get('user_list', []):
                user_info = user.get('user', {})
                user_id = user_info.get('uid')
                sec_uid = user_info.get('sec_uid')
                username = user_info.get('unique_id')
                
                if user_id and sec_uid:
                    users.append({
                        'user_id': user_id,
                        'sec_uid': sec_uid,
                        'username': username,
                        'followers': user_info.get('follower_count', 0)
                    })
            
            print(f"[✅] Got {len(users)} recommended users")
            return users
            
        except Exception as e:
            print(f"[⚠️] Error: {e}")
            return []
    
    def auto_follow_recommended(self, amount=50):
        """Auto follow recommended users"""
        print(f"[🚀] Starting auto-follow for {amount} users...")
        
        followed = 0
        failed = 0
        
        while followed < amount:
            # Get batch of users
            users = self.get_recommended_users(20)
            
            if not users:
                print("[⚠️] No users found, waiting...")
                time.sleep(30)
                continue
            
            for user in users:
                if followed >= amount:
                    break
                    
                print(f"[{followed+1}/{amount}] Following @{user['username']}...")
                
                if self.follow_user(user['user_id'], user['sec_uid']):
                    followed += 1
                    
                    # Save to log
                    with open('followed_users.txt', 'a') as f:
                        f.write(f"{user['username']}|{user['user_id']}|{datetime.now()}\n")
                else:
                    failed += 1
                
                # Random delay 10-30 seconds
                delay = random.uniform(10, 30)
                print(f"[⏳] Waiting {delay:.1f} seconds...")
                time.sleep(delay)
            
            print(f"[📊] Progress: {followed}/{amount} followed, {failed} failed")
            
            if followed < amount:
                print(f"[⏳] Cooling down for 60 seconds...")
                time.sleep(60)
        
        print(f"[🎉] AUTO-FOLLOW COMPLETE!")
        print(f"    Followed: {followed}")
        print(f"    Failed: {failed}")
        
        return followed
    
    def mass_follow_target(self, target_username, amount=100):
        """Mass follow from multiple accounts (simulated)"""
        print(f"[💀] MASS FOLLOW ATTACK: @{target_username}")
        print(f"[🎯] Target: {amount} followers")
        
        # Get target user ID
        target_id = self.get_user_id(target_username)
        if not target_id:
            return False
        
        # Simulate mass follow (in reality need multiple sessions)
        print("[⚠️] This feature requires multiple bot accounts")
        print("[💡] Use the auto-follow-recommended method instead")
        
        return False
    
    def unfollow_non_followers(self):
        """Unfollow users who don't follow back"""
        print(f"[🧹] Cleaning up non-followers...")
        
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/following/list/"
        
        params = {
            'count': 200,
            'max_time': int(time.time()),
        }
        
        try:
            r = requests.get(url, headers=self.headers, params=params, timeout=10)
            data = r.json()
            
            followings = data.get('followings', [])
            print(f"[📊] You follow {len(followings)} users")
            
            unfollowed = 0
            for user in followings:
                user_id = user.get('uid')
                username = user.get('unique_id')
                is_followed_back = user.get('follow_status', 0) == 2
                
                if not is_followed_back:
                    print(f"[➖] Unfollowing @{username}...")
                    
                    # Unfollow request
                    unfollow_url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/commit/follow/user/"
                    unfollow_data = {
                        'user_id': user_id,
                        'type': 2,  # 2 = unfollow
                        'from': 0,
                    }
                    
                    r2 = requests.post(unfollow_url, headers=self.headers, data=unfollow_data)
                    
                    if r2.json().get('status_code') == 0:
                        unfollowed += 1
                        
                        # Save to log
                        with open('unfollowed.txt', 'a') as f:
                            f.write(f"{username}|{user_id}|{datetime.now()}\n")
                    
                    # Delay 5-15 seconds
                    time.sleep(random.uniform(5, 15))
            
            print(f"[✅] Unfollowed {unfollowed} users")
            
        except Exception as e:
            print(f"[⚠️] Error: {e}")
    
    def show_stats(self):
        """Show current account stats"""
        print(f"[📊] Getting account stats...")
        
        url = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/me/"
        
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            data = r.json()
            
            if data.get('status_code') == 0:
                user = data.get('user', {})
                
                table = PrettyTable()
                table.field_names = ["Stat", "Value"]
                table.align["Stat"] = "l"
                table.align["Value"] = "r"
                
                table.add_row(["Username", f"@{user.get('unique_id', 'N/A')}"])
                table.add_row(["Followers", f"{user.get('follower_count', 0):,}"])
                table.add_row(["Following", f"{user.get('following_count', 0):,}"])
                table.add_row(["Likes", f"{user.get('total_favorited', 0):,}"])
                table.add_row(["Videos", f"{user.get('aweme_count', 0):,}"])
                
                print(table)
                
                # Check if shadow banned
                if user.get('follower_count', 0) > 1000 and user.get('aweme_count', 0) > 10:
                    avg_views = user.get('total_favorited', 0) / max(user.get('aweme_count', 1), 1)
                    if avg_views < 10:
                        print(f"[⚠️] WARNING: Possible shadow ban detected!")
                        print(f"[💡] Avg likes per video: {avg_views:.1f}")
                
                return True
                
        except Exception as e:
            print(f"[⚠️] Error: {e}")
            
        return False

def main_menu():
    """Main menu"""
    bot = TikTokFollowerTermux()
    
    while True:
        show_banner()
        
        print(Fore.YELLOW + "\n📱 MAIN MENU:")
        print(Fore.CYAN + "═"*50)
        print(Fore.GREEN + "1. ✅ Check Session Login")
        print(Fore.GREEN + "2. 🔍 Find User ID")
        print(Fore.GREEN + "3. 🚀 Auto-Follow Recommended Users")
        print(Fore.GREEN + "4. 🎯 Mass Follow Target")
        print(Fore.GREEN + "5. 🧹 Unfollow Non-Followers")
        print(Fore.GREEN + "6. 📊 Show Account Stats")
        print(Fore.GREEN + "7. ⚙️ Settings")
        print(Fore.RED + "0. ❌ Exit")
        print(Fore.CYAN + "═"*50)
        
        choice = input(Fore.YELLOW + "\n[➤] Select option: " + Style.RESET_ALL)
        
        if choice == "1":
            if bot.check_session():
                input("\n[↵] Press Enter to continue...")
            else:
                print(Fore.RED + "[❌] Invalid session! Edit session.txt")
                input("\n[↵] Press Enter to continue...")
                
        elif choice == "2":
            username = input(Fore.YELLOW + "[?] Enter TikTok username (without @): " + Style.RESET_ALL)
            if username:
                user_id = bot.get_user_id(username)
                if user_id:
                    print(Fore.GREEN + f"[✅] User ID: {user_id}")
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "3":
            try:
                amount = int(input(Fore.YELLOW + "[?] How many users to follow? " + Style.RESET_ALL))
                if 1 <= amount <= 1000:
                    bot.auto_follow_recommended(amount)
                else:
                    print(Fore.RED + "[⚠️] Amount must be between 1-1000")
            except:
                print(Fore.RED + "[❌] Invalid input")
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "4":
            username = input(Fore.YELLOW + "[?] Target username: " + Style.RESET_ALL)
            if username:
                try:
                    amount = int(input(Fore.YELLOW + "[?] Followers amount: " + Style.RESET_ALL))
                    bot.mass_follow_target(username, amount)
                except:
                    print(Fore.RED + "[❌] Invalid amount")
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "5":
            confirm = input(Fore.RED + "[⚠️] Unfollow users who don't follow back? (y/n): " + Style.RESET_ALL)
            if confirm.lower() == 'y':
                bot.unfollow_non_followers()
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "6":
            bot.show_stats()
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "7":
            settings_menu(bot)
            
        elif choice == "0":
            print(Fore.CYAN + "\n[👋] Goodbye!")
            break
            
        else:
            print(Fore.RED + "[❌] Invalid option!")
            time.sleep(1)

def settings_menu(bot):
    """Settings menu"""
    while True:
        show_banner()
        
        print(Fore.YELLOW + "\n⚙️ SETTINGS:")
        print(Fore.CYAN + "═"*50)
        print(Fore.GREEN + "1. 📝 Edit Session ID")
        print(Fore.GREEN + "2. 🔄 Update Script")
        print(Fore.GREEN + "3. 📁 View Log Files")
        print(Fore.GREEN + "4. 🗑️ Clear Logs")
        print(Fore.GREEN + "5. 📋 View Followed Users")
        print(Fore.GREEN + "0. ↩️ Back to Main Menu")
        print(Fore.CYAN + "═"*50)
        
        choice = input(Fore.YELLOW + "\n[➤] Select option: " + Style.RESET_ALL)
        
        if choice == "1":
            print(Fore.YELLOW + "\n[ℹ️] How to get sessionid:")
            print("1. Open TikTok in Chrome/Firefox")
            print("2. Press F12 → Application → Cookies")
            print("3. Copy 'sessionid' value")
            print("\n[💡] Example: sessionid=abc123def456ghi789")
            
            edit = input(Fore.YELLOW + "\n[?] Edit session.txt now? (y/n): " + Style.RESET_ALL)
            if edit.lower() == 'y':
                os.system('nano session.txt')
                print(Fore.GREEN + "[✅] Session file updated!")
                bot.load_config()
                
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "2":
            print(Fore.YELLOW + "\n[⬇️] Updating script...")
            os.system('cd ~/tiktok-brutal && git pull')
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "3":
            print(Fore.YELLOW + "\n📁 LOG FILES:")
            os.system('ls -la ~/tiktok-brutal/*.txt')
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "4":
            confirm = input(Fore.RED + "[⚠️] Clear all log files? (y/n): " + Style.RESET_ALL)
            if confirm.lower() == 'y':
                os.system('rm -f ~/tiktok-brutal/*.txt')
                print(Fore.GREEN + "[✅] Logs cleared!")
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "5":
            if os.path.exists('followed_users.txt'):
                print(Fore.YELLOW + "\n📋 FOLLOWED USERS:")
                os.system('cat followed_users.txt | tail -20')
            else:
                print(Fore.RED + "[❌] No log file found")
            input("\n[↵] Press Enter to continue...")
            
        elif choice == "0":
            break
            
        else:
            print(Fore.RED + "[❌] Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n\n[👋] Script stopped by user")
    except Exception as e:
        print(Fore.RED + f"\n[❌] Error: {e}")
        input("\n[↵] Press Enter to exit...")
