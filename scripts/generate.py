#!/usr/bin/env python3
"""Regenerate data/sp500-compliance.csv from the live production screening cache.

Source of truth: the financedata2-api container's screening_results.sqlite3
read replica (same cache the Halal Terminal engine serves). Verdicts are copied
verbatim from the engine, with no re-screening or post-processing.

Universe: the 503 S&P 500 constituents of the 2026-07-28 bulk screening run.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "data", "sp500-compliance.csv")
CONTAINER = "financedata2-api"

SYMBOLS = [
    "A","AAPL","ABBV","ABNB","ABT","ACGL","ACN","ADBE","ADI","ADM","ADP","ADSK",
    "AEE","AEP","AES","AFL","AIG","AIZ","AJG","AKAM","ALB","ALGN","ALL","ALLE",
    "AMAT","AMCR","AMD","AME","AMGN","AMP","AMT","AMZN","ANET","AON","AOS","APA",
    "APD","APH","APO","APP","APTV","ARE","ARES","ATO","AVB","AVGO","AVY","AWK",
    "AXON","AXP","AZO","BA","BAC","BALL","BAX","BBY","BDX","BEN","BF-B","BG",
    "BIIB","BKNG","BKR","BLDR","BLK","BMY","BNY","BR","BRK-B","BRO","BSX","BX",
    "BXP","C","CAH","CARR","CASY","CAT","CB","CBOE","CBRE","CCI","CCL","CDNS",
    "CDW","CEG","CF","CFG","CHD","CHRW","CHTR","CI","CIEN","CINF","CL","CLX",
    "CMCSA","CME","CMG","CMI","CMS","CNC","CNP","COF","COHR","COIN","COO","COP",
    "COR","COST","CPAY","CPRT","CPT","CRH","CRL","CRM","CRWD","CSCO","CSGP","CSX",
    "CTAS","CTSH","CTVA","CVNA","CVS","CVX","D","DAL","DASH","DD","DDOG","DE",
    "DECK","DELL","DG","DGX","DHI","DHR","DIS","DLR","DLTR","DOC","DOV","DOW",
    "DPZ","DRI","DTE","DUK","DVA","DVN","DXCM","EA","EBAY","ECHO","ECL","ED",
    "EFX","EG","EIX","EL","ELV","EME","EMR","EOG","EQIX","EQR","EQT","ERIE","ES",
    "ESS","ETN","ETR","EVRG","EW","EXC","EXE","EXPD","EXPE","EXR","F","FANG",
    "FAST","FCX","FDS","FDX","FDXF","FE","FFIV","FICO","FIS","FISV","FITB","FIX",
    "FLEX","FOX","FOXA","FRT","FSLR","FTNT","FTV","GD","GDDY","GE","GEHC","GEN",
    "GEV","GILD","GIS","GL","GLW","GM","GNRC","GOOG","GOOGL","GPC","GPN","GRMN",
    "GS","GWW","HAL","HAS","HBAN","HCA","HD","HIG","HII","HLT","HON","HONA",
    "HOOD","HPE","HPQ","HRL","HSIC","HST","HSY","HUBB","HUM","HWM","IBKR","IBM",
    "ICE","IDXX","IEX","IFF","INCY","INTC","INTU","INVH","IP","IQV","IR","IRM",
    "ISRG","IT","ITW","IVZ","J","JBHT","JBL","JCI","JKHY","JNJ","JPM","KDP","KEY",
    "KEYS","KHC","KIM","KKR","KLAC","KMB","KMI","KO","KR","KVUE","L","LDOS","LEN",
    "LH","LHX","LII","LIN","LITE","LLY","LMT","LNT","LOW","LRCX","LULU","LUV",
    "LVS","LYB","LYV","MA","MAA","MAR","MAS","MCD","MCHP","MCK","MCO","MDLZ",
    "MDT","MET","META","MGM","MKC","MLM","MMM","MNST","MO","MOS","MPC","MPWR",
    "MRK","MRNA","MRSH","MRVL","MS","MSCI","MSFT","MSI","MTB","MTD","MU","NCLH",
    "NDAQ","NDSN","NEE","NEM","NFLX","NI","NKE","NOC","NOW","NRG","NSC","NTAP",
    "NTRS","NUE","NVDA","NVR","NWS","NWSA","NXPI","O","ODFL","OKE","OMC","ON",
    "ORCL","ORLY","OTIS","OXY","PANW","PAYX","PCAR","PCG","PEG","PEP","PFE","PFG",
    "PG","PGR","PH","PHM","PKG","PLD","PLTR","PM","PNC","PNR","PNW","PODD","PPG",
    "PPL","PRU","PSA","PSKY","PSX","PTC","PWR","PYPL","Q","QCOM","RCL","REG",
    "REGN","RF","RJF","RL","RMD","ROK","ROL","ROP","ROST","RSG","RTX","RVTY",
    "SBAC","SBUX","SCHW","SHW","SJM","SLB","SMCI","SNA","SNDK","SNPS","SO","SOLV",
    "SPG","SPGI","SRE","STE","STLD","STT","STX","STZ","SW","SWK","SWKS","SYF",
    "SYK","SYY","T","TAP","TDG","TDY","TECH","TEL","TER","TFC","TGT","TJX","TKO",
    "TMO","TMUS","TPL","TPR","TRGP","TRMB","TROW","TRV","TSCO","TSLA","TSN","TT",
    "TTD","TTWO","TXN","TXT","TYL","UAL","UBER","UDR","UHS","ULTA","UNH","UNP",
    "UPS","URI","USB","V","VEEV","VICI","VLO","VLTO","VMC","VRSK","VRSN","VRT",
    "VRTX","VST","VTR","VTRS","VZ","WAB","WAT","WBD","WDAY","WDC","WEC","WELL",
    "WFC","WM","WMB","WMT","WRB","WSM","WST","WTW","WY","WYNN","XEL","XOM","XYL",
    "XYZ","YUM","ZBH","ZBRA","ZTS",
]

INNER = r'''
import sqlite3, json, csv, sys
DB = "/app/data/screening_results.sqlite3"
symbols = sys.stdin.read().split()
conn = sqlite3.connect(DB)
w = csv.writer(sys.stdout)
w.writerow(["symbol","name","overall_status","aaoifi","djim","ftse","msci","sp",
            "purification_rate","as_of_date"])
OVERALL = {1: "compliant", 0: "non_compliant", None: "insufficient_data"}
def disp(bm, m):
    e = bm.get(m) if isinstance(bm, dict) else None
    if isinstance(e, dict) and e.get("disposition"):
        return e["disposition"]
    return "insufficient_data"
for s in symbols:
    row = conn.execute(
        "select is_compliant, purification_rate, payload_json, last_checked_at "
        "from screening_results where symbol=?", (s,)).fetchone()
    if not row:
        w.writerow([s, "", "insufficient_data", "insufficient_data",
                    "insufficient_data", "insufficient_data",
                    "insufficient_data", "insufficient_data", "", ""])
        continue
    is_comp, purif, payload, lca = row
    p = json.loads(payload) if payload else {}
    name = p.get("name") or ""
    overall = OVERALL.get(is_comp, "insufficient_data")
    bm = p.get("by_methodology") or {}
    aaoifi = disp(bm, "AAOIFI"); djim = disp(bm, "DJIM"); ftse = disp(bm, "FTSE")
    msci = disp(bm, "MSCI"); sp = disp(bm, "SP")
    pr = "" if purif is None else purif
    lc = p.get("last_checked_at") or lca or ""
    asof = lc[:10] if lc else ""
    w.writerow([s, name, overall, aaoifi, djim, ftse, msci, sp, pr, asof])
'''

def main():
    proc = subprocess.run(
        ["docker", "exec", "-i", CONTAINER, "python3", "-c", INNER],
        input="\n".join(SYMBOLS), capture_output=True, text=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit(1)
    with open(OUT, "w", newline="") as f:
        f.write(proc.stdout)
    lines = proc.stdout.strip().count("\n")
    sys.stderr.write("wrote %s (%d data rows)\n" % (OUT, lines))

if __name__ == "__main__":
    main()
