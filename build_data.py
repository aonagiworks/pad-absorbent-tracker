#!/usr/bin/env python3
# stdlib only
import json, hashlib, urllib.request, urllib.error, xml.etree.ElementTree as ET, gzip, re
from datetime import datetime, timezone

# CURATED: pad absorbent daging (soaker pad / drip pad) — market mapping Indonesia + global
CURATED = [
    # === MARKET LEADER ===
    {"title":"Sealed Air Cryovac Dri-Loc","provider":"Sealed Air (USA)","category":"Market Leader","type":"Standard PE + SAP","absorb":"700-1000ml/m²","price":"Rp 180-350 /pcs","url":"https://www.sealedair.com/products/food-packaging/absorbent-pads","desc":"Market leader global. Dri-Loc paling dipakai retail daging sapi/ayam. SAP ultra, PE perforated, food-grade FDA/EU. Kapasitas tertinggi, distribusi worldwide termasuk Indonesia via distributor.","tags":["leader","SAP","PE","ayam","sapi"]},
    {"title":"Novipax SuperAbsorb","provider":"Novipax (USA)","category":"Market Leader","type":"Airlaid + SAP","absorb":"800-1200ml/m²","price":"Rp 200-400 /pcs","url":"https://www.novipax.com/products/meat-poultry-pads","desc":"Leader USA, supply Walmart/Costco. Airlaid + SAP, anti-leak seal, varian black pad untuk daging merah. Kapasitas jumbo untuk tray besar.","tags":["leader","airlaid","SAP","sapi"]},
    {"title":"Sirane Dri-Fresh Fresh-Hold","provider":"Sirane (UK)","category":"Market Leader","type":"Cellulose + SAP","absorb":"600-900ml/m²","price":"Rp 170-320 /pcs","url":"https://www.sirane.com/food-packaging/absorbent-pads/","desc":"Leader Eropa. Dri-Fresh range lengkap: standard, super, absorbent + anti-fog. Sertifikasi BRC, supply Tesco/M&S. Ada versi compostable.","tags":["leader","cellulose","fresh-hold"]},
    {"title":"McAirlaid's OptiDri","provider":"McAirlaid's (Germany)","category":"Market Leader","type":"Airlaid Dry-Means","absorb":"750-1100ml/m²","price":"Rp 190-380 /pcs","url":"https://www.mcairlaids.com/food-pads","desc":"Jerman, teknologi airlaid non-woven proprietary. Dry-Means tidak pakai fluff pulp — lebih tipis tapi serap tinggi. OEKO-TEX, supply Lidl/Aldi.","tags":["leader","airlaid","jerman"]},
    {"title":"Elliott Absorbents Meat Pad","provider":"Elliott Absorbents (UK)","category":"Market Leader","type":"Cellulose + PE","absorb":"500-800ml/m²","price":"Rp 150-300 /pcs","url":"https://www.elliottabsorbents.co.uk/food-absorbent-pads","desc":"UK leader, 40+ tahun. Range paling luas: mini 60x80mm sampai jumbo 200x300mm. PE backing anti-bocor, food contact approved.","tags":["leader","cellulose","UK"]},
    {"title":"PaperPak Absorbent Pads","provider":"PaperPak (Canada)","category":"Market Leader","type":"Recycled Cellulose + SAP","absorb":"600-950ml/m²","price":"Rp 160-310 /pcs","url":"https://www.paperpak.ca/food-pads","desc":"Leader Kanada, fokus sustainable. 100% recycled cellulose + SAP food-grade. Supply Sobeys, Costco Canada. Harga kompetitif untuk volume besar.","tags":["leader","recycled","kanada"]},

    # === MARKET CHALLENGER ===
    {"title":"Cellcomb Absorber Pad","provider":"Cellcomb (Sweden)","category":"Market Challenger","type":"Cellulose + SAP","absorb":"550-850ml/m²","price":"Rp 140-280 /pcs","url":"https://www.cellcomb.com/absorbent-pads","desc":"Challenger Skandinavia. Serang leader dengan harga 15-20% lebih murah, kualitas setara. Supply ICA, Coop. Varian anti-bakteri.","tags":["challenger","sweden","antibakteri"]},
    {"title":"Coating Excellence Thermasorb","provider":"Coating Excellence (USA)","category":"Market Challenger","type":"PE Coated + SAP","absorb":"650-900ml/m²","price":"Rp 150-290 /pcs","url":"https://www.thermasorb.com","desc":"Challenger USA. Thermasorb dengan heat-seal edge — tidak bocor samping. Target ambil share Novipax di midwest USA.","tags":["challenger","heat-seal","USA"]},
    {"title":"De Cymbal Absorbent Soaker","provider":"De Cymbal (UK)","category":"Market Challenger","type":"Fluff + SAP + PE","absorb":"500-750ml/m²","price":"Rp 130-260 /pcs","url":"https://www.decymbal.co.uk/soaker-pads","desc":"Challenger UK harga fighter. Fluff pulp + SAP, PE backing. Fokus pasar wholesale & butcher lokal, MOQ rendah.","tags":["challenger","fluff","wholesale"]},
    {"title":"Mascarello Soaker Pad","provider":"Mascarello (Italy)","category":"Market Challenger","type":"Cellulose + SAP","absorb":"550-800ml/m²","price":"Rp 145-275 /pcs","url":"https://www.mascarello.it/pad-assorbenti","desc":"Challenger Italia. Desain tipis untuk packaging premium (prosciutto, bresaola). Supply pasar Mediterania, ekspansi ke Asia.","tags":["challenger","italy","premium"]},
    {"title":"Qingdao Ideal Goal Pad","provider":"Ideal Goal (China)","category":"Market Challenger","type":"SAP + Nonwoven + PE","absorb":"600-950ml/m²","price":"Rp 90-180 /pcs","url":"https://www.idealgoal.cn/meat-pad","desc":"Challenger China terbesar. Harga 40-50% di bawah leader, kapasitas setara. Supply OEM untuk brand Eropa. MOQ 50k pcs, lead time 20 hari.","tags":["challenger","china","OEM","murah"]},
    {"title":"Zhongshan Qidong Soaker","provider":"Zhongshan Qidong (China)","category":"Market Challenger","type":"SAP Composite","absorb":"550-900ml/m²","price":"Rp 85-170 /pcs","url":"https://www.qidongpack.com/absorbent-pad","desc":"Challenger China, spesialis export. Varian warna hitam/putih, ukuran custom. Sudah masuk pasar Indonesia via importir Jakarta.","tags":["challenger","china","custom"]},

    # === MARKET FOLLOWER ===
    {"title":"Dewi Pack Soaker Lokal","provider":"PT Dewi Pack (Indonesia)","category":"Market Follower","type":"Tissue + SAP + PE","absorb":"400-600ml/m²","price":"Rp 75-140 /pcs","url":"https://shopee.co.id/search?keyword=pad%20absorbent%20daging","desc":"Follower lokal Indonesia. Produksi Bandung/Surabaya, tissue + SAP impor, PE lokal. Harga murah, kualitas menengah. Jual via Shopee/Tokopedia, MOQ 1k pcs.","tags":["follower","lokal","indonesia","shopee"]},
    {"title":"Indo Absorb Standard","provider":"PT Indo Absorb (Indonesia)","category":"Market Follower","type":"Cellulose + PE","absorb":"350-550ml/m²","price":"Rp 60-120 /pcs","url":"https://www.tokopedia.com/search?st=product&q=soaker%20pad%20daging","desc":"Follower lokal, tanpa SAP (hanya cellulose). Daya serap rendah, cocok untuk ayam potong & ikan segar. Harga paling murah, target pasar tradisional.","tags":["follower","lokal","tanpa-SAP","murah"]},
    {"title":"Bulteau Soaker Basic","provider":"Bulteau Systems (France)","category":"Market Follower","type":"Cellulose + PE","absorb":"400-650ml/m²","price":"Rp 110-210 /pcs","url":"https://www.bulteau-systems.com/pads","desc":"Follower Prancis. Ikut spec leader tapi tanpa inovasi. Harga mid, supply pasar lokal Perancis & export kecil.","tags":["follower","france","basic"]},
    {"title":"Tristar Packaging Pad","provider":"Tristar Packaging (India)","category":"Market Follower","type":"Fluff + PE","absorb":"350-600ml/m²","price":"Rp 70-130 /pcs","url":"https://www.tristarpackaging.in/soaker-pads","desc":"Follower India. Fluff pulp lokal, PE impor. Fokus pasar domestik India & export ke Timur Tengah. Harga low-end.","tags":["follower","india","fluff"]},
    {"title":"Viet Pack Absorbent","provider":"Viet Pack (Vietnam)","category":"Market Follower","type":"Nonwoven + SAP","absorb":"450-700ml/m²","price":"Rp 80-150 /pcs","url":"https://vietpack.vn/absorbent-pad","desc":"Follower Vietnam. Copy desain China, harga sedikit lebih tinggi tapi kualitas kontrol lebih baik. Supply pasar ASEAN.","tags":["follower","vietnam","ASEAN"]},
    {"title":"Generic Alibaba Soaker 100pcs","provider":"Generic / Alibaba Import","category":"Market Follower","type":"Mixed","absorb":"300-600ml/m²","price":"Rp 50-100 /pcs","url":"https://www.alibaba.com/showroom/meat-absorbent-pad.html","desc":"Follower generic Alibaba. Banyak seller, kualitas bervariasi. Risiko: tidak semua food-grade certified. Wajib minta COA & migration test sebelum bulk.","tags":["follower","alibaba","generic","risiko"]},

    # === MARKET NICHER ===
    {"title":"Sirane Earth Packaging Compostable","provider":"Sirane (UK) - Earth Line","category":"Market Nicher","type":"Compostable Cellulose","absorb":"400-650ml/m²","price":"Rp 220-420 /pcs","url":"https://www.sirane.com/earth-packaging/","desc":"Nicher eco. 100% compostable, plastic-free, EN13432 certified. Target premium organic meat, zero-waste retailer. Harga 30-40% premium.","tags":["nicher","compostable","eco","premium"]},
    {"title":"Sealed Air rDri-Loc Recycle-Ready","provider":"Sealed Air - rDriLoc","category":"Market Nicher","type":"Recyclable PE + SAP","absorb":"600-850ml/m²","price":"Rp 200-380 /pcs","url":"https://www.sealedair.com/products/food-packaging/recycle-ready-pads","desc":"Nicher sustainable. Recycle-ready pad, bisa masuk stream PE recycling. Jawab demand retailer ESG (Aldi, Carrefour).","tags":["nicher","recyclable","ESG"]},
    {"title":"Cryovac Active CO2 Emitter Pad","provider":"Sealed Air - Active","category":"Market Nicher","type":"Active Pad CO2 + Absorb","absorb":"500-750ml/m²","price":"Rp 280-500 /pcs","url":"https://www.sealedair.com/products/active-packaging","desc":"Nicher active packaging. Pad + CO2 emitter extend shelf life 2-3 hari. Untuk daging premium export, seafood. Butuh cold chain ketat.","tags":["nicher","active","CO2","seafood"]},
    {"title":"Sirane Dri-Fresh ABV Antimicrobial","provider":"Sirane - ABV","category":"Market Nicher","type":"Antimicrobial Cellulose","absorb":"500-700ml/m²","price":"Rp 250-450 /pcs","url":"https://www.sirane.com/dri-fresh-abv/","desc":"Nicher antimicrobial. Infused active agent hambat bakteri, kurangi bau drip. Untuk ayam & ikan yang cepat busuk. BRC + EFSA approved.","tags":["nicher","antimicrobial","ayam","ikan"]},
    {"title":"PaperPak Ultra Green Bio","provider":"PaperPak - Green Line","category":"Market Nicher","type":"Bio SAP + Kraft","absorb":"450-700ml/m²","price":"Rp 210-400 /pcs","url":"https://www.paperpak.ca/green-pads","desc":"Nicher bio. SAP dari pati tanaman (bukan akrilik), kraft paper unbleached. Target pasar organic/natural meat USA & EU.","tags":["nicher","bio-SAP","organic"]},
    {"title":"TOMI Odor-Capture Pad","provider":"TOMI (Japan)","category":"Market Nicher","type":"Charcoal + SAP","absorb":"400-600ml/m²","price":"Rp 260-480 /pcs","url":"https://www.tomi-jp.com/odor-pad","desc":"Nicher Jepang. Pad + activated charcoal serap bau amis. Untuk ikan sashimi-grade & daging wagyu. Pasar premium Jepang/Korea.","tags":["nicher","charcoal","japan","ikan","wagyu"]},
    {"title":"McAirlaid's Black Pad Premium","provider":"McAirlaid's - Black","category":"Market Nicher","type":"Black Airlaid + SAP","absorb":"600-850ml/m²","price":"Rp 190-350 /pcs","url":"https://www.mcairlaids.com/black-pads","desc":"Nicher visual. Pad hitam untuk daging merah — drip tidak terlihat, display lebih menarik. Dipakai premium butcher & steakhouse.","tags":["nicher","black-pad","display","steak"]},
    {"title":"Cellcomb Freshness Indicator","provider":"Cellcomb - Indicator","category":"Market Nicher","type":"Smart Pad + Indicator","absorb":"500-700ml/m²","price":"Rp 350-600 /pcs","url":"https://www.cellcomb.com/smart-pads","desc":"Nicher smart. Pad + indikator warna pH: berubah jika daging mulai rusak. Untuk supply chain farm-to-retail, kurangi food waste.","tags":["nicher","smart","indicator","IoT"]},
]

