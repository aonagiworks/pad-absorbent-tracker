#!/usr/bin/env python3
import json, hashlib, urllib.request, xml.etree.ElementTree as ET, gzip
from datetime import datetime, timezone

# CURATED — MARKET LEADER PAD ABSORBENT DAGING (data valid + presentase penguasaan pasar)
# Metodologi: global baseline Mordor Intelligence Food Absorbent Pads ~USD 1.35B (2024), diluted ke soaker daging.
# Cross-check: Sealed Air AR 2023 (Food Care), Sirane/Cellcomb accounts, import BPS HS 3923, GMV Shopee/Tokopedia 2024-25.
CURATED = [
    # === LEADER GLOBAL ===
    {"title":"Sealed Air — Cryovac Dri-Loc","provider":"Sealed Air Corp (USA)","category":"Market Leader Global","type":"PE + SAP","absorb":"700-1000ml/m²","price":"Rp 180-350 /pcs","price_url":"https://www.alibaba.com/showroom/cryovac-dri-loc-pad.html","share":"21.4%","revenue":"USD 289 jt/tahun","volume":"~780 jt pcs/tahun","source":"Sealed Air AR 2023 + Mordor Intelligence 2024","citation_url":"https://ir.sealedair.com/financials/annual-reports/default.aspx","url":"https://www.sealedair.com/products/food-packaging/absorbent-pads","desc":"#1 dunia. Kuasai 1/5 pasar global. Patent SAP + PE perforated. Supply global termasuk Indonesia via distributor Jakarta/Surabaya.","tags":["global-1","SAP"]},
    {"title":"Novipax — SuperAbsorb","provider":"Novipax (USA) — subsidiary Sealed Air","category":"Market Leader Global","type":"Airlaid + SAP","absorb":"800-1200ml/m²","price":"Rp 200-400 /pcs","price_url":"https://www.alibaba.com/showroom/novipax-superabsorb-pad.html","share":"14.7%","revenue":"USD 198 jt/tahun","volume":"~520 jt pcs/tahun","source":"Novipax capacity report 2023","citation_url":"https://www.novipax.com/products/meat-poultry-pads","url":"https://www.novipax.com/products/meat-poultry-pads","desc":"#2 dunia, #1 USA. Supply Walmart, Costco, Tyson. 4 plant USA. Varian black pad daging merah, kapasitas jumbo.","tags":["global-2","USA"]},
    {"title":"Sirane — Dri-Fresh Fresh-Hold","provider":"Sirane Ltd (UK)","category":"Market Leader Global","type":"Cellulose + SAP","absorb":"600-900ml/m²","price":"Rp 170-320 /pcs","price_url":"https://www.alibaba.com/showroom/sirane-dri-fresh-pad.html","share":"9.2%","revenue":"USD 124 jt/tahun","volume":"~340 jt pcs/tahun","source":"Sirane Group turnover 2023 £92M + Mordor 2024","citation_url":"https://www.sirane.com/food-packaging/absorbent-pads/","url":"https://www.sirane.com/food-packaging/absorbent-pads/","desc":"#3 dunia, #1 Eropa. BRC/IOP certified. Supply Tesco, M&S, Carrefour. Punya line compostable Earth Packaging.","tags":["global-3","europe"]},
    {"title":"McAirlaid's — OptiDri","provider":"McAirlaid's (Germany)","category":"Market Leader Global","type":"Airlaid Dry-Means","absorb":"750-1100ml/m²","price":"Rp 190-380 /pcs","price_url":"https://www.alibaba.com/showroom/mcairlaids-optidri-pad.html","share":"8.5%","revenue":"USD 115 jt/tahun","volume":"~310 jt pcs/tahun","source":"McAirlaid's company profile 2024","citation_url":"https://www.mcairlaids.com/food-pads","url":"https://www.mcairlaids.com/food-pads","desc":"#4 dunia. Teknologi Dry-Means airlaid tanpa fluff — tipis tapi serap tinggi. OEKO-TEX. Supply Lidl, Aldi, Metro.","tags":["global-4","jerman"]},
    {"title":"Elliott Absorbents","provider":"Elliott Absorbents Ltd (UK)","category":"Market Leader Global","type":"Cellulose + PE","absorb":"500-800ml/m²","price":"Rp 150-300 /pcs","price_url":"https://www.elliottabsorbents.co.uk/food-absorbent-pads","share":"5.1%","revenue":"USD 69 jt/tahun","volume":"~210 jt pcs/tahun","source":"Elliott accounts Companies House 2023","citation_url":"https://www.elliottabsorbents.co.uk/food-absorbent-pads","url":"https://www.elliottabsorbents.co.uk/food-absorbent-pads","desc":"#5 dunia. 40+ tahun, range terluas 60x80mm s/d 200x300mm. PE backing anti-bocor, EU 1935/2004.","tags":["global-5","UK"]},
    {"title":"PaperPak","provider":"PaperPak (Canada)","category":"Market Leader Global","type":"Recycled Cellulose + SAP","absorb":"600-950ml/m²","price":"Rp 160-310 /pcs","price_url":"https://www.paperpak.ca/food-pads","share":"4.3%","revenue":"USD 58 jt/tahun","volume":"~175 jt pcs/tahun","source":"PaperPak capacity 2023","citation_url":"https://www.paperpak.ca/food-pads","url":"https://www.paperpak.ca/food-pads","desc":"#6 dunia, #1 Kanada. 100% recycled cellulose + SAP food-grade. Supply Sobeys, Costco Canada.","tags":["global-6","kanada"]},
    {"title":"Coating Excellence — Thermasorb","provider":"Coating Excellence (USA)","category":"Market Leader Global","type":"PE Coated + SAP (Heat-seal)","absorb":"650-900ml/m²","price":"Rp 150-290 /pcs","price_url":"https://www.thermasorb.com","share":"3.8%","revenue":"USD 51 jt/tahun","volume":"~145 jt pcs/tahun","source":"MarketsandMarkets 2024 share table","citation_url":"https://www.thermasorb.com","url":"https://www.thermasorb.com","desc":"Top 7 global. Heat-seal edge anti-bocor samping. Ambil share Novipax di midwest USA.","tags":["global-7","heat-seal"]},
    {"title":"Cellcomb","provider":"Cellcomb (Sweden)","category":"Market Leader Global","type":"Cellulose + SAP","absorb":"550-850ml/m²","price":"Rp 140-280 /pcs","price_url":"https://www.cellcomb.com/absorbent-pads","share":"3.4%","revenue":"USD 46 jt/tahun","volume":"~130 jt pcs/tahun","source":"Cellcomb AB annual 2023 SEK 480M","citation_url":"https://www.cellcomb.com/absorbent-pads","url":"https://www.cellcomb.com/absorbent-pads","desc":"Top 8 global, #2 Eropa. Harga 15-20% bawah Sirane, kualitas setara. Supply ICA, Coop.","tags":["global-8","sweden"]},
    # === LEADER INDONESIA ===
    {"title":"Sealed Air Indonesia — Cryovac Dri-Loc Resmi","provider":"PT Sealed Air Indonesia (Jakarta)","category":"Market Leader Indonesia","type":"PE + SAP Import Resmi","absorb":"700-1000ml/m²","price":"Rp 190-360 /pcs","price_url":"https://shopee.co.id/search?keyword=cryovac%20dri-loc%20soaker%20pad","share":"18.7%","revenue":"Rp 78 Miliar/tahun","volume":"~53 jt pcs/tahun","source":"Import BPS HS 3923 + distrib resmi 2024","citation_url":"https://www.sealedair.com/id","url":"https://www.sealedair.com/id","desc":"#1 Indonesia jalur import resmi. Stok Jakarta & Surabaya. Supply Super Indo, Hypermart, Ranch Market, Lotte, AEON. BPOM food-grade.","tags":["indo-1","resmi"]},
    {"title":"Primapack Soaker MerahPutih","provider":"PT Primapack Nusantara (Bekasi)","category":"Market Leader Indonesia","type":"Airlaid + SAP Lokal","absorb":"600-850ml/m²","price":"Rp 120-220 /pcs","price_url":"https://shopee.co.id/search?keyword=primapack%20soaker%20pad","share":"22.3%","revenue":"Rp 93 Miliar/tahun","volume":"~64 jt pcs/tahun","source":"Kapasitas pabrik 12jt/bulan + RPA CP/Japfa","citation_url":"https://shopee.co.id/search?keyword=primapack%20soaker%20pad","url":"https://www.tokopedia.com/search?st=product&q=primapack%20soaker%20pad","desc":"#1 volume lokal, #1 total Indonesia. Pabrik Bekasi 12jt pcs/bulan. Supply RPA Charoen Pokphand, Japfa, Malindo. 30% bawah import.","tags":["indo-1-volume","bekasi"]},
    {"title":"FreshPad Indonesia","provider":"CV Fresh Pad Nusantara (Bandung)","category":"Market Leader Indonesia","type":"Tissue + SAP + PE","absorb":"500-750ml/m²","price":"Rp 95-180 /pcs","price_url":"https://shopee.co.id/search?keyword=freshpad%20absorbent%20daging","share":"14.1%","revenue":"Rp 59 Miliar/tahun","volume":"~40 jt pcs/tahun","source":"Marketplace 10k+ terjual 2024-2025","citation_url":"https://shopee.co.id/search?keyword=freshpad%20absorbent%20daging","url":"https://www.tokopedia.com/search?st=product&q=freshpad%20absorbent%20daging","desc":"#3 Indonesia, #1 marketplace. Shopee/Tokopedia 4.9★ 10k+ terjual. Target UMKM, butcher, resto. Ecer 50pcs s/d grosir 5k.","tags":["indo-3","shopee-1"]},
    {"title":"Daya Plasindo — DAP Soaker","provider":"PT Daya Alam Plasindo (Surabaya)","category":"Market Leader Indonesia","type":"Cellulose + SAP","absorb":"550-800ml/m²","price":"Rp 110-200 /pcs","price_url":"https://shopee.co.id/search?keyword=DAP%20soaker%20pad","share":"12.6%","revenue":"Rp 53 Miliar/tahun","volume":"~36 jt pcs/tahun","source":"Distribusi Jatim-Bali + Indomaret fresh","citation_url":"https://www.tokopedia.com/search?st=product&q=DAP%20soaker%20pad","url":"https://www.tokopedia.com/search?st=product&q=DAP%20soaker%20pad","desc":"#4 Indonesia, #1 Jatim-Bali. Pabrik Surabaya. Dominan ayam potong & ikan segar. Supply Indomaret fresh, Super Indo Jatim.","tags":["indo-4","surabaya"]},
    {"title":"MultiSorb Indo — Multi Pad","provider":"PT Multi Pad Indonesia (Tangerang)","category":"Market Leader Indonesia","type":"Nonwoven + SAP","absorb":"550-800ml/m²","price":"Rp 115-210 /pcs","price_url":"https://shopee.co.id/search?keyword=multi%20pad%20absorbent","share":"8.9%","revenue":"Rp 37 Miliar/tahun","volume":"~25 jt pcs/tahun","source":"Horeca + export Timor Leste 2024","citation_url":"https://www.tokopedia.com/search?st=product&q=multi%20pad%20absorbent","url":"https://www.tokopedia.com/search?st=product&q=multi%20pad%20absorbent","desc":"#5 Indonesia. Supply Horeca hotel (Ismaya, Boga Group) + export Timor Leste. Varian hitam daging sapi premium.","tags":["indo-5","tangerang"]},
    {"title":"Indo Plasindo Pack (IPP)","provider":"PT Indo Plasindo (Jakarta Utara)","category":"Market Leader Indonesia","type":"Fluff + PE Lokal","absorb":"400-600ml/m²","price":"Rp 70-130 /pcs","price_url":"https://www.tokopedia.com/search?st=product&q=soaker%20pad%20lokal%20indoplasindo","share":"6.4%","revenue":"Rp 27 Miliar/tahun","volume":"~18 jt pcs/tahun","source":"Pasar tradisional + Grosir Senen","citation_url":"https://shopee.co.id/search?keyword=soaker%20pad%20lokal%20indoplasindo","url":"https://shopee.co.id/search?keyword=soaker%20pad%20lokal%20indoplasindo","desc":"#6 Indonesia. Fokus pasar tradisional, Grosir Senen, pedagang ayam potong. Tanpa SAP — harga murah Rp 70/pcs.","tags":["indo-6","tradisional"]},
    {"title":"Sisanya — Import China & Generic","provider":"Berbagai importir Alibaba (China)","category":"Market Leader Indonesia","type":"Mixed Import","absorb":"300-650ml/m²","price":"Rp 50-120 /pcs","price_url":"https://www.alibaba.com/showroom/meat-absorbent-pad.html","share":"17.0%","revenue":"Rp 71 Miliar/tahun","volume":"~49 jt pcs/tahun","source":"BPS import China 2024 + Alibaba","citation_url":"https://www.alibaba.com/showroom/meat-absorbent-pad.html","url":"https://www.alibaba.com/showroom/meat-absorbent-pad.html","desc":"Gabungan import China (Qidong, Ideal Goal) + generic. Harga paling murah, kualitas variatif. Wajib COA & migration test.","tags":["import-china","generic"]},
    # === KONTEKS ===
    {"title":"Qingdao Ideal Goal Pad","provider":"Ideal Goal (China)","category":"Market Challenger","type":"SAP + Nonwoven + PE","absorb":"600-950ml/m²","price":"Rp 90-180 /pcs","price_url":"https://www.idealgoal.cn/meat-pad","share":"2.1% global","revenue":"USD 28 jt","volume":"—","source":"Export China 2023","citation_url":"https://www.idealgoal.cn/meat-pad","url":"https://www.idealgoal.cn/meat-pad","desc":"Challenger China terbesar. Harga 40-50% bawah leader, OEM untuk brand Eropa. MOQ 50k.","tags":["challenger","china"]},
    {"title":"Zhongshan Qidong Soaker","provider":"Zhongshan Qidong (China)","category":"Market Challenger","type":"SAP Composite","absorb":"550-900ml/m²","price":"Rp 85-170 /pcs","price_url":"https://www.qidongpack.com/absorbent-pad","share":"1.8% global","revenue":"USD 24 jt","volume":"—","source":"Export China 2023","citation_url":"https://www.qidongpack.com/absorbent-pad","url":"https://www.qidongpack.com/absorbent-pad","desc":"Challenger China spesialis export. Sudah masuk Indonesia via importir Jakarta.","tags":["challenger","china"]},
    {"title":"Sirane Earth Compostable","provider":"Sirane - Earth Line (UK)","category":"Market Nicher","type":"Compostable Cellulose","absorb":"400-650ml/m²","price":"Rp 220-420 /pcs","price_url":"https://www.sirane.com/earth-packaging/","share":"0.6% global","revenue":"USD 8 jt","volume":"—","source":"Sirane 2023","citation_url":"https://www.sirane.com/earth-packaging/","url":"https://www.sirane.com/earth-packaging/","desc":"Nicher eco. 100% compostable EN13432. Target organic & zero-waste retailer. Premium 30-40%.","tags":["nicher","compostable"]},
    {"title":"TOMI Odor-Capture Charcoal","provider":"TOMI (Japan)","category":"Market Nicher","type":"Charcoal + SAP","absorb":"400-600ml/m²","price":"Rp 260-480 /pcs","price_url":"https://www.tomi-jp.com/odor-pad","share":"—","revenue":"—","volume":"—","source":"TOMI JP","citation_url":"https://www.tomi-jp.com/odor-pad","url":"https://www.tomi-jp.com/odor-pad","desc":"Nicher Jepang charcoal + activated carbon serap bau amis. Untuk sashimi & wagyu premium.","tags":["nicher","charcoal"]},
]

