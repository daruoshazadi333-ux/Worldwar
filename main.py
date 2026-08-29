import asyncio, json, random, logging, traceback, time
from pathlib import Path
from datetime import datetime, date, timedelta
from os import system as os_system, name as os_name
from rubka.asynco import Robot
from rubka.context import Message
from rubka.keypad import ChatKeypadBuilder

# ---------- Logging ----------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_errors.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ---------- config ----------
BOT_TOKEN = "BHJEGG0LZYHJRDVYGAQUHCZXQLNBOMCRDTAWBRSPVRGVDOHEJZIZOOXSYIXOEEOK"
ADMINS = [admin for admin in ["", "b0IHXHW0nOE0346b7cf8cf9382619504"] if admin]
ADMIN_PASSWORD = "admin090hk989897877"
ADMIN_USERNAME = "@admin10blue"
DATA_FILE = Path("worldwar_data.json")
COUNTRIES_FILE = Path("countries_data.json")
UN_FILE = Path("un_data.json")
ALLIANCE_FILE = Path("alliance_data.json")
BOT_STATUS_FILE = Path("bot_status.json")

F = {"b":"**","i":"_","m":"`","l":"▬"*30,"a":"➤","s":"★","f":"🔥","c":"♛","sh":"🛡","sw":"⚔","co":"🪙","d":"◆","ch":"✅","cr":"❌","sk":"💀","t":"🏆","g":"🌐","bo":"💥","h":"🤝","be":"🗡️"}

MAX_WARNINGS = 3
RULES_TEXT = (
    "📜 قوانین جنگ جهانی\n\n"
    "⚠️ هر فحش یا توهین = ۱ اخطار.\n"
    "🔴 مجموع اخطارها حداکثر ۳ عدد است.\n"
    "🚫 با رسیدن به ۳ اخطار، کشور شما ریست و حساب شما مسدود می‌شود.\n"
    "💰 پول پرداخت‌شده برای پک‌ها و خریدها به هیچ عنوان پس داده نمی‌شود.\n"
    "⚔️ سوءاستفاده از باگ، اسپم و ایجاد مزاحمت نیز می‌تواند اخطار داشته باشد.\n"
    "🛡️ قوانین برای همه کاربران یکسان است."
)
# واژه‌های پایه برای تشخیص توهین؛ فهرست عمداً کوتاه نگه داشته شده تا خطای تشخیص کم شود.
BAD_WORDS = {
    "احمق","بی شعور","بی‌شعور","کسخل","کودن","نفهم","حرومزاده","حرامزاده",
    "گمشو","دهنتو ببند","خفه شو","عوضی","فحش","fuck","shit"
}


COUNTRIES = [
    {"code":"US","flag":"🇺🇸","name":"آمریکا","emoji":"🦅","bonus":500},
    {"code":"GB","flag":"🇬🇧","name":"بریتانیا","emoji":"👑","bonus":400},
    {"code":"FR","flag":"🇫🇷","name":"فرانسه","emoji":"🗼","bonus":350},
    {"code":"DE","flag":"🇩🇪","name":"آلمان","emoji":"🦅","bonus":450},
    {"code":"IT","flag":"🇮🇹","name":"ایتالیا","emoji":"🍕","bonus":300},
    {"code":"CA","flag":"🇨🇦","name":"کانادا","emoji":"🍁","bonus":350},
    {"code":"ES","flag":"🇪🇸","name":"اسپانیا","emoji":"💃","bonus":300},
    {"code":"GR","flag":"🇬🇷","name":"یونان","emoji":"🏛","bonus":200},
    {"code":"NL","flag":"🇳🇱","name":"هلند","emoji":"🌷","bonus":250},
    {"code":"NO","flag":"🇳🇴","name":"نروژ","emoji":"🏔","bonus":200},
    {"code":"JP","flag":"🇯🇵","name":"ژاپن","emoji":"🗾","bonus":400},
    {"code":"RU","flag":"🇷🇺","name":"روسیه","emoji":"🐻","bonus":500},
    {"code":"CN","flag":"🇨🇳","name":"چین","emoji":"🐉","bonus":500},
    {"code":"IR","flag":"🇮🇷","name":"ایران","emoji":"🦁","bonus":350},
    {"code":"IN","flag":"🇮🇳","name":"هند","emoji":"🐘","bonus":450},
    {"code":"KP","flag":"🇰🇵","name":"کره شمالی","emoji":"💣","bonus":300},
    {"code":"IL","flag":"✡️","name":"اسرائیل","emoji":"🕎","bonus":350},
    {"code":"SA","flag":"🇸🇦","name":"عربستان","emoji":"🕋","bonus":400},
    {"code":"TR","flag":"🇹🇷","name":"ترکیه","emoji":"🕌","bonus":300},
    {"code":"BR","flag":"🇧🇷","name":"برزیل","emoji":"⚽","bonus":300},
    {"code":"AE","flag":"🇦🇪","name":"امارات","emoji":"🏙","bonus":400},
    {"code":"PK","flag":"🇵🇰","name":"پاکستان","emoji":"⭐","bonus":250},
    {"code":"EG","flag":"🇪🇬","name":"مصر","emoji":"🏺","bonus":250},
    {"code":"KR","flag":"🇰🇷","name":"کره جنوبی","emoji":"🎵","bonus":300},
    {"code":"SY","flag":"🇸🇾","name":"سوریه","emoji":"🏛","bonus":150},
    {"code":"VN","flag":"🇻🇳","name":"ویتنام","emoji":"🌴","bonus":200},
    {"code":"VE","flag":"🇻🇪","name":"ونزوئلا","emoji":"🛢","bonus":200},
    {"code":"CU","flag":"🇨🇺","name":"کوبا","emoji":"🚬","bonus":150},
    {"code":"ET","flag":"🇪🇹","name":"اتیوپی","emoji":"☕","bonus":150},
    {"code":"LB","flag":"🇱🇧","name":"لبنان","emoji":"🌲","bonus":150},
    {"code":"PS","flag":"🇵🇸","name":"فلسطین","emoji":"🕊","bonus":200},
    {"code":"ZA","flag":"🇿🇦","name":"آفریقای جنوبی","emoji":"🦁","bonus":200},
    {"code":"IQ","flag":"🇮🇶","name":"عراق","emoji":"🏛","bonus":200},
    {"code":"AU","flag":"🇦🇺","name":"استرالیا","emoji":"🦘","bonus":350},
    {"code":"NZ","flag":"🇳🇿","name":"نیوزیلند","emoji":"🥝","bonus":220},
    {"code":"MX","flag":"🇲🇽","name":"مکزیک","emoji":"🌵","bonus":280},
    {"code":"AR","flag":"🇦🇷","name":"آرژانتین","emoji":"⚽","bonus":320},
    {"code":"CL","flag":"🇨🇱","name":"شیلی","emoji":"🏔","bonus":220},
    {"code":"CO","flag":"🇨🇴","name":"کلمبیا","emoji":"☕","bonus":240},
    {"code":"PE","flag":"🇵🇪","name":"پرو","emoji":"🦙","bonus":210},
    {"code":"UY","flag":"🇺🇾","name":"اروگوئه","emoji":"⚽","bonus":190},
    {"code":"PY","flag":"🇵🇾","name":"پاراگوئه","emoji":"🌿","bonus":160},
    {"code":"BO","flag":"🇧🇴","name":"بولیوی","emoji":"⛰️","bonus":150},
    {"code":"EC","flag":"🇪🇨","name":"اکوادور","emoji":"🌋","bonus":170},
    {"code":"GY","flag":"🇬🇾","name":"گویان","emoji":"🌴","bonus":130},
    {"code":"SR","flag":"🇸🇷","name":"سورینام","emoji":"🌳","bonus":120},
    {"code":"FJ","flag":"🇫🇯","name":"فیجی","emoji":"🌴","bonus":100},
    {"code":"PT","flag":"🇵🇹","name":"پرتغال","emoji":"⚓","bonus":280},
    {"code":"IE","flag":"🇮🇪","name":"ایرلند","emoji":"☘️","bonus":210},
    {"code":"IS","flag":"🇮🇸","name":"ایسلند","emoji":"❄️","bonus":180},
    {"code":"SE","flag":"🇸🇪","name":"سوئد","emoji":"🛡️","bonus":260},
    {"code":"FI","flag":"🇫🇮","name":"فنلاند","emoji":"❄️","bonus":240},
    {"code":"DK","flag":"🇩🇰","name":"دانمارک","emoji":"⚔️","bonus":230},
    {"code":"PL","flag":"🇵🇱","name":"لهستان","emoji":"🦅","bonus":260},
    {"code":"CZ","flag":"🇨🇿","name":"چک","emoji":"🏰","bonus":210},
    {"code":"SK","flag":"🇸🇰","name":"اسلواکی","emoji":"🏔","bonus":160},
    {"code":"HU","flag":"🇭🇺","name":"مجارستان","emoji":"🦅","bonus":190},
    {"code":"RO","flag":"🇷🇴","name":"رومانی","emoji":"🏰","bonus":200},
    {"code":"BG","flag":"🇧🇬","name":"بلغارستان","emoji":"🌹","bonus":170},
    {"code":"RS","flag":"🇷🇸","name":"صربستان","emoji":"🦅","bonus":180},
    {"code":"HR","flag":"🇭🇷","name":"کرواسی","emoji":"♟️","bonus":200},
    {"code":"HT","flag":"🇭🇹","name":"هائیتی","emoji":"🌴","bonus":110},
    {"code":"SI","flag":"🇸🇮","name":"اسلوونی","emoji":"🏔","bonus":150},
    {"code":"AL","flag":"🇦🇱","name":"آلبانی","emoji":"🦅","bonus":140},
    {"code":"DO","flag":"🇩🇴","name":"جمهوری دومینیکن","emoji":"🌴","bonus":140},
    {"code":"TT","flag":"🇹🇹","name":"ترینیداد و توباگو","emoji":"🌊","bonus":110},
    {"code":"JM","flag":"🇯🇲","name":"جامائیکا","emoji":"🎵","bonus":130},
    {"code":"UA","flag":"🇺🇦","name":"اوکراین","emoji":"🌾","bonus":280},
    {"code":"BY","flag":"🇧🇾","name":"بلاروس","emoji":"🌲","bonus":190},
    {"code":"MD","flag":"🇲🇩","name":"مولداوی","emoji":"🍇","bonus":130},
    {"code":"LT","flag":"🇱🇹","name":"لیتوانی","emoji":"🌲","bonus":150},
    {"code":"LV","flag":"🇱🇻","name":"لتونی","emoji":"🌲","bonus":145},
    {"code":"EE","flag":"🇪🇪","name":"استونی","emoji":"💻","bonus":150},
    {"code":"GE","flag":"🇬🇪","name":"گرجستان","emoji":"🍇","bonus":170},
    {"code":"AM","flag":"🇦🇲","name":"ارمنستان","emoji":"⛰️","bonus":140},
    {"code":"AZ","flag":"🇦🇿","name":"آذربایجان","emoji":"🔥","bonus":190},
    {"code":"KZ","flag":"🇰🇿","name":"قزاقستان","emoji":"🐎","bonus":240},
    {"code":"UZ","flag":"🇺🇿","name":"ازبکستان","emoji":"🏜️","bonus":190},
    {"code":"TM","flag":"🇹🇲","name":"ترکمنستان","emoji":"🐎","bonus":150},
    {"code":"KG","flag":"🇰🇬","name":"قرقیزستان","emoji":"🏔","bonus":140},
    {"code":"TJ","flag":"🇹🇯","name":"تاجیکستان","emoji":"⛰️","bonus":140},
    {"code":"MN","flag":"🇲🇳","name":"مغولستان","emoji":"🐎","bonus":180},
    {"code":"AF","flag":"🇦🇫","name":"افغانستان","emoji":"🏔","bonus":170},
    {"code":"BD","flag":"🇧🇩","name":"بنگلادش","emoji":"🌊","bonus":180},
    {"code":"LK","flag":"🇱🇰","name":"سریلانکا","emoji":"🌴","bonus":170},
    {"code":"NP","flag":"🇳🇵","name":"نپال","emoji":"🏔","bonus":180},
    {"code":"BT","flag":"🇧🇹","name":"بوتان","emoji":"🐉","bonus":110},
    {"code":"MM","flag":"🇲🇲","name":"میانمار","emoji":"🌴","bonus":150},
    {"code":"TH","flag":"🇹🇭","name":"تایلند","emoji":"🐘","bonus":220},
    {"code":"MY","flag":"🇲🇾","name":"مالزی","emoji":"🌴","bonus":230},
    {"code":"SG","flag":"🇸🇬","name":"سنگاپور","emoji":"🏙️","bonus":300},
    {"code":"ID","flag":"🇮🇩","name":"اندونزی","emoji":"🌋","bonus":240},
    {"code":"PH","flag":"🇵🇭","name":"فیلیپین","emoji":"🌊","bonus":200},
    {"code":"KH","flag":"🇰🇭","name":"کامبوج","emoji":"🏯","bonus":130},
    {"code":"LA","flag":"🇱🇦","name":"لائوس","emoji":"🌿","bonus":120},
    {"code":"BN","flag":"🇧🇳","name":"برونئی","emoji":"🛢️","bonus":150},
    {"code":"TL","flag":"🇹🇱","name":"تیمور شرقی","emoji":"🌊","bonus":100},
    {"code":"WS","flag":"🇼🇸","name":"ساموآ","emoji":"🌴","bonus":100},
    {"code":"QA","flag":"🇶🇦","name":"قطر","emoji":"🏙️","bonus":280},
    {"code":"KW","flag":"🇰🇼","name":"کویت","emoji":"🛢️","bonus":260},
    {"code":"BH","flag":"🇧🇭","name":"بحرین","emoji":"🌊","bonus":200},
    {"code":"OM","flag":"🇴🇲","name":"عمان","emoji":"🏜️","bonus":220},
    {"code":"YE","flag":"🇾🇪","name":"یمن","emoji":"🏔","bonus":130},
    {"code":"JO","flag":"🇯🇴","name":"اردن","emoji":"🏜️","bonus":180},
    {"code":"TO","flag":"🇹🇴","name":"تونگا","emoji":"🌊","bonus":95},
    {"code":"MA","flag":"🇲🇦","name":"مراکش","emoji":"🕌","bonus":230},
    {"code":"DZ","flag":"🇩🇿","name":"الجزایر","emoji":"🏜️","bonus":230},
    {"code":"TN","flag":"🇹🇳","name":"تونس","emoji":"🏺","bonus":180},
    {"code":"LY","flag":"🇱🇾","name":"لیبی","emoji":"🛢️","bonus":160},
    {"code":"SD","flag":"🇸🇩","name":"سودان","emoji":"🌾","bonus":140},
    {"code":"SS","flag":"🇸🇸","name":"سودان جنوبی","emoji":"🌿","bonus":120},
    {"code":"SO","flag":"🇸🇴","name":"سومالی","emoji":"🏜️","bonus":120},
    {"code":"DJ","flag":"🇩🇯","name":"جیبوتی","emoji":"⚓","bonus":100},
    {"code":"ER","flag":"🇪🇷","name":"اریتره","emoji":"🏜️","bonus":110},
    {"code":"KE","flag":"🇰🇪","name":"کنیا","emoji":"🦁","bonus":180},
    {"code":"TZ","flag":"🇹🇿","name":"تانزانیا","emoji":"🦒","bonus":170},
    {"code":"UG","flag":"🇺🇬","name":"اوگاندا","emoji":"🦍","bonus":140},
    {"code":"RW","flag":"🇷🇼","name":"رواندا","emoji":"🌋","bonus":120},
    {"code":"GH","flag":"🇬🇭","name":"غنا","emoji":"⭐","bonus":160},
    {"code":"NG","flag":"🇳🇬","name":"نیجریه","emoji":"🦅","bonus":240},
    {"code":"CM","flag":"🇨🇲","name":"کامرون","emoji":"🦁","bonus":130},
    {"code":"SN","flag":"🇸🇳","name":"سنگال","emoji":"🦁","bonus":140},
    {"code":"CI","flag":"🇨🇮","name":"ساحل عاج","emoji":"🐘","bonus":150},
    {"code":"ML","flag":"🇲🇱","name":"مالی","emoji":"🏜️","bonus":120},
    {"code":"NE","flag":"🇳🇪","name":"نیجر","emoji":"🏜️","bonus":110},
    {"code":"MR","flag":"🇲🇷","name":"موریتانی","emoji":"🐪","bonus":110},
    {"code":"ZW","flag":"🇿🇼","name":"زیمبابوه","emoji":"🦁","bonus":130},
    {"code":"ZM","flag":"🇿🇲","name":"زامبیا","emoji":"🦅","bonus":120},
    {"code":"MZ","flag":"🇲🇿","name":"موزامبیک","emoji":"🌊","bonus":130},
    {"code":"AO","flag":"🇦🇴","name":"آنگولا","emoji":"🛢️","bonus":170},
    {"code":"NA","flag":"🇳🇦","name":"نامیبیا","emoji":"🏜️","bonus":120},
    {"code":"BW","flag":"🇧🇼","name":"بوتسوانا","emoji":"🐘","bonus":110},
    {"code":"MG","flag":"🇲🇬","name":"ماداگاسکار","emoji":"🌴","bonus":120},
    {"code":"MU","flag":"🇲🇺","name":"موریس","emoji":"🌊","bonus":100},
    {"code":"SC","flag":"🇸🇨","name":"سیشل","emoji":"🌊","bonus":100},
    {"code":"CD","flag":"🇨🇩","name":"کنگو","emoji":"🌳","bonus":150},
    {"code":"CG","flag":"🇨🇬","name":"کنگو برازاویل","emoji":"🌳","bonus":130},
    {"code":"GA","flag":"🇬🇦","name":"گابن","emoji":"🌳","bonus":120},
    {"code":"GQ","flag":"🇬🇶","name":"گینه استوایی","emoji":"🛢️","bonus":120},
    {"code":"VU","flag":"🇻🇺","name":"وانواتو","emoji":"🌋","bonus":95},
    {"code":"BJ","flag":"🇧🇯","name":"بنین","emoji":"🌴","bonus":110},
    {"code":"TG","flag":"🇹🇬","name":"توگو","emoji":"🌴","bonus":105},
    {"code":"BF","flag":"🇧🇫","name":"بورکینافاسو","emoji":"🏜️","bonus":110},
    {"code":"GN","flag":"🇬🇳","name":"گینه","emoji":"🌿","bonus":110},
    {"code":"SL","flag":"🇸🇱","name":"سیرالئون","emoji":"🌊","bonus":100},
    {"code":"LR","flag":"🇱🇷","name":"لیبریا","emoji":"🌴","bonus":100},
    {"code":"CV","flag":"🇨🇻","name":"کیپ ورد","emoji":"🌊","bonus":95},
    {"code":"GM","flag":"🇬🇲","name":"گامبیا","emoji":"🌊","bonus":95},
    {"code":"BI","flag":"🇧🇮","name":"بوروندی","emoji":"🌿","bonus":100},
    {"code":"MW","flag":"🇲🇼","name":"مالاوی","emoji":"🌿","bonus":100},
]