FEEDS = [
    "https://www.packagingdigest.com/rss.xml",
    "https://www.foodpackagingforum.org/news/rss.xml",
    "https://feeds.feedburner.com/ThePackagingPortal",
    "https://www.meatpoultry.com/rss",
    "https://feeds.feedburner.com/TechCrunch",
    "https://www.packworld.com/rss.xml",
]

KEYWORDS = ["absorbent","pad","packaging","meat","poultry","seafood","food packaging","soaker","drip","tray","shelf life","MAP","vacuum","protein","butcher","retail","fresh","SAP","airlaid","cellulose","compostable"]

def fetch_feed(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Accept":"*/*"})
        resp = urllib.request.urlopen(req, timeout=20)
        data = resp.read()
        if resp.headers.get('Content-Encoding')=='gzip':
            data = gzip.decompress(data)
        return data
    except Exception as e:
        print(f"feed err {url}: {e}")
        return None

def parse_feed(data):
    items=[]
    try:
        root = ET.fromstring(data)
    except: return items
    # RSS
    for it in root.findall('.//item'):
        t = it.find('title')
        l = it.find('link')
        d = it.find('description')
        title = t.text.strip() if t is not None and t.text else ""
        link = l.text.strip() if l is not None and l.text else ""
        desc = d.text.strip() if d is not None and d.text else ""
        if title and link: items.append((title,link,desc))
    # Atom
    ns={'a':'http://www.w3.org/2005/Atom'}
    for e in root.findall('.//a:entry', ns):
        t = e.find('a:title', ns)
        title = t.text.strip() if t is not None and t.text else ""
        link_el = e.find('a:link', ns)
        link = link_el.get('href','') if link_el is not None else ""
        if not link:
            link_el2 = e.find('a:id', ns)
            link = link_el2.text.strip() if link_el2 is not None and link_el2.text else ""
        d = e.find('a:summary', ns)
        if d is None: d = e.find('a:content', ns)
        desc = d.text.strip() if d is not None and d.text else ""
        if title and link: items.append((title,link,desc))
    return items

def relevant(title):
    tl = title.lower()
    if len(title) < 12: return False
    return any(k.lower() in tl for k in KEYWORDS)

def build():
    out_items=[]
    seen=set()
    seen_titles=set()
    curated_n=0
    for c in CURATED:
        url=c["url"]
        cid=hashlib.md5(url.encode()).hexdigest()[:12]
        item={
            "id":cid,
            "title":c["title"],
            "provider":c["provider"],
            "category":c["category"],
            "type":c["type"],
            "absorb":c["absorb"],
            "price":c["price"],
            "url":c["url"],
            "desc":c["desc"],
            "tags":c.get("tags",[]),
            "source":"curated",
        }
        out_items.append(item)
        seen.add(url)
        seen_titles.add(c["title"].lower())
        curated_n+=1

    from_feeds=[]
    for f in FEEDS:
        data=fetch_feed(f)
        if not data: continue
        for title,link,desc in parse_feed(data):
            if link in seen: continue
            if title.lower() in seen_titles: continue
            if not relevant(title): continue
            seen.add(link)
            seen_titles.add(title.lower())
            fid=hashlib.md5(link.encode()).hexdigest()[:12]
            from_feeds.append({
                "id":fid,
                "title":title,
                "provider":"Industry News",
                "category":"News/Update",
                "type":"Artikel",
                "absorb":"—",
                "price":"—",
                "url":link,
                "desc": (desc[:180]+"..." if len(desc)>180 else desc) or title,
                "tags":["news"],
                "source":"feed"
            })
            if len(from_feeds)>=20: break
        if len(from_feeds)>=20: break

    all_items=out_items+from_feeds
    # sort: curated first, then feeds
    now=datetime.now(timezone.utc).isoformat()
    out={
        "updated_at":now,
        "total":len(all_items),
        "curated":curated_n,
        "from_feeds":len(from_feeds),
        "offers":all_items,
        "courses":all_items
    }
    # asserts
    assert out["total"] >= len(CURATED), "curated missing"
    assert all("id" in x and "url" in x for x in all_items), "schema broken"
    assert len(set(x["id"] for x in all_items))==len(all_items), "duplicate id"
    REQ=("title","provider","category","url","desc")
    bad=[x["title"] for x in all_items if x["source"]=="curated" and not all(x.get(k) for k in REQ)]
    assert not bad, f"curated entries missing fields: {bad[:5]}"
    return out

if __name__=="__main__":
    out=build()
    with open("data.json","w",encoding="utf-8") as f:
        json.dump(out,f,ensure_ascii=False,indent=2)
    print(f"built data.json: total={out['total']} curated={out['curated']} feeds={out['from_feeds']}")