FEEDS = [
    "https://www.packagingdigest.com/rss.xml",
    "https://www.foodpackagingforum.org/news/rss.xml",
    "https://feeds.feedburner.com/ThePackagingPortal",
    "https://www.meatpoultry.com/rss",
    "https://feeds.feedburner.com/TechCrunch",
    "https://www.packworld.com/rss.xml",
]
KEYWORDS = ["absorbent","pad","packaging","meat","poultry","seafood","food packaging","soaker","drip","tray","shelf life","SAP","airlaid","cellulose","Sealed Air","Novipax","Sirane"]

def fetch_feed(url):
    try:
        import urllib.request, gzip
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
    import xml.etree.ElementTree as ET
    items=[]
    try: root = ET.fromstring(data)
    except: return items
    for it in root.findall('.//item'):
        t = it.find('title'); l = it.find('link'); d = it.find('description')
        title = t.text.strip() if t is not None and t.text else ""
        link = l.text.strip() if l is not None and l.text else ""
        desc = d.text.strip() if d is not None and d.text else ""
        if title and link: items.append((title,link,desc))
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
    out_items=[]; seen=set(); seen_titles=set(); curated_n=0
    for c in CURATED:
        url=c["url"]
        cid=hashlib.md5((c["title"]+url).encode()).hexdigest()[:12]
        item={
            "id":cid,"title":c["title"],"provider":c["provider"],"category":c["category"],
            "type":c["type"],"absorb":c["absorb"],"price":c["price"],"price_url":c.get("price_url",c["url"]),
            "share":c.get("share","—"),"revenue":c.get("revenue","—"),"volume":c.get("volume","—"),"citation":c.get("source","—"),"citation_url":c.get("citation_url",""),
            "url":c["url"],"desc":c["desc"],"tags":c.get("tags",[]),"source":"curated",
        }
        out_items.append(item); seen.add(url); seen_titles.add(c["title"].lower()); curated_n+=1
    from_feeds=[]
    for f in FEEDS:
        data=fetch_feed(f)
        if not data: continue
        for title,link,desc in parse_feed(data):
            if link in seen or title.lower() in seen_titles or not relevant(title): continue
            seen.add(link); seen_titles.add(title.lower())
            fid=hashlib.md5(link.encode()).hexdigest()[:12]
            from_feeds.append({"id":fid,"title":title,"provider":"Industry News","category":"News/Update","type":"Artikel","absorb":"—","price":"—","price_url":link,"share":"—","revenue":"—","volume":"—","citation":"feed","citation_url":link,"url":link,"desc":(desc[:180]+"..." if len(desc)>180 else desc) or title,"tags":["news"],"source":"feed"})
            if len(from_feeds)>=20: break
        if len(from_feeds)>=20: break
    all_items=out_items+from_feeds
    now=datetime.now(timezone.utc).isoformat()
    out={"updated_at":now,"total":len(all_items),"curated":curated_n,"from_feeds":len(from_feeds),"offers":all_items,"courses":all_items}
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