FACTIONS = {
    "sepah":{"name":"سپاه پاسداران","icon":"🛡⚔️","emoji":"🇮🇷","atk":1.5,"def":2.0,"w":["خیبرشکن","موشک","پهپاد"],"min":5000,"max":10},
    "darkweb":{"name":"دارک وب","icon":"💀🌐","emoji":"🖤","atk":2.0,"def":0.5,"w":["بمب اتم","پهپاد","B2"],"min":8000,"max":7},
    "hezbollah":{"name":"حزب‌الله","icon":"⚔️🕊","emoji":"🇱🇧","atk":1.8,"def":1.5,"w":["موشک","خیبرشکن","تانک"],"min":4000,"max":12}
}

EQUIP = {
    "اف۲۲":(1600,"🛩","جنگنده",50),"اف۳۵":(1700,"🛩","جنگنده",60),"اف۱۶":(1500,"🛩","جنگنده",40),
    "اف۱۵":(1450,"🛩","جنگنده",35),"تایفون":(1550,"🛩","جنگنده",45),"سوخو۳۵":(1650,"🛩","جنگنده",55),
    "سوخو۵۷":(1800,"🛩","جنگنده",70),"جی۲۰":(1750,"🛩","جنگنده",65),
    "B2":(3100,"💣","بمب‌افکن",200),"B1":(2900,"💣","بمب‌افکن",180),"B52":(2600,"💣","بمب‌افکن",150),
    "موشک":(1400,"🚀","موشکی",30),"خیبرشکن":(1900,"🚀","موشکی",80),"پهپاد":(1350,"🛸","پهپادی",25),
    "تانک":(1500,"🪖","زمینی",40),"بالگرد":(1450,"🚁","هوایی",35),"زیردریایی":(1700,"🌊","دریایی",60),
    "ناو":(2100,"🚢","دریایی",100),"بمب اتم":(10000,"☢️","ویژه",1000),"بمب تزار":(9100,"💥","ویژه",800),
    "پدافند":(1300,"🛡","دفاعی",20),"اس۴۰۰":(1400,"🛡","دفاعی",30),"پاتریوت":(1380,"🛡","دفاعی",28),
    "تاد":(1420,"🛡","دفاعی",32),"گنبد":(1450,"🛡","دفاعی",35),"اس۵۰۰":(1500,"🛡","دفاعی",40),
}

PACKS = {
    "پک جنگنده":(10000,"🛩","ناوگان هوایی",{"اف۲۲":300,"اف۳۵":300,"اف۱۶":300,"اف۱۵":300,"تایفون":300,"سوخو۳۵":300,"سوخو۵۷":300,"جی۲۰":300}),
    "پک نابود":(30000,"💀","قدرت تخریب بالا",{"B2":200,"B1":200,"B52":200,"موشک":200,"پهپاد":200,"تانک":100,"بالگرد":50,"زیردریایی":25,"ناو":10,"بمب اتم":5}),
    "پک اقتصادی":(30000,"💰","مقرون به صرفه",{"B2":100,"B1":100,"B52":100,"موشک":100,"پدافند":100,"تانک":50,"بالگرد":30,"زیردریایی":20,"ناو":10}),
    "پک افسانه":(30000,"👑","افسانه‌ای و بی‌نظیر",{"موشک":350,"خیبرشکن":200,"زیردریایی":150,"ناو":100,"بمب تزار":100,"پدافند":200,"B2":200,"اف۳۵":200}),
    "پدافند جهان":(25000,"🛡","سپر دفاعی قدرتمند",{"اس۴۰۰":1000,"پاتریوت":1000,"تاد":1000,"گنبد":1000,"اس۵۰۰":1000})
}

# ---------- helpers ----------
def st(t,s="b"): return f"{F[s]}{t}{F[s]}"
def fn(n): return f"{n:,}"
def ml(c="▬",n=30): return c*n
def mh(t,i="🔹"): return f"{i}{ml('═',15)}{i}\n{st('  '+t+'  ','b')}\n{i}{ml('═',15)}{i}"
def mf(txt,title="",icon="📨"):
    lines=txt.split('\n')
    max_len=max((len(l) for l in lines),default=20)
    border="╔"+"═"*(max_len+2)+"╗"
    bottom="╚"+"═"*(max_len+2)+"╝"
    header=f"║ {icon} {title}".ljust(max_len+3)+"║" if title else ""
    content="\n".join("║ "+l.ljust(max_len)+" ║" for l in lines)
    return f"{border}\n{header}\n{content}\n{bottom}" if header else f"{border}\n{content}\n{bottom}"

def gid(msg,uid):
    try:
        if hasattr(msg,'author') and msg.author:
            un=getattr(msg.author,'username',None)
            if un: return f"@{un} | `{uid}`"
            fn=getattr(msg.author,'first_name',None)
            if fn: return f"{fn} | `{uid}`"
    except: pass
    try:
        sn=getattr(msg,'sender_name',None)
        if sn: return f"{sn} | `{uid}`"
    except: pass
    return f"`{uid}`"

def guser(msg):
    try:
        if hasattr(msg,'author') and msg.author:
            return getattr(msg.author,'username',None) or getattr(msg.author,'first_name',None)
    except: pass
    try: return getattr(msg,'sender_name',None)
    except: pass
    return None

def power(data,uid):
    eq=data.get("user_eq",{}).get(uid,{})
    pk=data.get("user_packs",{}).get(uid,[])
    p=sum(EQUIP.get(k,(0,)*4)[3]*v for k,v in eq.items())
    p+=len(set(pk))*500
    fac=data.get("users",{}).get(uid,{}).get("faction")
    if fac and fac in FACTIONS: p=int(p*FACTIONS[fac]["atk"])
    un=load_un()
    if uid==un.get("leader"): p=int(p*1.5)
    elif uid in un.get("members",[]): p=int(p*1.2)
    return p

def defense_power(data,uid):
    eq=data.get("user_eq",{}).get(uid,{})
    dp=sum(EQUIP.get(it,(0,)*4)[3]*eq.get(it,0) for it in ["پدافند","اس۴۰۰","پاتریوت","تاد","گنبد","اس۵۰۰"])
    fac=data.get("users",{}).get(uid,{}).get("faction")
    if fac and fac in FACTIONS: dp=int(dp*FACTIONS[fac]["def"])
    return dp

def get_coins(data,uid): return data.get("users",{}).get(uid,{}).get("coins",0)

def addc(data,uid,amt):
    if uid not in data.get("users",{}): return
    data["users"][uid]["coins"]=data["users"][uid].get("coins",0)+amt
    save_data(data)

def remc(data,uid,amt):
    if uid not in data.get("users",{}): return False,"کاربر یافت نشد"
    cur=data["users"][uid].get("coins",0)
    if amt<=0: return False,"مقدار باید مثبت باشد"
    if cur<amt: return False,f"موجودی کافی نیست. موجودی: {fn(cur)}"
    data["users"][uid]["coins"]=cur-amt
    save_data(data)
    return True,"موفق"

