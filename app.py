# =============================================================================
# Country Information Service
# Single-file app: Flask serves the HTML UI at "/" AND the JSON API at
# "/country/<name>". No separate index.html needed.
# =============================================================================

import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# API ekata onima thenakin access karanna CORS allow karanawa
CORS(app, resources={r"/country/*": {"origins": "*"}})

# =============================================================================
# HTML UI — served at GET /
# The entire frontend (HTML + CSS + JS) is embedded as a Python string.
# =============================================================================
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Country Information Service</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#ffffff;--bg2:#f5f5f4;--bg3:#eeede9;
  --tx:#1a1a18;--tx2:#6b6b67;--tx3:#9b9b97;
  --bd:rgba(0,0,0,.10);--bd2:rgba(0,0,0,.18);
  --acc:#1a1a18;--acc-fg:#ffffff;
  --rm:8px;--rl:12px;
  --green:#15803d;--blue:#1d4ed8;--red:#b91c1c;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#1c1c1a;--bg2:#262624;--bg3:#2e2e2c;
  --tx:#f0efea;--tx2:#a8a8a4;--tx3:#6e6e6a;
  --bd:rgba(255,255,255,.10);--bd2:rgba(255,255,255,.18);
  --acc:#f0efea;--acc-fg:#1c1c1a;
  --green:#4ade80;--blue:#60a5fa;--red:#f87171;
}}
body{font-family:'DM Sans',sans-serif;background:var(--bg3);color:var(--tx);min-height:100vh;padding:2rem 1rem 4rem}
.app{max-width:680px;margin:0 auto}
.eyebrow{font-size:11px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--tx3);margin-bottom:.5rem;display:flex;align-items:center;gap:6px}
h1{font-family:'Syne',sans-serif;font-size:28px;font-weight:700;line-height:1.15;margin-bottom:2.5rem}
h1 span{color:var(--tx2);font-weight:400}
.search-bar{display:flex;gap:10px;margin-bottom:1.25rem}
.sw{flex:1;position:relative}
.si{position:absolute;left:13px;top:50%;transform:translateY(-50%);font-size:17px;color:var(--tx3);pointer-events:none}
input[type=text]{width:100%;height:46px;padding:0 14px 0 42px;font-size:15px;font-family:'DM Sans',sans-serif;border-radius:var(--rl);border:1px solid var(--bd2);background:var(--bg);color:var(--tx);outline:none;transition:border-color .15s}
input[type=text]::placeholder{color:var(--tx3)}
input[type=text]:focus{border-color:var(--acc)}
.btn{height:46px;padding:0 22px;font-size:14px;font-weight:500;font-family:'DM Sans',sans-serif;border-radius:var(--rl);border:none;background:var(--acc);color:var(--acc-fg);cursor:pointer;display:flex;align-items:center;gap:7px;transition:opacity .15s;white-space:nowrap}
.btn:hover{opacity:.82}.btn:disabled{opacity:.4;cursor:default}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:2rem}
.chip{font-size:12.5px;padding:5px 13px;border-radius:999px;border:.5px solid var(--bd);background:var(--bg2);color:var(--tx2);cursor:pointer;transition:border-color .15s,color .15s;font-family:'DM Sans',sans-serif}
.chip:hover{border-color:var(--bd2);color:var(--tx)}
.center{text-align:center;padding:3.5rem 1rem;color:var(--tx2)}
.center .ico{font-size:42px;display:block;margin-bottom:1rem;color:var(--tx3)}
.center p{font-size:15px}
.center code{background:var(--bg2);padding:2px 6px;border-radius:4px;font-size:13px}
@keyframes spin{to{transform:rotate(360deg)}}
.spinner{width:28px;height:28px;border:2.5px solid var(--bd2);border-top-color:var(--tx);border-radius:50%;animation:spin .7s linear infinite;margin:0 auto 1rem}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.result{animation:fadeUp .3s ease}
.card{background:var(--bg);border:.5px solid var(--bd);border-radius:var(--rl);padding:1.5rem}
.hero{display:flex;align-items:flex-start;gap:16px;margin-bottom:1.25rem}
.flag-sm{width:72px;height:48px;border-radius:6px;overflow:hidden;border:.5px solid var(--bd);flex-shrink:0}
.flag-sm img{width:100%;height:100%;object-fit:cover}
.cname{font-family:'Syne',sans-serif;font-size:22px;font-weight:700;line-height:1.15;margin-bottom:4px}
.cofficial{font-size:13px;color:var(--tx2);line-height:1.4}
.div{height:.5px;background:var(--bd);margin:1.25rem 0}
.sgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:1.25rem}
.sc{background:var(--bg2);border-radius:var(--rm);padding:14px 16px}
.slabel{font-size:11px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--tx3);margin-bottom:5px;display:flex;align-items:center;gap:5px}
.slabel i{font-size:13px}
.sval{font-size:16px;font-weight:500;color:var(--tx)}
.irow{display:flex;align-items:flex-start;gap:12px;padding:11px 0;border-bottom:.5px solid var(--bd)}
.irow:last-of-type{border-bottom:none}
.iico{width:32px;height:32px;border-radius:var(--rm);background:var(--bg2);display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px}
.iico i{font-size:16px;color:var(--tx2)}
.ilabel{font-size:12px;color:var(--tx3);margin-bottom:2px}
.ival{font-size:15px;color:var(--tx)}
.flagsec{margin-top:1.25rem;display:flex;align-items:center;gap:16px}
.flag-lg{border-radius:8px;overflow:hidden;border:.5px solid var(--bd);width:210px;height:124px;flex-shrink:0}
.flag-lg img{width:100%;height:100%;object-fit:cover;display:block}
.fmeta .ml{font-size:11px;font-weight:500;text-transform:uppercase;letter-spacing:.07em;color:var(--tx3);margin-bottom:5px}
.fmeta a{color:var(--blue);font-size:12px;text-decoration:none;word-break:break-all;line-height:1.5}
.fmeta a:hover{text-decoration:underline}
.footer{margin-top:2.5rem;text-align:center;font-size:12px;color:var(--tx3)}
.footer a{color:var(--blue);text-decoration:none}
.footer code{background:var(--bg2);padding:2px 6px;border-radius:4px}
</style>
</head>
<body>
<div class="app">
  <p class="eyebrow"><i class="ti ti-world"></i> Country Explorer</p>
  <h1>Country Information <span>Service</span></h1>

  <div class="search-bar">
    <div class="sw">
      <i class="ti ti-search si"></i>
      <input type="text" id="inp" placeholder="Enter a country name…" autocomplete="off"/>
    </div>
    <button class="btn" id="btn" onclick="go()">
      <i class="ti ti-arrow-right"></i> Search
    </button>
  </div>

  <div class="chips" id="chips"></div>
  <div id="out">
    <div class="center">
      <i class="ti ti-map-2 ico"></i>
      <p>Search any country above to view its details</p>
    </div>
  </div>

  <div class="footer">
    Powered by <a href="https://restcountries.com" target="_blank">REST Countries API</a>
  </div>
