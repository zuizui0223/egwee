#!/usr/bin/env python3
"""Official public Echinacea source inventory and table schemas only; no effects."""
import csv,hashlib,io,json,re,zipfile,tarfile
from urllib.request import Request,urlopen
from urllib.parse import urlparse,quote,urljoin
from urllib.error import HTTPError,URLError

HOSTS={"conservancy.umn.edu","hdl.handle.net","api.figshare.com","figshare.com","ndownloader.figshare.com"}
CAP=32*1024*1024
BASE="https://conservancy.umn.edu/server/api"
HANDLES={"ECH01":"11299/271643","ECH02":"11299/227155"}
FIG=23994528
def urlcheck(u):
    p=urlparse(u)
    if p.scheme!="https" or p.hostname not in HOSTS or p.username or p.password:raise ValueError("unexpected official host")
def get(u,cap=CAP):
    urlcheck(u)
    with urlopen(Request(u,headers={"User-Agent":"EGWEE-ECH source schema research audit","Accept":"*/*"}),timeout=25) as r:
        b=r.read(cap+1)
        if len(b)>cap:raise ValueError("source size cap")
        return b,r.geturl()
def js(u):return json.loads(get(u,4*1024*1024)[0])
def href(d,k):return d.get("_links",{}).get(k,{}).get("href")
def safe_name(s):return str(s).replace("\\","/").split("/")[-1][:160]
def table(b,n):
    if len(b)>CAP:return {"status":"oversize"}
    ext=n.lower().rsplit(".",1)[-1]
    if ext not in ("csv","tsv","txt"):return {"status":"not_delimited"}
    try:
        line=b.splitlines()[0].decode("utf-8-sig")
        sep="\t" if ext=="tsv" or (ext=="txt" and "\t" in line) else ","
        h=next(csv.reader([line],delimiter=sep))
        # Only short, field-name-like headers, never data or coordinates.
        if not h or len(h)>250 or any(len(x)>100 for x in h):return {"status":"header_ambiguous"}
        if len(h)<2 or not any(re.search("[A-Za-z]",x) for x in h):return {"status":"header_ambiguous"}
        if any(not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_. /()%-]*",x.strip()) for x in h):
            return {"status":"header_not_unambiguously_textual"}
        # Count only, no nonheader values emitted.
        return {"status":"headers_only","headers":[x.strip() for x in h],"physical_lines":len(b.splitlines())}
    except (UnicodeError,IndexError,csv.Error):return {"status":"header_read_stop"}
def inspect(b,n):
    d={"sha256":hashlib.sha256(b).hexdigest(),"bytes_read":len(b)}
    if zipfile.is_zipfile(io.BytesIO(b)):
        out=[]
        with zipfile.ZipFile(io.BytesIO(b)) as z:
            for f in z.infolist()[:200]:
                q={"member":safe_name(f.filename),"bytes":f.file_size}
                if not f.is_dir() and f.file_size<=CAP and safe_name(f.filename).lower().endswith((".csv",".tsv")):
                    q.update(table(z.read(f),f.filename))
                out.append(q)
        d["members"]=out
    else:d.update(table(b,n))
    return d
def download_entry(n,size,u):
    row={"name":safe_name(n),"declared_bytes":size}
    if size is None or not (0<size<=CAP) or not n.lower().endswith((".zip",".csv",".tsv",".txt",".rds",".rdata",".rda",".tar.gz")) or not u:
        row["access"]="inventory_only";return row
    try:
        b,_=get(u)
        if size!=len(b):raise ValueError("declared size mismatch")
        row.update(access="public_original_downloaded",**inspect(b,n))
    except Exception as e:
        row.update(access="download_stop",error=type(e).__name__)
        if isinstance(e,HTTPError):row["http_status"]=e.code
    return row
def drum(h):
    # DSpace public REST identifier resolution; fallback is the published Handle
    # landing redirect, then its exact item UUID, not guessed bitstream paths.
    errors=[]
    try:
        item=js(BASE+"/pid/find?id="+quote(h,safe=""))
    except Exception as e:
        errors.append(type(e).__name__+(" "+str(e.code) if isinstance(e,HTTPError) else ""))
        _,u=get("https://hdl.handle.net/"+h,4*1024*1024)
        urlcheck(u)
        m=re.search(r"/items/([0-9a-fA-F-]{36})(?:/|$)",urlparse(u).path)
        if not m:raise ValueError("public landing did not expose item UUID")
        item=js(BASE+"/core/items/"+m.group(1))
    if item.get("handle")!=h:raise ValueError("handle mismatch")
    bundles=js(href(item,"bundles"))
    entries=[]
    for b in bundles.get("_embedded",{}).get("bundles",[]):
        if b.get("name")!="ORIGINAL":continue
        u=href(b,"bitstreams")
        if not u:continue
        bits=js(u)
        if bits.get("page",{}).get("totalPages",1)>1:raise ValueError("bitstream pagination unresolved")
        for f in bits.get("_embedded",{}).get("bitstreams",[]):
            entries.append(download_entry(f.get("name",""),f.get("sizeBytes"),href(f,"content")))
    if not entries:raise ValueError("no advertised original bundle files")
    return {"status":"official_item_verified","handle":h,"title":item.get("name"),"files":entries,"resolver_fallback_errors":errors}
def figshare():
    m=js("https://api.figshare.com/v2/articles/"+str(FIG))
    if m.get("id")!=FIG or not str(m.get("doi","")).startswith("10.6084/m9.figshare.23994528"):raise ValueError("DOI mismatch")
    return {"status":"official_item_verified","doi":m.get("doi"),"title":m.get("title"),"files":[download_entry(f.get("name",""),f.get("size"),f.get("download_url")) for f in m.get("files",[])]}
def main():
    out={"status":"ECH_SOURCE_SCHEMA_ONLY","original_individual_values_exported":False,"no_model_fitted":True,"sources":{}}
    for k,h in list(HANDLES.items())+[("ECH03",None)]:
        try:d=drum(h) if h else figshare()
        except Exception as e:
            d={"status":"source_access_stop","error":type(e).__name__,"handle":h}
            if isinstance(e,HTTPError):d["http_status"]=e.code
        out["sources"][k]=d
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