def addeq(data,uid,eq,amt):
    if amt<=0: return
    if "user_eq" not in data: data["user_eq"]={}
    if uid not in data["user_eq"]: data["user_eq"][uid]={}
    data["user_eq"][uid][eq]=data["user_eq"][uid].get(eq,0)+amt
    save_data(data)

def remeq(data,uid,eq,amt):
    if amt<=0: return False,"مقدار باید مثبت باشد"
    if "user_eq" not in data: data["user_eq"]={}
    if uid not in data["user_eq"]: data["user_eq"][uid]={}
    cur=data["user_eq"][uid].get(eq,0)
    if cur<amt: return False,f"تجهیزات کافی نیست. موجودی: {fn(cur)}"
    data["user_eq"][uid][eq]=cur-amt
    if data["user_eq"][uid][eq]<=0: del data["user_eq"][uid][eq]
    save_data(data)
    return True,"موفق"

def totaleq(data,uid):
    eq=data.get("user_eq",{}).get(uid,{}).copy()
    return eq

def consume(data,uid,eq,amt):
    if amt<=0: return 0,False
    total=data.get("user_eq",{}).get(uid,{}).get(eq,0)
    if total<amt: return 0,False
    data["user_eq"][uid][eq]-=amt
    if data["user_eq"][uid][eq]<=0: del data["user_eq"][uid][eq]
    save_data(data)
    return amt,True


def warning_count(data, uid):
    return int(data.get("users", {}).get(uid, {}).get("warnings", 0))

def set_warnings(data, uid, count):
    if uid in data.get("users", {}):
        data["users"][uid]["warnings"] = max(0, min(MAX_WARNINGS, int(count)))
        save_data(data)

async def issue_warning(bot, data, countries, uid, reason="تخلف از قوانین", notify=True):
    """یک اخطار ثبت می‌کند؛ اخطار سوم = ریست کشور + مسدودی."""
    if uid not in data.get("users", {}) or uid in ADMINS:
        return False
    user = data["users"][uid]
    count = warning_count(data, uid) + 1
    user["warnings"] = count
    user.setdefault("warning_log", []).append({
        "reason": reason, "time": datetime.now().isoformat()
    })
    if len(user["warning_log"]) > 20:
        user["warning_log"] = user["warning_log"][-20:]
    save_data(data)
    if count >= MAX_WARNINGS:
        my = next((code for code, info in countries.items() if info.get("owner") == uid), None)
        if my:
            info = countries[my]
            info["owner"] = None
            info["defense"] = False
            info["damage_taken"] = 0
        user["has_country"] = False
        user["coins"] = 0
        user["faction"] = None
        data.setdefault("user_eq", {})[uid] = {}
        data.setdefault("user_packs", {})[uid] = []
        data.setdefault("banned_users", [])
        if uid not in data["banned_users"]:
            data["banned_users"].append(uid)
        save_data(data)
        save_countries(countries)
        if notify:
            try:
                await bot.send_message(uid,
                    "🚫 اخطار سوم ثبت شد.\n"
                    "💥 کشور شما ریست شد.\n"
                    "🔒 حساب شما مسدود شد.\n\n"
                    "💰 مبالغ پرداخت‌شده برای پک‌ها و خریدها قابل استرداد نیستند.")
            except Exception:
                pass
        return True
    if notify:
        try:
            await bot.send_message(uid,
                f"⚠️ اخطار شماره {count}/{MAX_WARNINGS}\n"
                f"📌 دلیل: {reason}\n"
                f"🔴 اخطار سوم باعث ریست کشور و مسدودی می‌شود.")
        except Exception:
            pass
    return True

def contains_bad_word(text):
    t = (text or "").strip().lower()
    return any(w in t for w in BAD_WORDS)

def get_rules_menu():
    b = ChatKeypadBuilder()
    b.row(b.button(id="rules", text="📜 قوانین"))
    b.row(b.button(id="back_to_menu", text="🏠 بازگشت"))
    return b.build(resize_keyboard=True, on_time_keyboard=True)

# ---------- alliances ----------
def load_alliance():
    try:
        if ALLIANCE_FILE.exists():
            with ALLIANCE_FILE.open('r',encoding='utf-8') as f: return json.load(f)
    except: pass
    d={"alliances":{},"user_alliance":{},"traitor_until":{}}
    save_alliance(d)
    return d
def save_alliance(d):
    try:
        with ALLIANCE_FILE.open('w',encoding='utf-8') as f: json.dump(d,f,indent=4,ensure_ascii=False)
    except: pass
def get_al(ad,uid):
    name=ad["user_alliance"].get(uid)
    if name and name in ad["alliances"]: return name,ad["alliances"][name]
    return None,None
def is_leader(ad,uid):
    name=ad["user_alliance"].get(uid)
    return name in ad.get("alliances",{}) and ad["alliances"][name]["leader"]==uid

# ---------- file loaders ----------
def safe_json_load(file,default):
    if file.exists():
        try:
            with file.open('r',encoding='utf-8') as f: return json.load(f)
        except: pass
    return default

def load_un():
    d=safe_json_load(UN_FILE,{"leader":None,"members":[],"requests":[],"resolutions":[],"created_at":datetime.now().isoformat()})
    save_un(d)
    return d
def save_un(d):
    try:
        with UN_FILE.open('w',encoding='utf-8') as f: json.dump(d,f,indent=4,ensure_ascii=False)
    except: pass

def load_countries():
    d=safe_json_load(COUNTRIES_FILE,None)
    if d is None:
        d={}
    # Migration: add any newly introduced countries without touching existing ownership.
    for c in COUNTRIES:
        d.setdefault(c["code"],{"flag":c["flag"],"name":c["name"],"emoji":c["emoji"],"owner":None,"defense":False,"damage_taken":0,"power_bonus":c["bonus"]})
    return d
def save_countries(cd):
    try:
        with COUNTRIES_FILE.open('w',encoding='utf-8') as f: json.dump(cd,f,indent=4,ensure_ascii=False)
    except: pass

def load_data():
    d=safe_json_load(DATA_FILE,None)
    if d is None:
        d={"users":{},"banned_users":[],"user_eq":{},"user_packs":{},"attack_logs":[],"bot_country":None,"bot_last_action":None}
    for k,v in {"users":{},"banned_users":[],"user_eq":{},"user_packs":{},"attack_logs":[],"bot_country":None,"bot_last_action":None,"daily_rewards":{},"coin_transfers":[]}.items():
        if k not in d: d[k]=v
    for uid,u in d.get("users",{}).items():
        u.setdefault("warnings",0); u.setdefault("warning_log",[]); u.setdefault("daily_statements",{}); u.setdefault("faction",None)
    return d
def save_data(data):
    try:
        with DATA_FILE.open('w',encoding='utf-8') as f: json.dump(data,f,indent=4,ensure_ascii=False)
    except: pass

def load_bot_status():
    d=safe_json_load(BOT_STATUS_FILE,{"online":True})
    save_bot_status(d)
    return d
def save_bot_status(s):
    try:
        with BOT_STATUS_FILE.open('w',encoding='utf-8') as f: json.dump(s,f,indent=4,ensure_ascii=False)
    except: pass

# ---------- bot AI ----------
async def bot_ai(bot,data,countries):
    now=datetime.now()
    last=data.get("bot_last_action")
    if last:
        try:
            last_time=datetime.fromisoformat(last)
            if (now-last_time).total_seconds()<3600: return
        except: pass
    data["bot_last_action"]=now.isoformat()
    un=load_un()
    if not un.get("leader"): un["leader"]="BOT_AI"; save_un(un)
    # Recover an existing AI country before creating a new one.
    existing_ai = next((c for c, info in countries.items() if info.get("owner")=="BOT_AI"), None)
    if existing_ai:
        data["bot_country"] = existing_ai
        countries[existing_ai].setdefault("defense", True)
    elif not data.get("bot_country") or data.get("bot_country") not in countries:
        free=[(c,i) for c,i in countries.items() if not i.get("owner")]
        if free:
            bot_code,info=random.choice(free)
            countries[bot_code]["owner"]="BOT_AI"
            countries[bot_code]["defense"]=True
            data["bot_country"]=bot_code
    # Always ensure the AI has a usable arsenal, without overwriting existing stock.
    if "user_eq" not in data: data["user_eq"]={}
    bot_eq=data["user_eq"].setdefault("BOT_AI",{})
    defaults={"اف۲۲":200,"موشک":500,"پدافند":600,"تانک":150,"پهپاد":200,"بمب اتم":20,"خیبرشکن":100,"ناو":50}
    for eq_name, amount in defaults.items():
        if eq_name in EQUIP:
            bot_eq.setdefault(eq_name, amount)
    save_data(data); save_countries(countries)