</div>

<script>
const CHIPS=['Sri Lanka','France','Japan','Brazil','Germany','New Zealand','Australia','Canada','South Africa','Egypt'];
const out=document.getElementById('out');
const inp=document.getElementById('inp');
const btn=document.getElementById('btn');
const cc=document.getElementById('chips');

CHIPS.forEach(n=>{
  const c=document.createElement('button');
  c.className='chip';c.textContent=n;
  c.onclick=()=>{inp.value=n;go();};
  cc.appendChild(c);
});

inp.addEventListener('keydown',e=>{if(e.key==='Enter')go();});

function pop(n){
  if(n>=1e9)return(n/1e9).toFixed(2)+' B';
  if(n>=1e6)return(n/1e6).toFixed(1)+' M';
  if(n>=1e3)return Math.round(n/1e3)+' K';
  return n.toLocaleString();
}

async function go(){
  const q=inp.value.trim();if(!q)return;
  btn.disabled=true;
  out.innerHTML=`<div class="center"><div class="spinner"></div><p>Fetching <strong>${q}</strong>…</p></div>`;
  try{
    const r=await fetch('/country/'+encodeURIComponent(q));
    const d=await r.json();
    if(!r.ok){
      out.innerHTML=`<div class="center"><i class="ti ti-map-off ico" style="color:var(--red)"></i><p>${d.error||'Country not found'}</p></div>`;
      btn.disabled=false;return;
    }
    out.innerHTML=`
<div class="result">
  <div class="card">
    <div class="hero">
      <div class="flag-sm"><img src="${d.flag}" alt="Flag of ${d.country_name}" onerror="this.parentElement.style.display='none'"/></div>
      <div>
        <div class="cname">${d.country_name}</div>
        <div class="cofficial">${d.official_name}</div>
      </div>
    </div>
    <div class="div"></div>
    <div class="sgrid">
      <div class="sc"><div class="slabel"><i class="ti ti-users"></i> Population</div><div class="sval">${pop(d.population)}</div></div>
      <div class="sc"><div class="slabel"><i class="ti ti-building-bank"></i> Capital</div><div class="sval">${d.capital}</div></div>
      <div class="sc"><div class="slabel"><i class="ti ti-coin"></i> Currency</div><div class="sval">${d.currency}</div></div>
    </div>
    <div class="div"></div>
    <div class="irow"><div class="iico"><i class="ti ti-map"></i></div><div><div class="ilabel">Region</div><div class="ival">${d.region}</div></div></div>
    <div class="irow"><div class="iico"><i class="ti ti-map-pin"></i></div><div><div class="ilabel">Subregion</div><div class="ival">${d.subregion}</div></div></div>
    <div class="div"></div>
    <div class="flagsec">
      <div class="flag-lg"><img src="${d.flag}" alt="Flag of ${d.country_name}"/></div>
      <div class="fmeta"><p class="ml">Flag URL</p><a href="${d.flag}" target="_blank">${d.flag}</a></div>
    </div>
  </div>
</div>`;
  }catch(e){
    out.innerHTML=`<div class="center"><i class="ti ti-wifi-off ico" style="color:var(--red)"></i><p>Cannot reach the server.</p></div>`;
  }
  btn.disabled=false;
}
</script>
</body>
</html>"""


# =============================================================================
# Route 1 — UI
# Serves the embedded HTML page when the user opens the root URL
# =============================================================================
@app.route("/", methods=["GET"])
def index():
    return HTML_PAGE, 200, {"Content-Type": "text/html; charset=utf-8"}


# =============================================================================
# Route 2 — API helper
# =============================================================================
def fetch_country_info(country_name: str):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url, timeout=10)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()
    c = data[0]

    capital_list = c.get("capital", [])
    currencies   = c.get("currencies", {})

    return {
        "country_name": c.get("name", {}).get("common", "N/A"),
        "official_name": c.get("name", {}).get("official", "N/A"),
        "capital":  ", ".join(capital_list) if capital_list else "N/A",
        "region":    c.get("region", "N/A"),
        "subregion": c.get("subregion", "N/A"),
        "population": c.get("population", 0),
        "currency":  ", ".join(i.get("name", k) for k, i in currencies.items()) or "N/A",
        "flag":      c.get("flags", {}).get("png", "N/A"),
    }


# =============================================================================
# Route 2 — API endpoint
# GET /country/<country_name>  →  JSON response
# =============================================================================
@app.route("/country/<path:country_name>", methods=["GET"])
def get_country(country_name: str):
    try:
        info = fetch_country_info(country_name)
        if info is None:
            return jsonify({"error": "Country not found"}), 404
        return jsonify(info), 200

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Unable to connect to the REST Countries API"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request to the REST Countries API timed out"}), 500
    except requests.exceptions.HTTPError as e:
        return jsonify({"error": f"Upstream API error: {e}"}), 500
    except (KeyError, IndexError, ValueError) as e:
        return jsonify({"error": f"Failed to parse country data: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


# =============================================================================
# Entry point
# =============================================================================
if __name__ == "__main__":
    # Render automatically assigns a PORT environment variable. 
    # If it's not found (like when running locally), it will default to 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