# ---------- BOT counterattack ----------
async def bot_counterattack(bot, data, countries, attacked_uid, reason=""):
    """Immediately retaliate against a player who attacked BOT_AI.
    This function is intentionally isolated from do_attack so it cannot recursively trigger itself.
    """
    try:
        if attacked_uid == "BOT_AI":
            return
        bot_country = data.get("bot_country")
        if not bot_country or bot_country not in countries:
            bot_country = next((c for c, info in countries.items() if info.get("owner")=="BOT_AI"), None)
        if not bot_country:
            return

        # Find the player's current country.
        target_code = next((c for c, info in countries.items() if info.get("owner")==attacked_uid), None)
        if not target_code or target_code == bot_country:
            return

        bot_eq = data.setdefault("user_eq", {}).setdefault("BOT_AI", {})
        available = [(name, int(amount)) for name, amount in bot_eq.items()
                     if name in EQUIP and int(amount) > 0]
        if not available:
            # Self-heal an empty AI arsenal.
            defaults = {"اف۲۲":200,"موشک":500,"پدافند":600,"تانک":150,
                        "پهپاد":200,"بمب اتم":20,"خیبرشکن":100,"ناو":50}
            for name, amount in defaults.items():
                if name in EQUIP:
                    bot_eq[name] = amount
            available = [(name, int(amount)) for name, amount in bot_eq.items()
                         if name in EQUIP and int(amount) > 0]
        if not available:
            return

        # Prefer a strong but controlled weapon.
        available.sort(key=lambda x: EQUIP[x[0]][3], reverse=True)
        eq_name, stock = available[0]
        use = max(1, min(stock, max(1, stock // 10)))
        eq_power = max(1, int(EQUIP[eq_name][3]))
        attack_power = int(use * eq_power * 0.75)

        target_info = countries[target_code]
        defense = defense_power(data, attacked_uid)
        win_ch = max(0.45, min(0.90, attack_power/(attack_power+defense))) if defense > 0 else 0.85
        # AI retaliates deterministically enough to feel responsive, but not every hit is overwhelming.
        won = random.random() < win_ch
        damage = int(attack_power * (0.55 if won else 0.12))
        if target_info.get("defense"):
            damage = max(0, damage - 150)
        if damage <= 0:
            damage = 1

        bot_eq[eq_name] = max(0, stock-use)
        target_info["damage_taken"] = target_info.get("damage_taken", 0) + damage

        destroyed = False
        if target_code != "US" and target_info["damage_taken"] >= 200000:
            await destroy(bot, data, countries, target_code, attacked_uid)
            destroyed = True

        save_countries(countries)
        save_data(data)

        flag = target_info.get("flag","🌍")
        name = target_info.get("name","کشور")
        result = (
            "🤖⚔️ ضدحمله ربات\n\n"
            f"🎯 هدف: {flag} {name}\n"
            f"💣 سلاح: {eq_name} × {use}\n"
            f"💥 خسارت: {fn(damage)}\n"
            f"📊 خسارت کل: {fn(target_info.get('damage_taken',0))}/۲۰۰,۰۰۰\n"
        )
        if destroyed:
            result += "☠️ کشور شما در ضدحمله نابود شد!"
        elif won:
            result += "🔴 ربات در ضدحمله موفق شد."
        else:
            result += "🟡 ضدحمله ربات انجام شد، اما قدرت آن محدود بود."

        try:
            await bot.send_message(attacked_uid, result, chat_keypad=get_main_menu())
        except Exception:
            pass

        # Notify others without allowing a notification failure to break the attack flow.
        try:
            await broadcast_war(
                bot, data, countries, "BOT_AI", target_code,
                eq_name, use, damage, won,
                "🤖 این حمله، پاسخ مستقیم ربات به حمله قبلی بود."
            )
        except Exception:
            pass
    except Exception as e:
        logger.error(f"BOT counterattack error: {e}\n{traceback.format_exc()}")

# ---------- destroy country ----------
async def destroy(bot,data,countries,code,owner):
    info=countries[code]
    if owner and owner!="BOT_AI" and owner in data.get("users",{}):
        data["users"][owner]["has_country"]=False
        data["users"][owner]["coins"]=0
        data["users"][owner]["faction"]=None
        data["user_eq"][owner]={}
        data["user_packs"][owner]=[]
    countries[code]["owner"]=None; countries[code]["defense"]=False; countries[code]["damage_taken"]=0
    save_data(data); save_countries(countries)
    if owner and owner!="BOT_AI":
        try: await bot.send_message(owner,f"💥 کشور {info['flag']} {info['name']} نابود شد!\nتمامی دارایی‌ها پاک شد.",chat_keypad=get_main_menu())
        except: pass
    for u in data["users"]:
        try: await bot.send_message(u,f"☠️ کشور {info['flag']} {info['name']} نابود شد!")
        except: pass

# ---------- broadcast ----------
async def broadcast_war(bot,data,countries,attacker_uid,target,eq_name,amt,damage,won,extra=""):
    tinfo=countries.get(target,{})
    ac=None
    for c,i in countries.items():
        if i.get("owner")==attacker_uid: ac=i; break
    if not ac or not tinfo: return
    aname=data["users"].get(attacker_uid,{}).get("username","نامشخص")
    towner=tinfo.get("owner")
    tname="🤖 ربات" if towner=="BOT_AI" else data["users"].get(towner,{}).get("username","نامشخص")
    emoji="🏆" if won else "💀"
    txt=f"{st('پیروز شد!','b')}" if won else f"{st('شکست خورد!','b')}"
    col="🟢" if won else "🔴"
    msg=f"🌐 {mh('خبر فوری','📡')}\n\n{col} {ac['flag']} {ac['name']} به {tinfo['flag']} {tinfo['name']} حمله کرد!\n⚔️ مهاجم: {aname}\n🛡 مدافع: {tname}\n💣 سلاح: {eq_name} × {fn(amt)}\n💥 خسارت: {fn(damage)}\n{extra}\nنتیجه: {emoji} {txt}"
    for u in data["users"]:
        try: await bot.send_message(u,msg); await asyncio.sleep(0.05)
        except: pass

# ---------- attack ----------
def record_battle(data, uid, target, won, damage, eq, amount, opponent_owner):
    """Store a small bounded battle history; never raises into the battle flow."""
    try:
        logs=data.setdefault("attack_logs",[])
        logs.append({
            "uid":str(uid), "target":str(target), "won":bool(won),
            "damage":int(damage), "equipment":str(eq), "amount":int(amount),
            "opponent":str(opponent_owner), "time":datetime.now().isoformat()
        })
        if len(logs)>100:
            del logs[:-100]
    except Exception as e:
        logger.error(f"battle history error: {e}")

async def do_attack(bot,cid,data,countries,uid,target,eq,amt):
    if amt<=0: return await bot.send_message(cid,"❌ تعداد باید مثبت باشد.")
    last_attack = data["users"][uid].get("last_attack")
    if last_attack:
        try:
            last_time = datetime.fromisoformat(last_attack)
            if (datetime.now() - last_time).total_seconds() < 300:
                remaining = int(300 - (datetime.now() - last_time).total_seconds())
                return await bot.send_message(cid, f"⏳ {remaining} ثانیه تا حمله بعدی صبر کنید.")
        except: pass

    attacker_code = None
    for c,i in countries.items():
        if i.get("owner")==uid: attacker_code=c; break
    if not attacker_code: return await bot.send_message(cid,"❌ کشور ندارید!",chat_keypad=get_main_menu())
    tinfo=countries.get(target)
    if not tinfo or not tinfo.get("owner"): return await bot.send_message(cid,"❌ هدف نامعتبر!")
    if attacker_code==target: return await bot.send_message(cid,"❌ به خودتان نمی‌توانید حمله کنید!")

    if eq not in EQUIP: return await bot.send_message(cid,"❌ تجهیزات نامعتبر!")
    total = totaleq(data,uid).get(eq,0)
    if total<amt: return await bot.send_message(cid,f"❌ موجودی کافی نیست! (داری: {fn(total)})")

    data["users"][uid]["last_attack"] = datetime.now().isoformat()
    save_data(data)

    user = data["users"][uid]
    fac = user.get("faction")
    atk_bonus = FACTIONS[fac]["atk"] if fac and fac in FACTIONS else 1.0
    towner = tinfo["owner"]
    tdef = defense_power(data,towner)
    eq_power = EQUIP[eq][3]
    attack_power = int(amt*eq_power*atk_bonus)
    win_ch = max(0.2, min(0.85, attack_power/(attack_power+tdef))) if tdef>0 else 0.9
    won = random.random()<win_ch

    used,ok = consume(data,uid,eq,amt)
    if not ok: return await bot.send_message(cid,"❌ مصرف تجهیزات با خطا مواجه شد.")
    remaining = totaleq(data,uid).get(eq,0)

    attacker_flag = countries[attacker_code]["flag"]
    attacker_name = countries[attacker_code]["name"]
    target_flag = tinfo["flag"]
    target_name = tinfo["name"]

    if won:
        dmg = int(attack_power*0.7)
        if countries[target].get("defense"): dmg = max(0,dmg-300)
        countries[target]["damage_taken"] = countries[target].get("damage_taken",0)+dmg
        destroyed = False
        if target!="US" and countries[target]["damage_taken"]>=200000:
            if towner in data.get("users",{}):
                await destroy(bot,data,countries,target,towner)
                destroyed=True
        loot_text = ""
        if not destroyed and towner!="BOT_AI" and random.random()<0.4:
            loot_item = random.choice(list(EQUIP.keys()))
            loot_amt = random.randint(1,5)
            addeq(data,uid,loot_item,loot_amt)
            loot_text = f"\n🎁 غنیمت: {loot_item} × {loot_amt}"
        if destroyed: loot_text += "\n☠️ کشور هدف نابود شد!"
        addc(data,uid,100)
        record_battle(data, uid, target, True, dmg, eq, used, towner)
        save_countries(countries); save_data(data)
        user_coins = get_coins(data,uid)
        result = f"{mh('گزارش نبرد','⚔️')}\n\n🏆 پیروز شدید!\n\n🗡 {attacker_flag} {attacker_name}\n🎯 {target_flag} {target_name}\n💣 {eq} × {fn(used)}\n📦 موجودی: {fn(remaining)}\n⚔️ قدرت حمله: {fn(attack_power)}\n🛡 پدافند دشمن: {fn(tdef)}\n📊 شانس برد: {int(win_ch*100)}٪\n💥 خسارت: {fn(dmg)} (کل: {fn(countries[target].get('damage_taken',0))}/۲۰۰,۰۰۰)\n{loot_text}\n🪙 +۱۰۰ کوین\n🪙 موجودی: {fn(user_coins)}"
        await bot.send_message(cid, result, chat_keypad=get_main_menu())
        await broadcast_war(bot,data,countries,uid,target,eq,used,dmg,True,loot_text)
        if towner=="BOT_AI":
            await bot_counterattack(bot,data,countries,uid,"player_won")
    else:
        dmg = int(attack_power*0.15)
        if countries[target].get("defense"): dmg = max(0,dmg-200)
        countries[target]["damage_taken"] = countries[target].get("damage_taken",0)+dmg
        destroyed = False
        if target!="US" and countries[target]["damage_taken"]>=200000:
            if towner in data.get("users",{}):
                await destroy(bot,data,countries,target,towner)
                destroyed=True
        casualty = ""
        if destroyed: casualty = "\n☠️ کشور هدف نابود شد!"
        addc(data,uid,-20)
        record_battle(data, uid, target, False, dmg, eq, used, towner)
        save_countries(countries); save_data(data)
        user_coins = get_coins(data,uid)
        result = f"{mh('گزارش نبرد','⚔️')}\n\n💀 شکست خوردید!\n\n🗡 {attacker_flag} {attacker_name}\n🎯 {target_flag} {target_name}\n💣 {eq} × {fn(used)}\n📦 موجودی: {fn(remaining)}\n⚔️ قدرت حمله: {fn(attack_power)}\n🛡 پدافند دشمن: {fn(tdef)}\n📊 شانس برد: {int(win_ch*100)}٪\n💥 خسارت: {fn(dmg)} (کل: {fn(countries[target].get('damage_taken',0))}/۲۰۰,۰۰۰)\n{casualty}\n🪙 -۲۰ کوین\n🪙 موجودی: {fn(user_coins)}"
        await bot.send_message(cid, result, chat_keypad=get_main_menu())
        await broadcast_war(bot,data,countries,uid,target,eq,used,dmg,False,casualty)
        if towner=="BOT_AI":
            await bot_counterattack(bot,data,countries,uid,"player_lost")

async def send_battle_report(bot, cid, data, countries, uid):
    logs=[x for x in data.get("attack_logs",[]) if str(x.get("uid"))==str(uid)]
    logs=logs[-10:][::-1]
    if not logs:
        return await bot.send_message(cid,"📜 هنوز هیچ نبردی در تاریخچه شما ثبت نشده است.",chat_keypad=get_main_menu())
    wins=sum(1 for x in logs if x.get("won"))
    total_damage=sum(int(x.get("damage",0)) for x in logs)
    lines=["📜 گزارش ۱۰ نبرد اخیر","","🏆 پیروزی: %d"%wins,"⚔️ نبردها: %d"%len(logs),f"💥 مجموع خسارت: {fn(total_damage)}",""]
    for x in logs:
        target=x.get("target","?")
        name=countries.get(target,{}).get("name",target)
        icon="🏆" if x.get("won") else "💀"
        lines.append(f"{icon} {name} | {x.get('equipment','-')} × {x.get('amount',0)} | 💥{fn(int(x.get('damage',0)))}")
    await bot.send_message(cid,"\n".join(lines),chat_keypad=get_main_menu())

# ---------- daily reward / leave ----------
async def daily(bot,cid,data,uid):
    today=date.today().isoformat()
    if "daily_rewards" not in data: data["daily_rewards"]={}
    if data["daily_rewards"].get(uid)==today: return await bot.send_message(cid,"❌ امروز دریافت کرده‌اید!")
    data["daily_rewards"][uid]=today
    addc(data,uid,500)
    await bot.send_message(cid,f"🎁 ۵۰۰ کوین دریافت کردید!\n🪙 موجودی: {fn(get_coins(data,uid))}",chat_keypad=get_main_menu())

async def leave_country(bot,cid,data,countries,uid):
    my=None
    for c,i in countries.items():
        if i.get("owner")==uid: my=c; break
    if not my: return await bot.send_message(cid,"❌ کشوری ندارید!")
    info=countries[my]
    data["users"][uid]["has_country"]=False
    data["users"][uid]["coins"]=0
    data["users"][uid]["faction"]=None
    data["user_eq"][uid]={}
    data["user_packs"][uid]=[]
    countries[my]["owner"]=None; countries[my]["defense"]=False; countries[my]["damage_taken"]=0
    save_data(data); save_countries(countries)
    await bot.send_message(cid,f"🚪 کشور {info['flag']} {info['name']} را ترک کردید!\n💀 تمام دارایی‌ها پاک شد.",chat_keypad=get_main_menu())


async def admin_reset_user(bot, data, countries, uid):
    if uid not in data.get("users",{}): return False
    for code,info in countries.items():
        if info.get("owner")==uid:
            info["owner"]=None; info["defense"]=False; info["damage_taken"]=0
    u=data["users"][uid]
    u.update({"coins":0,"has_country":False,"faction":None,"warnings":0,"warning_log":[]})
    data.setdefault("user_eq",{})[uid]={}
    data.setdefault("user_packs",{})[uid]=[]
    save_data(data); save_countries(countries)
    try: await bot.send_message(uid,"👑 ادمین حساب شما را ریست کرد.")
    except Exception: pass
    return True

# ---------- admin functions ----------
async def admin_change_owner(bot,cid,data,countries,country_code,new_owner_uid):
    if country_code not in countries:
        await bot.send_message(cid,"❌ کشور نامعتبر!")
        return
    info=countries[country_code]
    old_owner=info.get("owner")
    if old_owner and old_owner!="BOT_AI" and old_owner in data.get("users",{}):
        data["users"][old_owner]["has_country"]=False
    if new_owner_uid not in data.get("users",{}):
        await bot.send_message(cid,"❌ کاربر مقصد وجود ندارد!")
        return
    for c,i in countries.items():
        if i.get("owner")==new_owner_uid and c!=country_code:
            await bot.send_message(cid,"❌ کاربر مقصد قبلاً یک کشور دارد!")
            return
    info["owner"]=new_owner_uid
    if "has_country" not in data["users"][new_owner_uid]: data["users"][new_owner_uid]["has_country"]=True
    data["users"][new_owner_uid]["has_country"]=True
    save_data(data); save_countries(countries)
    new_name=data["users"][new_owner_uid].get("username",new_owner_uid[:10])
    await bot.send_message(cid,f"✅ مالک {info['flag']} {info['name']} به {new_name} (`{new_owner_uid}`) تغییر یافت.")

async def admin_reset_country(bot,cid,data,countries,country_code):
    if country_code not in countries:
        await bot.send_message(cid,"❌ کشور نامعتبر!")
        return
    info=countries[country_code]
    old_owner=info.get("owner")
    if old_owner and old_owner!="BOT_AI" and old_owner in data.get("users",{}):
        data["users"][old_owner]["has_country"]=False
        data["users"][old_owner]["coins"]=0
        data["users"][old_owner]["faction"]=None
        data["user_eq"][old_owner]={}
        data["user_packs"][old_owner]=[]
    info["owner"]=None; info["defense"]=False; info["damage_taken"]=0
    save_data(data); save_countries(countries)
    await bot.send_message(cid,f"✅ کشور {info['flag']} {info['name']} کاملاً ریست شد.")

# ---------- keyboards ----------
def get_main_menu():
    b=ChatKeypadBuilder()
    b.row(b.button(id="buy_country",text="🌍 کشورگیری"),b.button(id="attack",text="⚔️ حمله"))
    b.row(b.button(id="my_info",text="👤 پروفایل"),b.button(id="equipment_shop",text="🛒 فروشگاه"))
    b.row(b.button(id="buy_single",text="🎯 خرید تجهیزات"),b.button(id="send_message",text="📨 بیانیه"))
    b.row(b.button(id="top_owners",text="🏆 رتبه‌بندی"),b.button(id="un_menu",text="🌐 سازمان ملل"))
    b.row(b.button(id="faction_menu",text="⚔️ گروهک‌ها"),b.button(id="daily_reward",text="🎁 پاداش روزانه"))
    b.row(b.button(id="alliance_menu",text="🤝 اتحادها"),b.button(id="battle_report",text="📜 گزارش جنگ"))
    b.row(b.button(id="rules",text="📜 قوانین"),b.button(id="my_warnings",text="⚠️ اخطارهای من"))
    b.row(b.button(id="leave_country",text="🚪 خروج از کشور"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_alliance_menu(is_member,is_leader):
    b=ChatKeypadBuilder()
    b.row(b.button(id="alliance_list",text="📋 لیست اتحادها"))
    if not is_member:
        b.row(b.button(id="alliance_create",text="📝 ایجاد اتحاد"))
    else:
        b.row(b.button(id="alliance_info",text="🔍 اتحاد من"))
        b.row(b.button(id="alliance_chat",text="💬 چت اتحاد"))
        b.row(b.button(id="alliance_leave",text="🚪 خروج"))
        b.row(b.button(id="alliance_betray",text="💀 خیانت"))
        if is_leader:
            b.row(b.button(id="alliance_manage",text="👥 مدیریت اعضا"))
            b.row(b.button(id="alliance_disband",text="❌ انحلال"))
    b.row(b.button(id="back_to_menu",text="🏠 بازگشت"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_un_menu():
    b=ChatKeypadBuilder()
    b.row(b.button(id="un_info",text="🏛 اطلاعات سازمان"),b.button(id="un_join",text="📝 درخواست عضویت"))
    b.row(b.button(id="un_members",text="👥 اعضا"),b.button(id="un_resolutions",text="📜 قطعنامه‌ها"))
    b.row(b.button(id="un_request_list",text="📋 درخواست‌ها"),b.button(id="back_to_menu",text="🏠 بازگشت"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_faction_menu():
    b=ChatKeypadBuilder()
    b.row(b.button(id="faction_sepah",text="🛡⚔️ سپاه"),b.button(id="faction_darkweb",text="💀🌐 دارک وب"))
    b.row(b.button(id="faction_hezbollah",text="⚔️🕊 حزب‌الله"),b.button(id="faction_info",text="📊 اطلاعات"))
    b.row(b.button(id="back_to_menu",text="🏠 بازگشت"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_countries_kb(countries,page=0):
    b=ChatKeypadBuilder()
    lst=list(countries.items())
    start=page*12; end=start+12; cur=lst[start:end]
    row=[]
    for code,info in cur:
        st="🟢" if info.get("owner") else "⚪"
        bt="🤖" if info.get("owner")=="BOT_AI" else ""
        row.append(b.button(id=f"country_{code}",text=f"{info['flag']} {st}{bt}"))
        if len(row)==3: b.row(*row); row=[]
    if row: b.row(*row)
    nav=[]
    if page>0: nav.append(b.button(id=f"countries_page_{page-1}",text="◀️ قبل"))
    nav.append(b.button(id="back_to_menu",text="🏠 خانه"))
    if end<len(lst): nav.append(b.button(id=f"countries_page_{page+1}",text="بعد ▶️"))
    if nav: b.row(*nav)
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_attack_countries_kb(countries,page=0):
    b=ChatKeypadBuilder()
    active=[(c,i) for c,i in countries.items() if i.get("owner")]
    start=page*9; end=start+9; cur=active[start:end]
    row=[]
    for code,info in cur:
        bt=" 🤖" if info.get("owner")=="BOT_AI" else ""
        row.append(b.button(id=f"attack_{code}",text=f"{info['flag']} {info['name']}{bt}"))
        if len(row)==3: b.row(*row); row=[]
    if row: b.row(*row)
    nav=[]
    if page>0: nav.append(b.button(id=f"attack_page_{page-1}",text="◀️"))
    nav.append(b.button(id="back_to_menu",text="🏠"))
    if end<len(active): nav.append(b.button(id=f"attack_page_{page+1}",text="▶️"))
    if nav: b.row(*nav)
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_admin_country_kb(countries,action_prefix):
    b=ChatKeypadBuilder()
    lst=list(countries.items())
    row=[]
    for code,info in lst:
        row.append(b.button(id=f"{action_prefix}{code}",text=f"{info['flag']} {info['name']}"))
        if len(row)==3: b.row(*row); row=[]
    if row: b.row(*row)
    b.row(b.button(id="cancel",text="❌ لغو"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_attack_eq_kb(ueq,upacks,target):
    b=ChatKeypadBuilder()
    items={}
    for eq,cnt in ueq.items():
        if cnt>0: items[eq]=items.get(eq,0)+cnt
    row=[]
    for eq,cnt in list(items.items())[:24]:
        short=eq[:10]+".." if len(eq)>10 else eq
        row.append(b.button(id=f"eq_{target}_{eq}",text=f"🔸 {short} ({cnt})"))
        if len(row)==2: b.row(*row); row=[]
    if row: b.row(*row)
    b.row(b.button(id="back_to_menu",text="🏠 بازگشت"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_attack_amt_kb(target,eq,max_cnt):
    b=ChatKeypadBuilder()
    amounts=[1,5,10,25,50,100,200,500]
    row=[]
    for amt in amounts:
        if amt<=max_cnt: row.append(b.button(id=f"amt_{target}_{eq}_{amt}",text=f"🎯 {amt}"))
        if len(row)==4: b.row(*row); row=[]
    if row: b.row(*row)
    b.row(b.button(id=f"custom_{target}_{eq}",text="✏️ تعداد دلخواه"),b.button(id="back_to_menu",text="🏠"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_single_eq_kb():
    b=ChatKeypadBuilder()
    cats={}
    for eq,info in EQUIP.items():
        cats.setdefault(info[2],[]).append((eq,info))
    for cat,items in cats.items():
        row=[]
        for eq,info in items[:4]:
            row.append(b.button(id=f"buyeq_{eq}",text=f"{info[1]} {eq} | 🪙{info[0]}"))
            if len(row)==3: b.row(*row); row=[]
        if row: b.row(*row)
    b.row(b.button(id="back_to_menu",text="🏠 بازگشت"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_shop_menu():
    b=ChatKeypadBuilder()
    for pn,pi in PACKS.items():
        b.row(b.button(id=f"shop_{pn}",text=f"{pi[1]} {pn} | 💰{fn(pi[0])}"))
    b.row(b.button(id="back_to_menu",text="🏠 بازگشت"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_admin_panel(bs):
    b=ChatKeypadBuilder()
    b.row(b.button(id="ad_stats",text="📊 آمار"),b.button(id="ad_countries",text="🌍 کشورها"))
    b.row(b.button(id="ad_users",text="👥 کاربران"),b.button(id="ad_broadcast",text="📣 همگانی"))
    b.row(b.button(id="ad_add_coins",text="🪙 +کوین"),b.button(id="ad_remove_coins",text="🪙 -کوین"))
    b.row(b.button(id="ad_add_pack",text="🎁 +پک"),b.button(id="ad_add_eq",text="➕ +تجهیزات"))
    b.row(b.button(id="ad_remove_eq",text="➖ -تجهیزات"),b.button(id="ad_un_manage",text="🌐 مدیریت سازمان ملل"))
    b.row(b.button(id="ad_change_owner",text="🔄 تغییر مالک"),b.button(id="ad_reset_country",text="♻️ ریست کشور"))
    b.row(b.button(id="ad_ban",text="🚫 مسدود"),b.button(id="ad_unban",text="✅ رفع مسدود"))
    b.row(b.button(id="ad_warn",text="⚠️ اخطار"),b.button(id="ad_unwarn",text="🧹 حذف اخطار"))
    b.row(b.button(id="ad_reset_user",text="👑 ریست کاربر"),b.button(id="ad_give_country",text="🌍 اعطای کشور"))
    b.row(b.button(id="ad_user_search",text="🔎 جستجوی کاربر"),b.button(id="ad_economy",text="💰 اقتصاد"))
    b.row(b.button(id="ad_system",text="🛡 وضعیت سیستم"),b.button(id="ad_backup",text="💾 پشتیبان"))
    if bs.get("online",True): b.row(b.button(id="ad_bot_off",text="🔴 خاموش کردن ربات"))
    else: b.row(b.button(id="ad_bot_on",text="🟢 روشن کردن ربات"))
    b.row(b.button(id="ad_to_main_menu",text="🏠 منوی اصلی"),b.button(id="ad_close",text="🔒 خروج"))
    return b.build(resize_keyboard=True,on_time_keyboard=True)

def get_admin_back():
    b=ChatKeypadBuilder(); b.row(b.button(id="ad_back_to_admin",text="🔙 پنل ادمین"),b.button(id="ad_to_main_menu",text="🏠 منوی اصلی")); return b.build(resize_keyboard=True,on_time_keyboard=True)
def get_admin_back_cancel():
    b=ChatKeypadBuilder(); b.row(b.button(id="ad_back_to_admin",text="🔙 پنل ادمین"),b.button(id="cancel",text="❌ لغو")); return b.build(resize_keyboard=True,on_time_keyboard=True)
def get_back():
    b=ChatKeypadBuilder(); b.row(b.button(id="back_to_menu",text="🏠 بازگشت")); return b.build(resize_keyboard=True,on_time_keyboard=True)
def get_cancel():
    b=ChatKeypadBuilder(); b.row(b.button(id="cancel",text="❌ لغو")); return b.build(resize_keyboard=True,on_time_keyboard=True)

# ---------- bot instance ----------
bot = Robot(token=BOT_TOKEN)
user_states={}
admin_session={}

@bot.on_message()
async def handler(bot_instance:Robot,msg:Message):
    global user_states,admin_session
    try:
        cid=msg.chat_id
        text=msg.text.strip() if msg.text else ""
        cb=None
        if hasattr(msg,'aux_data') and msg.aux_data:
            cb=getattr(msg.aux_data,'button_id',None)
    except Exception as e:
        logger.error(f"Error in handler initial block: {e}")
        return

    try:
        bs=load_bot_status()
        is_admin=str(cid) in ADMINS
        uid=str(cid)
        if not bs.get("online",True) and not is_admin:
            if text=="/start" or cb: await bot_instance.send_message(cid,"😴 ربات در حال استراحت است.")
            return
        data=load_data()
        countries=load_countries()
        adata=load_alliance()
        if uid in data.get("banned_users",[]):
            await msg.reply("🚫 مسدود هستید."); return
        username=guser(msg)
        if uid not in data.get("users",{}):
            data["users"][uid]={"join_date":datetime.now().isoformat(),"coins":1000,"username":username or f"فرمانده{uid[:6]}","has_country":False,"daily_statements":{},"faction":None,"warnings":0,"warning_log":[]}
            save_data(data)
        data["users"][uid].setdefault("warnings",0); data["users"][uid].setdefault("warning_log",[])
        if username and data["users"][uid].get("username")!=username:
            data["users"][uid]["username"]=username; save_data(data)
        # Moderation: each detected insult = 1 warning.
        if text and not is_admin and contains_bad_word(text):
            await issue_warning(bot_instance, data, countries, uid, "توهین/فحاشی")
            return
        await bot_ai(bot_instance,data,countries)

        # admin states
        if user_states.get(cid,{}).get("wait_change_owner_uid"):
            new_owner_uid=text.strip()
            country_code=user_states[cid]["country_code"]
            await admin_change_owner(bot_instance,cid,data,countries,country_code,new_owner_uid)
            user_states[cid]={}; return
        if user_states.get(cid,{}).get("confirm_reset"):
            if text.strip().lower()=="بله":
                country_code=user_states[cid]["country_code"]
                await admin_reset_country(bot_instance,cid,data,countries,country_code)
            else:
                await bot_instance.send_message(cid,"❌ عملیات لغو شد.")
            user_states[cid]={}; return

        # alliance creation / chat states
        if user_states.get(cid,{}).get("creating_alliance"):
            new_name=text.strip()
            if not new_name: await bot_instance.send_message(cid,"❌ نام نامعتبر!"); user_states[cid]={}; return
            if new_name in adata["alliances"]: await bot_instance.send_message(cid,"❌ این نام قبلاً استفاده شده!"); user_states[cid]={}; return
            success,msg=remc(data,uid,5000)
            if not success: await bot_instance.send_message(cid,f"❌ {msg}"); user_states[cid]={}; return
            adata["alliances"][new_name]={"leader":uid,"members":[uid],"created":datetime.now().isoformat()}
            adata["user_alliance"][uid]=new_name
            save_alliance(adata); save_data(data)
            await bot_instance.send_message(cid,f"✅ اتحاد {new_name} ایجاد شد!",chat_keypad=get_main_menu())
            user_states[cid]={}; return
        if user_states.get(cid,{}).get("alliance_chat"):
            name,_=get_al(adata,uid)
            if not name: await bot_instance.send_message(cid,"❌ خطا!"); user_states[cid]={}; return
            sender=data["users"][uid].get("username",uid[:10])
            msg_text=f"💬 [{name}] {sender}:\n{text}"
            for m in adata["alliances"][name]["members"]:
                try: await bot_instance.send_message(m,msg_text)
                except: pass
            await bot_instance.send_message(cid,"✅ پیام ارسال شد.")
            user_states[cid]={}; return

        in_admin=admin_session.get(cid,False)

        if text=="/start":
            user_states[cid]={}
            await bot_instance.send_message(cid,f"{mh('🌍 جنگ جهانی')}\n\n🆔 {gid(msg,uid)}\n🔑 شناسه: {st(uid,'m')}\n🪙 کوین: {fn(get_coins(data,uid))}",chat_keypad=get_main_menu())
            return
        if text=="/admin":
            user_states[cid]={"wait_pass":True}
            await bot_instance.send_message(cid,"🔐 رمز:"); return
        if user_states.get(cid,{}).get("wait_pass"):
            if text==ADMIN_PASSWORD:
                admin_session[cid]=True; user_states[cid]={}
                await bot_instance.send_message(cid,"✅ ورود موفق",chat_keypad=get_admin_panel(bs))
            else: user_states[cid]={}; await bot_instance.send_message(cid,"❌ رمز اشتباه!")
            return

        if cb=="back_to_menu":
            user_states[cid]={}
            await bot_instance.send_message(cid,"🏠 منوی اصلی:",chat_keypad=get_main_menu()); return
        if cb=="cancel":
            user_states[cid]={}
            await bot_instance.send_message(cid,"❌ لغو شد.",chat_keypad=get_admin_panel(bs) if in_admin else get_main_menu()); return

        if in_admin:
            if cb=="ad_to_main_menu": admin_session[cid]=False; await bot_instance.send_message(cid,"🏠 منوی اصلی:",chat_keypad=get_main_menu()); return
            if cb=="ad_back_to_admin": await bot_instance.send_message(cid,"🔙 پنل مدیریت:",chat_keypad=get_admin_panel(bs)); return
            if cb=="ad_close": admin_session[cid]=False; await bot_instance.send_message(cid,"🔒 پنل بسته شد.",chat_keypad=get_main_menu()); return
            if cb=="ad_bot_off": bs["online"]=False; save_bot_status(bs); await bot_instance.send_message(cid,"🔴 ربات خاموش شد.",chat_keypad=get_admin_panel(bs)); return
            if cb=="ad_bot_on": bs["online"]=True; save_bot_status(bs); await bot_instance.send_message(cid,"🟢 ربات روشن شد.",chat_keypad=get_admin_panel(bs)); return
            if cb=="ad_stats":
                users=len(data["users"]); banned=len(data.get("banned_users",[]))
                total_coins=sum(u.get("coins",0) for u in data["users"].values())
                taken=sum(1 for c in countries.values() if c.get("owner"))
                un=load_un()
                stats=f"📊 آمار\n👥 کاربران: {users}\n🚫 مسدود: {banned}\n🪙 مجموع کوین: {fn(total_coins)}\n🌍 کشورها: {len(countries)} (تصرف‌شده: {taken})\n🌐 اعضای UN: {len(un.get('members',[]))}"
                await bot_instance.send_message(cid,stats,chat_keypad=get_admin_back()); return
            if cb=="ad_countries":
                txt="🌍 کشورها:\n"
                for c,i in countries.items():
                    if i.get("owner"): own=i["owner"]; name="🤖 ربات" if own=="BOT_AI" else data["users"].get(own,{}).get("username",own[:15]); txt+=f"\n{i['flag']} {i['name']} | 👤 {name} | 🆔 `{own}`"
                    else: txt+=f"\n{i['flag']} {i['name']} | ⚪ آزاد"
                await bot_instance.send_message(cid,txt,chat_keypad=get_admin_back()); return
            if cb=="ad_users":
                txt="👥 کاربران:\n"
                for u,info in list(data["users"].items())[:20]:
                    sts="🚫" if u in data.get("banned_users",[]) else "✅"
                    txt+=f"\n{sts} `{u}` | {info.get('username','؟')} | 🪙 {fn(get_coins(data,u))}"
                await bot_instance.send_message(cid,txt,chat_keypad=get_admin_back()); return
            if cb=="ad_broadcast":
                user_states[cid]={"broadcast":True}
                await bot_instance.send_message(cid,"📣 پیام همگانی:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("broadcast"):
                cnt=0
                for u2 in data["users"]:
                    if u2 not in ADMINS:
                        try: await bot_instance.send_message(u2,f"📣 {mh('پیام فرماندهی')}\n\n{text}"); cnt+=1
                        except: pass
                await bot_instance.send_message(cid,f"✅ به {cnt} نفر ارسال شد.",chat_keypad=get_admin_back())
                user_states[cid]={}; return
            if cb=="ad_add_coins":
                user_states[cid]={"add_coins":True}
                await bot_instance.send_message(cid,"🪙 شناسه و مقدار:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("add_coins"):
                try:
                    parts=text.split(); target=parts[0]; amt=int(parts[1])
                    if amt<=0: await bot_instance.send_message(cid,"❌ مقدار باید مثبت باشد")
                    elif target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                    else: addc(data,target,amt); await bot_instance.send_message(cid,f"✅ {amt} کوین اضافه شد.")
                except: await bot_instance.send_message(cid,"❌ فرمت اشتباه")
                user_states[cid]={}; return
            if cb=="ad_remove_coins":
                user_states[cid]={"remove_coins":True}
                await bot_instance.send_message(cid,"🪙 شناسه و مقدار:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("remove_coins"):
                try:
                    parts=text.split(); target=parts[0]; amt=int(parts[1])
                    ok,msg=remc(data,target,amt)
                    await bot_instance.send_message(cid,f"✅ {amt} کوین کم شد." if ok else f"❌ {msg}")
                except: await bot_instance.send_message(cid,"❌ فرمت اشتباه")
                user_states[cid]={}; return
            if cb=="ad_add_pack":
                user_states[cid]={"add_pack":True}
                await bot_instance.send_message(cid,f"🎁 شناسه و نام پک:\n{', '.join(PACKS.keys())}",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("add_pack"):
                try:
                    parts=text.split(" ",1); target=parts[0]; pack_name=parts[1]
                    if target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                    elif pack_name not in PACKS: await bot_instance.send_message(cid,"❌ پک نامعتبر!")
                    else:
                        if "user_packs" not in data: data["user_packs"]={}
                        if target not in data["user_packs"]: data["user_packs"][target]=[]
                        if pack_name in data["user_packs"][target]: await bot_instance.send_message(cid,"⚠️ کاربر این پک را دارد!")
                        else:
                            data.setdefault("user_packs", {}).setdefault(target, [])
                            data.setdefault("user_eq", {}).setdefault(target, {})
                            data["user_packs"][target].append(pack_name)
                            # Grant every equipment item contained in the pack.
                            pack_items = PACKS[pack_name][3] if len(PACKS[pack_name]) > 3 else {}
                            for eq_name, amount in pack_items.items():
                                if eq_name in EQUIP:
                                    data["user_eq"][target][eq_name] = data["user_eq"][target].get(eq_name, 0) + int(amount)
                            save_data(data)
                            await bot_instance.send_message(cid,f"✅ پک {pack_name} اضافه شد.\n🧰 تجهیزات داخل پک هم به موجودی کاربر اضافه شدند.")
                except: await bot_instance.send_message(cid,"❌ فرمت اشتباه")
                user_states[cid]={}; return
            if cb=="ad_add_eq":
                user_states[cid]={"add_eq":True}
                await bot_instance.send_message(cid,"➕ شناسه، تجهیزات و تعداد:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("add_eq"):
                try:
                    parts=text.split(); target=parts[0]; eq_name=parts[1]; count=int(parts[2])
                    if count<=0: await bot_instance.send_message(cid,"❌ تعداد باید مثبت باشد")
                    elif target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                    elif eq_name not in EQUIP: await bot_instance.send_message(cid,"❌ تجهیزات نامعتبر!")
                    else: addeq(data,target,eq_name,count); await bot_instance.send_message(cid,f"✅ {count} {eq_name} اضافه شد.")
                except: await bot_instance.send_message(cid,"❌ فرمت اشتباه")
                user_states[cid]={}; return
            if cb=="ad_remove_eq":
                user_states[cid]={"remove_eq":True}
                await bot_instance.send_message(cid,"➖ شناسه، تجهیزات و تعداد:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("remove_eq"):
                try:
                    parts=text.split(); target=parts[0]; eq_name=parts[1]; count=int(parts[2])
                    ok,msg=remeq(data,target,eq_name,count)
                    await bot_instance.send_message(cid,f"✅ {count} {eq_name} کم شد." if ok else f"❌ {msg}")
                except: await bot_instance.send_message(cid,"❌ فرمت اشتباه")
                user_states[cid]={}; return
            if cb=="ad_warn":
                user_states[cid]={"admin_warn":True}
                await bot_instance.send_message(cid,"⚠️ شناسه و دلیل اختیاری:\nمثال: 12345 اسپم",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("admin_warn"):
                parts=text.split(" ",1); target=parts[0]; reason=parts[1] if len(parts)>1 else "تخلف از قوانین"
                if target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                elif target in ADMINS: await bot_instance.send_message(cid,"🛡️ برای ادمین اخطار ثبت نمی‌شود.")
                else:
                    await issue_warning(bot_instance,data,countries,target,reason)
                    await bot_instance.send_message(cid,f"✅ اخطار ثبت شد: {warning_count(data,target)}/{MAX_WARNINGS}")
                user_states[cid]={}; return
            if cb=="ad_unwarn":
                user_states[cid]={"admin_unwarn":True}
                await bot_instance.send_message(cid,"🧹 شناسه کاربر:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("admin_unwarn"):
                target=text.strip()
                if target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                else:
                    data["users"][target]["warnings"]=max(0,warning_count(data,target)-1)
                    save_data(data)
                    await bot_instance.send_message(cid,f"✅ اخطار حذف شد: {warning_count(data,target)}/{MAX_WARNINGS}")
                user_states[cid]={}; return
            if cb=="ad_reset_user":
                user_states[cid]={"admin_reset_user":True}
                await bot_instance.send_message(cid,"👑 شناسه کاربر برای ریست کامل:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("admin_reset_user"):
                target=text.strip()
                if target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                else:
                    await admin_reset_user(bot_instance,data,countries,target)
                    await bot_instance.send_message(cid,"✅ کاربر ریست شد.")
                user_states[cid]={}; return
            if cb=="ad_give_country":
                await bot_instance.send_message(cid,"🌍 کشور مورد نظر:",chat_keypad=get_admin_country_kb(countries,"ad_give_c_")); return
            if cb and cb.startswith("ad_give_c_"):
                code=cb.replace("ad_give_c_","")
                user_states[cid]={"admin_give_country":True,"country_code":code}
                await bot_instance.send_message(cid,"🆔 شناسه کاربر جدید:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("admin_give_country"):
                target=text.strip(); code=user_states[cid]["country_code"]
                if target not in data["users"]: await bot_instance.send_message(cid,"❌ کاربر یافت نشد!")
                elif any(i.get("owner")==target for i in countries.values()): await bot_instance.send_message(cid,"❌ کاربر قبلاً کشور دارد!")
                else:
                    countries[code]["owner"]=target; countries[code]["defense"]=False
                    data["users"][target]["has_country"]=True
                    save_countries(countries); save_data(data)
                    await bot_instance.send_message(cid,f"✅ {countries[code]['flag']} {countries[code]['name']} به کاربر داده شد.")
                user_states[cid]={}; return
            if cb=="ad_user_search":
                user_states[cid]={"admin_search":True}
                await bot_instance.send_message(cid,"🔎 شناسه یا نام کاربر:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("admin_search"):
                q=text.lower(); found=[]
                for u,info in data["users"].items():
                    if q in str(u).lower() or q in str(info.get("username","")).lower():
                        found.append((u,info))
                if not found: out="❌ نتیجه‌ای پیدا نشد."
                else:
                    out="🔎 نتایج:\n" + "\n".join(
                        f"• {info.get('username','؟')} | `{u}` | 🪙 {fn(get_coins(data,u))} | ⚠️ {warning_count(data,u)}"
                        for u,info in found[:15])
                await bot_instance.send_message(cid,out,chat_keypad=get_admin_back())
                user_states[cid]={}; return
            if cb=="ad_economy":
                total=sum(get_coins(data,u) for u in data["users"])
                packs=sum(len(v) for v in data.get("user_packs",{}).values())
                eq=sum(sum(int(x) for x in v.values()) for v in data.get("user_eq",{}).values())
                await bot_instance.send_message(cid,
                    f"💰 اقتصاد سرور\n🪙 مجموع کوین: {fn(total)}\n📦 پک‌های کاربران: {fn(packs)}\n🧰 مجموع تجهیزات: {fn(eq)}",
                    chat_keypad=get_admin_back()); return
            if cb=="ad_system":
                await bot_instance.send_message(cid,
                    f"🛡 وضعیت سیستم\n👥 کاربران: {len(data['users'])}\n🌍 کشورها: {len(countries)}\n🚫 مسدودها: {len(data.get('banned_users',[]))}\n⚠️ مجموع اخطار: {sum(warning_count(data,u) for u in data['users'])}\n🤖 AI: {'فعال' if bs.get('online',True) else 'خاموش'}",
                    chat_keypad=get_admin_back()); return
            if cb=="ad_backup":
                backup_name=f"worldwar_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup={"data":data,"countries":countries,"alliance":adata,"un":load_un(),"status":bs}
                Path(backup_name).write_text(json.dumps(backup,ensure_ascii=False,indent=2),encoding="utf-8")
                await bot_instance.send_message(cid,f"💾 پشتیبان ساخته شد: `{backup_name}`",chat_keypad=get_admin_back()); return

            if cb=="ad_un_manage":
                un=load_un()
                await bot_instance.send_message(cid,f"🌐 مدیریت سازمان ملل\n👑 رئیس: {un.get('leader','ندارد')}\n👥 اعضا: {len(un.get('members',[]))}\n📋 درخواست‌ها: {len(un.get('requests',[]))}",chat_keypad=get_admin_back()); return
            if cb=="ad_ban":
                user_states[cid]={"ban":True}
                await bot_instance.send_message(cid,"🚫 شناسه:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("ban"):
                target=text.strip()
                if target in data.get("banned_users",[]): await bot_instance.send_message(cid,"⚠️ قبلاً مسدود شده!")
                else: data.setdefault("banned_users",[]).append(target); save_data(data); await bot_instance.send_message(cid,"✅ مسدود شد.")
                user_states[cid]={}; return
            if cb=="ad_unban":
                user_states[cid]={"unban":True}
                await bot_instance.send_message(cid,"✅ شناسه:",chat_keypad=get_admin_back_cancel()); return
            if user_states.get(cid,{}).get("unban"):
                target=text.strip()
                if target in data.get("banned_users",[]): data["banned_users"].remove(target); save_data(data); await bot_instance.send_message(cid,"✅ رفع مسدود شد.")
                else: await bot_instance.send_message(cid,"⚠️ مسدود نیست!")
                user_states[cid]={}; return

            if cb=="ad_change_owner":
                await bot_instance.send_message(cid,"🔄 کشور مورد نظر برای تغییر مالک:",chat_keypad=get_admin_country_kb(countries,"ad_chg_c_"))
                return
            if cb.startswith("ad_chg_c_"):
                code=cb.replace("ad_chg_c_","")
                user_states[cid]={"wait_change_owner_uid":True,"country_code":code}
                await bot_instance.send_message(cid,f"🔑 شناسه کاربر جدید برای مالکیت {countries[code]['flag']} {countries[code]['name']}:",chat_keypad=get_cancel())
                return
            if cb=="ad_reset_country":
                await bot_instance.send_message(cid,"♻️ کشور مورد نظر برای ریست:",chat_keypad=get_admin_country_kb(countries,"ad_rst_c_"))
                return
            if cb.startswith("ad_rst_c_"):
                code=cb.replace("ad_rst_c_","")
                user_states[cid]={"confirm_reset":True,"country_code":code}
                await bot_instance.send_message(cid,f"⚠️ مطمئنی می‌خوای {countries[code]['flag']} {countries[code]['name']} رو کامل ریست کنی؟ (بله / خیر)",chat_keypad=get_cancel())
                return

            return

        # user menu
        if cb=="rules":
            await bot_instance.send_message(cid,RULES_TEXT,chat_keypad=get_rules_menu()); return
        if cb=="my_warnings":
            logs=data["users"][uid].get("warning_log",[])
            recent="\n".join(f"• {x.get('reason','تخلف')} | {x.get('time','')[:19]}" for x in logs[-5:])
            await bot_instance.send_message(cid,
                f"⚠️ اخطارهای شما: {warning_count(data,uid)}/{MAX_WARNINGS}\n\n"
                f"{recent or '✅ اخطاری ثبت نشده است.'}\n\n"
                "🔴 اخطار سوم = ریست کشور + مسدودی",
                chat_keypad=get_rules_menu()); return
        if cb=="daily_reward": await daily(bot_instance,cid,data,uid); return
        if cb=="leave_country":
            if not user_states.get(cid,{}).get("confirm_leave"):
                user_states[cid]={"confirm_leave":True}
                await bot_instance.send_message(cid,"🚪 هشدار: تمام دارایی‌ها پاک میشود!\nبرای تأیید دوباره بزنید.",chat_keypad=get_main_menu())
            else: user_states[cid]={}; await leave_country(bot_instance,cid,data,countries,uid)
            return
        if cb=="my_info":
            user=data["users"][uid]; user_coins=get_coins(data,uid); pwr=power(data,uid)
            my=next((i for i in countries.values() if i.get("owner")==uid),None)
            un=load_un()
            un_status="👑 رئیس" if un.get("leader")==uid else ("✅ عضو" if uid in un.get("members",[]) else "❌ غیرعضو")
            fac=user.get("faction")
            fac_name=f"{FACTIONS[fac]['icon']} {FACTIONS[fac]['name']}" if fac and fac in FACTIONS else "❌ ندارد"
            aname,_=get_al(adata,uid); al_str=aname if aname else "❌ ندارد"
            txt=f"👤 پروفایل\n🆔 {gid(msg,uid)}\n🔑 شناسه: {st(uid,'m')}\n🪙 کوین: {fn(user_coins)}\n⚔️ قدرت: {fn(pwr)}\n⚠️ اخطار: {warning_count(data,uid)}/{MAX_WARNINGS}\n🌐 سازمان ملل: {un_status}\n⚔️ گروهک: {fac_name}\n🤝 اتحاد: {al_str}"
            if my: txt+=f"\n🌍 کشور: {my['flag']} {my['name']}\n💥 خسارت: {fn(my.get('damage_taken',0))}/۲۰۰,۰۰۰"
            await bot_instance.send_message(cid,txt); return
        if cb=="alliance_menu":
            await bot_instance.send_message(
                cid,
                "🤝 برای دریافت اتحاد، وارد کانال زیر شوید:\n\n📢 @war_ethad",
                chat_keypad=get_main_menu()
            )
            return
        if cb=="battle_report":
            await send_battle_report(bot_instance,cid,data,countries,uid)
            return
        if cb=="alliance_create":
            if get_al(adata,uid)[0]: return await bot_instance.send_message(cid,"❌ شما قبلاً عضو یک اتحاد هستید!")
            if not any(i.get("owner")==uid for i in countries.values()): return await bot_instance.send_message(cid,"❌ برای ایجاد اتحاد باید کشور داشته باشید!")
            if get_coins(data,uid)<5000: return await bot_instance.send_message(cid,f"❌ هزینه ایجاد اتحاد ۵,۰۰۰ کوین است. موجودی: {fn(get_coins(data,uid))}")
            user_states[cid]={"creating_alliance":True}
            await bot_instance.send_message(cid,"📝 نام اتحاد جدید را وارد کنید:",chat_keypad=get_cancel()); return
        if cb=="alliance_list":
            alliances=adata["alliances"]
            if not alliances: return await bot_instance.send_message(cid,"📋 هیچ اتحادی وجود ندارد.")
            txt="📋 اتحادهای موجود:\n"
            for i,(a_name,a_info) in enumerate(alliances.items(),1):
                leader_name=data["users"].get(a_info["leader"],{}).get("username","نامشخص")
                txt+=f"\n{i}. {a_name} (رهبر: {leader_name}, اعضا: {len(a_info['members'])})"
            await bot_instance.send_message(cid,txt); return
        if cb and cb.startswith("join_alliance_"):
            a_name=cb.replace("join_alliance_","")
            if a_name not in adata["alliances"]: return await bot_instance.send_message(cid,"❌ اتحاد یافت نشد.")
            if adata["user_alliance"].get(uid): return await bot_instance.send_message(cid,"❌ شما قبلاً عضو یک اتحاد هستید!")
            if adata["traitor_until"].get(uid):
                try:
                    until=datetime.fromisoformat(adata["traitor_until"][uid])
                    if datetime.now()<until: return await bot_instance.send_message(cid,"⛔ به دلیل خیانت نمی‌توانید عضو شوید.")
                    else: del adata["traitor_until"][uid]
                except: pass
            if not any(i.get("owner")==uid for i in countries.values()): return await bot_instance.send_message(cid,"❌ برای پیوستن باید کشور داشته باشید!")
            if uid in adata["alliances"][a_name]["members"]: return await bot_instance.send_message(cid,"⚠️ شما قبلاً عضو این اتحاد هستید!")
            adata["alliances"][a_name]["members"].append(uid)
            adata["user_alliance"][uid]=a_name; save_alliance(adata)
            await bot_instance.send_message(cid,f"✅ شما به اتحاد {a_name} پیوستید!",chat_keypad=get_main_menu())
            try: await bot_instance.send_message(adata["alliances"][a_name]["leader"],f"👤 {username or uid} به اتحاد شما پیوست!")
            except: pass
            return
        if cb=="alliance_info":
            name,info=get_al(adata,uid)
            if not name: return await bot_instance.send_message(cid,"❌ شما عضو هیچ اتحادی نیستید!")
            leader_name=data["users"].get(info["leader"],{}).get("username","نامشخص")
            members="\n".join(f"{'👑' if m==info['leader'] else '👤'} {data['users'].get(m,{}).get('username',m[:10])} (`{m}`)" for m in info["members"])
            await bot_instance.send_message(cid,f"🔍 اتحاد {name}\nرهبر: {leader_name}\nاعضا ({len(info['members'])}):\n{members}"); return
        if cb=="alliance_chat":
            if not get_al(adata,uid)[0]: return await bot_instance.send_message(cid,"❌ عضو اتحاد نیستید!")
            user_states[cid]={"alliance_chat":True}
            await bot_instance.send_message(cid,"💬 پیام خود را برای اتحاد بفرستید:",chat_keypad=get_cancel()); return
        if cb=="alliance_leave":
            name,info=get_al(adata,uid)
            if not name: return await bot_instance.send_message(cid,"❌ عضو اتحاد نیستید!")
            if info["leader"]==uid: return await bot_instance.send_message(cid,"❌ رهبر نمی‌تواند خارج شود.")
            if uid in info["members"]: info["members"].remove(uid)
            if uid in adata["user_alliance"]: del adata["user_alliance"][uid]
            save_alliance(adata)
            await bot_instance.send_message(cid,f"🚪 شما از اتحاد {name} خارج شدید.",chat_keypad=get_main_menu()); return
        if cb=="alliance_betray":
            name,info=get_al(adata,uid)
            if not name: return await bot_instance.send_message(cid,"❌ عضو اتحاد نیستید!")
            if info["leader"]==uid: return await bot_instance.send_message(cid,"❌ رهبر نمی‌تواند خیانت کند!")
            user_coins=get_coins(data,uid); penalty=int(user_coins*0.5)
            remc(data,uid,penalty)
            ueq=totaleq(data,uid); removed=[]
            for _ in range(2):
                if not ueq: break
                eq=random.choice(list(ueq.keys())); amt=min(random.randint(1,3),ueq[eq])
                if amt>0:
                    ok,_=consume(data,uid,eq,amt)
                    if ok: removed.append(f"{eq} x{amt}")
                    ueq=totaleq(data,uid)
            save_data(data)
            if uid in info["members"]: info["members"].remove(uid)
            if uid in adata["user_alliance"]: del adata["user_alliance"][uid]
            adata["traitor_until"][uid]=(datetime.now()+timedelta(hours=24)).isoformat(); save_alliance(adata)
            traitor_name=data["users"][uid].get("username",uid[:10])
            for m in info["members"]:
                try: await bot_instance.send_message(m,f"💀 {traitor_name} به اتحاد خیانت کرد و جریمه شد!")
                except: pass
            await bot_instance.send_message(cid,f"💀 شما به اتحاد {name} خیانت کردید!\n🪙 جریمه: {fn(penalty)} کوین\n📦 تجهیزات از دست رفته: {', '.join(removed) if removed else 'هیچ'}\n⛔ تا ۲۴ ساعت نمی‌توانید عضو اتحاد شوید.",chat_keypad=get_main_menu()); return
        if cb=="alliance_manage":
            name,info=get_al(adata,uid)
            if not name or info["leader"]!=uid: return await bot_instance.send_message(cid,"❌ فقط رهبر می‌تواند مدیریت کند!")
            if len(info["members"])<=1: return await bot_instance.send_message(cid,"❌ هیچ عضوی برای مدیریت وجود ندارد.")
            builder=ChatKeypadBuilder()
            for m in info["members"]:
                if m!=uid: builder.row(builder.button(id=f"kick_{m}",text=f"❌ {data['users'].get(m,{}).get('username',m[:10])}"))
            builder.row(builder.button(id="back_to_menu",text="🏠 بازگشت"))
            await bot_instance.send_message(cid,"👥 اعضای اتحاد:",chat_keypad=builder.build(resize_keyboard=True,on_time_keyboard=True)); return
        if cb and cb.startswith("kick_"):
            target=cb.replace("kick_","")
            name,info=get_al(adata,uid)
            if not name or info["leader"]!=uid: return await bot_instance.send_message(cid,"❌ دسترسی غیرمجاز!")
            if target not in info["members"]: return await bot_instance.send_message(cid,"❌ کاربر در اتحاد نیست!")
            info["members"].remove(target)
            if target in adata["user_alliance"]: del adata["user_alliance"][target]
            save_alliance(adata)
            tname=data["users"].get(target,{}).get("username",target[:10])
            await bot_instance.send_message(cid,f"✅ {tname} از اتحاد اخراج شد.")
            try: await bot_instance.send_message(target,f"❌ شما از اتحاد {name} اخراج شدید.")
            except: pass
            return
        if cb=="alliance_disband":
            name,info=get_al(adata,uid)
            if not name or info["leader"]!=uid: return await bot_instance.send_message(cid,"❌ فقط رهبر می‌تواند منحل کند!")
            for m in info["members"]:
                if m in adata["user_alliance"]: del adata["user_alliance"][m]
            if name in adata["alliances"]: del adata["alliances"][name]
            save_alliance(adata)
            await bot_instance.send_message(cid,f"❌ اتحاد {name} منحل شد.",chat_keypad=get_main_menu())
            for m in info["members"]:
                try: await bot_instance.send_message(m,f"❌ اتحاد {name} توسط رهبر منحل شد.")
                except: pass
            return
        if cb=="attack":
            if not any(i.get("owner")==uid for i in countries.values()): return await bot_instance.send_message(cid,"❌ کشور ندارید!",chat_keypad=get_main_menu())
            await bot_instance.send_message(cid,"🎯 هدف:",chat_keypad=get_attack_countries_kb(countries,0)); return
        if cb and cb.startswith("attack_page_"):
            page=int(cb.replace("attack_page_",""))
            await bot_instance.send_message(cid,"🎯 هدف:",chat_keypad=get_attack_countries_kb(countries,page)); return
        if cb and cb.startswith("attack_"):
            target=cb.replace("attack_","")
            eq=data.get("user_eq",{}).get(uid,{}); packs=data.get("user_packs",{}).get(uid,[])
            await bot_instance.send_message(cid,"🔸 تجهیزات:",chat_keypad=get_attack_eq_kb(eq,packs,target)); return
        if cb and cb.startswith("eq_"):
            parts=cb.replace("eq_","").split("_",1)
            if len(parts)<2: return
            target,eq_name=parts[0],parts[1]
            if eq_name not in EQUIP: return await bot_instance.send_message(cid,"❌ تجهیزات نامعتبر!")
            max_cnt=totaleq(data,uid).get(eq_name,0)
            if max_cnt==0: return await bot_instance.send_message(cid,"❌ موجود نیست!")
            await bot_instance.send_message(cid,f"🎯 تعداد {eq_name}: {fn(max_cnt)}",chat_keypad=get_attack_amt_kb(target,eq_name,max_cnt)); return
        if cb and cb.startswith("amt_"):
            parts=cb.replace("amt_","").split("_")
            if len(parts)<3: return
            await do_attack(bot_instance,cid,data,countries,uid,parts[0],parts[1],int(parts[2])); return
        if cb and cb.startswith("custom_"):
            parts=cb.replace("custom_","").split("_",1)
            if len(parts)<2: return
            user_states[cid]={"wait_custom":True,"target":parts[0],"eq":parts[1]}
            await bot_instance.send_message(cid,f"✏️ تعداد {parts[1]}:",chat_keypad=get_cancel()); return
        if user_states.get(cid,{}).get("wait_custom"):
            try:
                amt=int(text)
                if amt<=0: return await bot_instance.send_message(cid,"❌ تعداد باید مثبت باشد.")
                target=user_states[cid]["target"]; eq_name=user_states[cid]["eq"]
                if eq_name not in EQUIP: return await bot_instance.send_message(cid,"❌ تجهیزات نامعتبر!")
                max_cnt=totaleq(data,uid).get(eq_name,0)
                if amt>max_cnt: return await bot_instance.send_message(cid,f"❌ حداکثر: {fn(max_cnt)}")
                await do_attack(bot_instance,cid,data,countries,uid,target,eq_name,amt)
                user_states[cid]={}
            except: await bot_instance.send_message(cid,"❌ عدد معتبر!")
            return
        if cb=="buy_country":
            await bot_instance.send_message(cid,"🌍 انتخاب کشور:",chat_keypad=get_countries_kb(countries,0)); return
        if cb and cb.startswith("countries_page_"):
            page=int(cb.replace("countries_page_",""))
            await bot_instance.send_message(cid,"🌍 انتخاب کشور:",chat_keypad=get_countries_kb(countries,page)); return
        if cb and cb.startswith("country_"):
            code=cb.replace("country_","")
            info=countries.get(code)
            if not info or info.get("owner"): return await bot_instance.send_message(cid,"❌ نامعتبر!")
            if any(i.get("owner")==uid for i in countries.values()): return await bot_instance.send_message(cid,"❌ قبلاً کشور دارید!")
            addc(data,uid,1000)
            countries[code]["owner"]=uid; data["users"][uid]["has_country"]=True
            save_data(data); save_countries(countries)
            await bot_instance.send_message(cid,f"🎉 کشور {info['flag']} {info['name']} تصرف شد!\n🪙 ۱,۰۰۰ کوین",chat_keypad=get_main_menu()); return
        if cb=="buy_single":
            await bot_instance.send_message(cid,"🎯 تجهیزات:",chat_keypad=get_single_eq_kb()); return
        if cb and cb.startswith("buyeq_"):
            eq_name=cb.replace("buyeq_","")
            if eq_name not in EQUIP: return await bot_instance.send_message(cid,"❌ نامعتبر!")
            price=EQUIP[eq_name][0]; user_coins=get_coins(data,uid)
            if user_coins<price: return await bot_instance.send_message(cid,f"❌ کوین کافی نیست! ({fn(price)})")
            data["users"][uid]["coins"]=user_coins-price; addeq(data,uid,eq_name,1); save_data(data)
            await bot_instance.send_message(cid,f"✅ {eq_name} خریداری شد!",chat_keypad=get_single_eq_kb()); return
        if cb=="equipment_shop":
            await bot_instance.send_message(cid,"🛒 فروشگاه پک‌ها",chat_keypad=get_shop_menu()); return
        for pn in PACKS:
            if cb==f"shop_{pn}":
                await bot_instance.send_message(cid,f"📦 {pn}\n💰 {fn(PACKS[pn][0])} تومان\n🔴 مبالغ پرداخت‌شده برای پک و خریدها پس داده نمی‌شود.\nبرای خرید به {ADMIN_USERNAME} پیام دهید."); return
        if cb=="send_message":
            if not any(i.get("owner")==uid for i in countries.values()): return await bot_instance.send_message(cid,"❌ کشور ندارید!")
            user_states[cid]={"wait_msg":True}
            await bot_instance.send_message(cid,"📨 بیانیه:",chat_keypad=get_cancel()); return
        if user_states.get(cid,{}).get("wait_msg"):
            my_country=next((i for i in countries.values() if i.get("owner")==uid),None)
            if my_country:
                today=date.today().isoformat()
                data["users"][uid].setdefault("daily_statements",{})
                cnt=data["users"][uid]["daily_statements"].get(today,0)
                if cnt>=30: return await bot_instance.send_message(cid,"❌ محدودیت ۳۰ بیانیه!")
                data["users"][uid]["daily_statements"][today]=cnt+1
                addc(data,uid,50); save_data(data)
                full_id=gid(msg,uid)
                framed=mf(text,title=f"{my_country['flag']} {my_country['name']}",icon="📨")
                final=f"{framed}\n\n👤 {full_id}\n🪙 +۵۰ کوین"
                count=0
                for u2 in data["users"]:
                    if u2!=uid:
                        try: await bot_instance.send_message(u2,final); count+=1
                        except: pass
                await bot_instance.send_message(cid,f"✅ بیانیه به {count} نفر ارسال شد!",chat_keypad=get_main_menu())
            user_states[cid]={}; return
        if cb=="top_owners":
            un=load_un(); tops=[]
            for c,i in countries.items():
                if i.get("owner"):
                    own=i["owner"]; pwr=power(data,own)
                    is_leader=(own==un.get("leader")); own_name="🤖 ربات" if own=="BOT_AI" else data["users"].get(own,{}).get("username",own[:15])
                    tops.append({"flag":i["flag"],"name":i["name"],"power":pwr+(10000 if is_leader else 0),"damage":i.get("damage_taken",0),"owner":own_name,"uid":own,"is_leader":is_leader})
            tops.sort(key=lambda x:x["power"],reverse=True)
            txt="🏆 رتبه‌بندی:\n\n"; medals=["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            for idx,t in enumerate(tops[:10]):
                dmg=f" | 💥 {fn(t['damage'])}" if t["damage"]>0 else ""
                txt+=f"{medals[idx]} {t['flag']} {t['name']} | 👤 {t['owner']} | 🆔 `{t['uid']}` | ⚔️ {fn(t['power'])}{dmg}\n"
            await bot_instance.send_message(cid,txt); return
        if cb=="un_menu": await bot_instance.send_message(cid,"🌐 سازمان ملل:",chat_keypad=get_un_menu()); return
        if cb=="un_info":
            un=load_un()
            await bot_instance.send_message(cid,f"🏛 سازمان ملل\n👥 اعضا: {len(un.get('members',[]))}"); return
        if cb=="un_join":
            un=load_un()
            if uid in un.get("members",[]): return await bot_instance.send_message(cid,"✅ عضو هستید!")
            if any(req["uid"]==uid and req.get("status")=="pending" for req in un.get("requests",[])):
                return await bot_instance.send_message(cid,"⏳ درخواست قبلی در حال بررسی است!")
            if not any(i.get("owner")==uid for i in countries.values()): return await bot_instance.send_message(cid,"❌ کشور ندارید!")
            un["requests"].append({"uid":uid,"status":"pending","time":datetime.now().isoformat()}); save_un(un)
            await bot_instance.send_message(cid,"✅ درخواست ثبت شد!"); return
        if cb=="faction_menu": await bot_instance.send_message(cid,"⚔️ گروهک‌ها:",chat_keypad=get_faction_menu()); return
        if cb and cb.startswith("faction_"):
            faction_key=cb.replace("faction_","")
            if faction_key in FACTIONS:
                f=FACTIONS[faction_key]
                if data["users"][uid].get("faction"): return await bot_instance.send_message(cid,"❌ قبلاً عضو هستید!")
                data["users"][uid]["faction"]=faction_key
                for w in f["w"]: addeq(data,uid,w,50)
                addc(data,uid,3000); save_data(data)
                await bot_instance.send_message(cid,f"✅ به {f['name']} پیوستید!",chat_keypad=get_main_menu()); return
    except Exception as e:
        logger.error(f"Unhandled error in handler: {e}\n{traceback.format_exc()}")
        try:
            await bot_instance.send_message(cid, "❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.")
        except:
            pass

async def main():
    while True:
        try:
            logger.info("ربات در حال اجرا...")
            await bot.run()
        except asyncio.CancelledError:
            logger.info("ربات به صورت دستی متوقف شد.")
            break
        except Exception as e:
            logger.error(f"ربات با خطا متوقف شد: {e}\n{traceback.format_exc()}")
            logger.info("تلاش برای راه‌اندازی مجدد در ۵ ثانیه...")
            await asyncio.sleep(5)

if __name__=="__main__":
    os_system('cls' if os_name=='nt' else 'clear')
    load_data(); load_countries(); load_un(); load_alliance(); load_bot_status()
    print("🚀 ربات جنگ جهانی با ۱۵۰ کشور در حال اجراست...\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 ربات متوقف شد")
