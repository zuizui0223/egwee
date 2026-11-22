
// Independent CP002 recount. Does not import production audit code.
// Only allowed metadata and baseline predictors are retained.
// Outcome and visit numeric cells become validity flags immediately.
function utf8(s) {
  const a=[]; for(const ch of s){let x=ch.codePointAt(0);
    if(x<128)a.push(x);else if(x<2048)a.push(192|(x>>6),128|(x&63));
    else if(x<65536)a.push(224|(x>>12),128|((x>>6)&63),128|(x&63));
    else a.push(240|(x>>18),128|((x>>12)&63),128|((x>>6)&63),128|(x&63));
  }return Uint8Array.from(a);
}
function pad(b) {
  const p=new Uint8Array(Math.ceil((b.length+9)/64)*64);p.set(b);p[b.length]=128;
  const bits=b.length*8;for(let i=0;i<8;i++)p[p.length-1-i]=Math.floor(bits/2**(8*i))&255;
  return p;
}
function sha256(b){
  const k=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  const h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],p=pad(b),w=new Uint32Array(64);
  const rr=(x,n)=>(x>>>n)|(x<<(32-n));
  for(let o=0;o<p.length;o+=64){
    for(let j=0;j<16;j++)w[j]=(p[o+j*4]<<24)|(p[o+j*4+1]<<16)|(p[o+j*4+2]<<8)|p[o+j*4+3];
    for(let j=16;j<64;j++){const x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(rr(x,7)^rr(x,18)^(x>>>3))+w[j-7]+(rr(y,17)^rr(y,19)^(y>>>10)))>>>0;}
    let [a,b,c,d,e,f,g,z]=h;
    for(let j=0;j<64;j++){const t1=(z+(rr(e,6)^rr(e,11)^rr(e,25))+((e&f)^(~e&g))+k[j]+w[j])>>>0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&b)^(a&c)^(b&c)))>>>0;z=g;g=f;f=e;e=(d+t1)>>>0;d=c;c=b;b=a;a=(t1+t2)>>>0;}
    for(let j=0;j<8;j++)h[j]=(h[j]+[a,b,c,d,e,f,g,z][j])>>>0;
  }return h.map(x=>x.toString(16).padStart(8,"0")).join("");
}
function sha1(b){
  const h=[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0],p=pad(b),w=new Uint32Array(80);
  const rl=(x,n)=>(x<<n)|(x>>>(32-n));
  for(let o=0;o<p.length;o+=64){
    for(let j=0;j<16;j++)w[j]=(p[o+j*4]<<24)|(p[o+j*4+1]<<16)|(p[o+j*4+2]<<8)|p[o+j*4+3];
    for(let j=16;j<80;j++)w[j]=rl(w[j-3]^w[j-8]^w[j-14]^w[j-16],1)>>>0;
    let [a,b,c,d,e]=h;
    for(let j=0;j<80;j++){
      const f=j<20?(b&c)|(~b&d):j<40?b^c^d:j<60?(b&c)|(b&d)|(c&d):b^c^d;
      const k=j<20?0x5a827999:j<40?0x6ed9eba1:j<60?0x8f1bbcdc:0xca62c1d6;
      const t=(rl(a,5)+f+e+k+w[j])>>>0;e=d;d=c;c=rl(b,30)>>>0;b=a;a=t;
    }for(let j=0;j<5;j++)h[j]=(h[j]+[a,b,c,d,e][j])>>>0;
  }return h.map(x=>x.toString(16).padStart(8,"0")).join("");
}
const norm=x=>(x??"").trim().toLowerCase().replace(/\s+/g," ");
const miss=x=>["","na","nan","null","none"].includes(norm(x));
const numberSyntax=/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$/;
function readNumber(text){
  const s=text.trim();if(miss(s))return {kind:"missing",value:null};
  if(!numberSyntax.test(s))return {kind:"invalid",value:null};
  const value=Number(s);return Number.isFinite(value)?{kind:"finite",value}:{kind:"invalid",value:null};
}
function validOutcome(text,checkPercentage=false){const n=readNumber(text);return {finite:n.kind==="finite",nonnegative:n.kind==="finite"&&n.value>=0,above100:checkPercentage&&n.kind==="finite"&&n.value>100,kind:n.kind==="finite"?(n.value<0?"negative":"finite_nonnegative"):n.kind};}
function positivePredictor(text){const n=readNumber(text);return n.kind==="finite"&&n.value>0?n.value:null;}
function parseReduced(raw,pin){
  let header=[],column=0,line=0,value="",quoted=false,current={};const records=[];
  const textFields=new Set(["study_id","study_id2","site_id","crop","country","sampling_year","yield_units","taxa_recorded","use_visits_or_abundance","visitation_rate_units","sampling_visitation","sampling_abundance","management","Publication"]);
  function finishCell(){
    if(line===0)header.push(value);
    else {
      const key=header[column];
      if(textFields.has(key))current[key]=value;
      if(key==="yield")current.outcome=validOutcome(value,true);
      if(key==="visitation_rate")current.visits=validOutcome(value);
      if(key==="abundance")current.abundance=validOutcome(value);
      if(key==="field_size"||key==="plant_density")current[key]=positivePredictor(value);
    }column++;value="";
  }
  function finishRow(){
    finishCell();
    if(line===0){if(JSON.stringify(header)!==JSON.stringify(pin.expected_columns))throw new Error("Schema mismatch");}
    else {if(column!==header.length)throw new Error("Malformed row width");records.push(current);}
    current={};column=0;line++;
  }
  for(let i=0;i<raw.length;i++){
    const ch=raw[i];if(ch==='"'){if(quoted&&raw[i+1]==='"'){value+='"';i++;}else quoted=!quoted;}
    else if(ch===","&&!quoted)finishCell();
    else if((ch==="\n"||ch==="\r")&&!quoted){if(ch==="\r"&&raw[i+1]==="\n")i++;finishRow();}
    else value+=ch;
  }
  if(quoted)throw new Error("Unclosed CSV quote");if(value||column)finishRow();
  return records;
}
function dois(text){
  let s;try{s=decodeURIComponent(text);}catch(e){s=text.replace(/%([0-9a-f]{2})/gi,(_,h)=>String.fromCharCode(parseInt(h,16)));}
  return new Set([...s.matchAll(/10\.\d{4,9}\/[^\s,;]+/gi)].map(m=>m[0].replace(/\.+$/,"").toLowerCase()));
}
function components(records,allowed,includeStems,includeDoi){
  const groups=new Set(records.map(r=>r.study_id2));if([...groups].some(miss))throw new Error("Missing source group");
  const parents=new Map([...groups].map(x=>[x,x]));
  function find(x){while(parents.get(x)!==x){parents.set(x,parents.get(parents.get(x)));x=parents.get(x);}return x;}
  function union(a,b){parents.set(find(a),find(b));}
  const stemFirst=new Map(),doiFirst=new Map();
  for(const r of records){
    if(miss(r.study_id))throw new Error("Missing study identifier");
    if(includeStems){
      const stem=r.study_id.split("_").filter(token=>!/^(?:19|20)\d{2}$/.test(token)).join("_");
      if(stemFirst.has(stem))union(r.study_id2,stemFirst.get(stem));else stemFirst.set(stem,r.study_id2);
    }
    if(includeDoi)for(const doi of dois(r.Publication)){
      if(!allowed.has(doi))continue;
      if(doiFirst.has(doi))union(r.study_id2,doiFirst.get(doi));else doiFirst.set(doi,r.study_id2);
    }
  }
  const lookup=new Map([...groups].map(x=>[x,find(x)]));
  return {lookup,count:new Set(lookup.values()).size};
}
function distinctKey(r){return JSON.stringify([r.study_id,r.site_id,r.sampling_year]);}
function blockKey(r,lookup){return JSON.stringify([lookup.get(r.study_id2),norm(r.crop),norm(r.sampling_year),norm(r.yield_units),norm(r.visitation_rate_units),norm(r.sampling_visitation),norm(r.taxa_recorded)]);}
function frameCount(rows,lookup){
  return {rows:rows.length,crops:new Set(rows.map(r=>norm(r.crop)).filter(x=>!miss(x))).size,countries:new Set(rows.map(r=>norm(r.country)).filter(x=>!miss(x))).size,unique_study_site_year_keys:new Set(rows.map(distinctKey)).size,study_id2_groups:new Set(rows.map(r=>r.study_id2)).size,source_components:new Set(rows.map(r=>lookup.get(r.study_id2))).size};
}
function baselineAudit(frame,features,lookup,rules){
  const blocks=new Map();
  for(const r of frame){const key=blockKey(r,lookup);if(!blocks.has(key))blocks.set(key,[]);blocks.get(key).push(r);}
  const rawSizeHistogram={},completeSizeHistogram={},rawKeySizeHistogram={},completeKeySizeHistogram={};
  let completeRows=0,anyCompleteBlocks=0;const completeComponents=new Set(),completeKeySet=new Set();
  const buckets={
    at_least_five_unique_complete_keys:{blocks:0,complete_rows:0,components:new Set(),keys:new Set()},
    at_least_five_and_any_variation:{blocks:0,complete_rows:0,components:new Set(),keys:new Set()},
    at_least_five_and_half_pairs_different:{blocks:0,complete_rows:0,components:new Set(),keys:new Set()}
  };
  let withinBlockDuplicateCompleteRows=0;
  for(const rows of blocks.values()){
    const complete=rows.filter(r=>features.every(f=>f==="management"?Object.hasOwn(rules.management,norm(r.management)):r[f]!==null));
    const rawKeys=new Set(rows.map(distinctKey)).size,completeKeys=new Set(complete.map(distinctKey)).size;
    rawSizeHistogram[rows.length]=(rawSizeHistogram[rows.length]||0)+1;
    completeSizeHistogram[complete.length]=(completeSizeHistogram[complete.length]||0)+1;
    rawKeySizeHistogram[rawKeys]=(rawKeySizeHistogram[rawKeys]||0)+1;
    completeKeySizeHistogram[completeKeys]=(completeKeySizeHistogram[completeKeys]||0)+1;
    if(!complete.length)continue;
    anyCompleteBlocks++;completeRows+=complete.length;
    const component=lookup.get(complete[0].study_id2);completeComponents.add(component);
    const keys=new Set(complete.map(distinctKey));for(const k of keys)completeKeySet.add(k);
    withinBlockDuplicateCompleteRows+=complete.length-keys.size;
    if(keys.size<5)continue;
    const freq=new Map();
    for(const r of complete){
      const vector=JSON.stringify(features.map(f=>f==="management"?rules.management[norm(r.management)]:r[f]));
      freq.set(vector,(freq.get(vector)||0)+1);
    }
    const totalPairs=complete.length*(complete.length-1)/2;
    let equalPairs=0;for(const n of freq.values())equalPairs+=n*(n-1)/2;
    const anyVariation=freq.size>1,halfDifferent=2*(totalPairs-equalPairs)>=totalPairs;
    const names=["at_least_five_unique_complete_keys"];
    if(anyVariation)names.push("at_least_five_and_any_variation");
    if(halfDifferent)names.push("at_least_five_and_half_pairs_different");
    for(const name of names){const b=buckets[name];b.blocks++;b.complete_rows+=complete.length;b.components.add(component);for(const k of keys)b.keys.add(k);}
  }
  const result={features,raw_block_row_size_histogram:rawSizeHistogram,complete_block_row_size_histogram_including_zero:completeSizeHistogram,raw_block_unique_key_size_histogram:rawKeySizeHistogram,complete_block_unique_key_size_histogram_including_zero:completeKeySizeHistogram,candidate_rows:frame.length,all_measurement_blocks:blocks.size,complete_rows:completeRows,unique_complete_keys:completeKeySet.size,blocks_with_any_complete_row:anyCompleteBlocks,components_with_any_complete_row:completeComponents.size,within_block_duplicate_complete_rows:withinBlockDuplicateCompleteRows};
  for(const [name,b]of Object.entries(buckets))result[name]={blocks:b.blocks,complete_rows:b.complete_rows,unique_complete_keys:b.keys.size,source_components:b.components.size};
  return result;
}
function recount(raw,rules,registry,pin){
  if(sha256(utf8("abc"))!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha1(utf8("abc"))!=="a9993e364706816aba3e25717850c26c9cd0d89d")throw new Error("Hash selftest failure");
  const b=utf8(raw),source={bytes:b.length,git_blob_sha1:sha1(utf8("blob "+b.length+"\0"+raw)),sha256:sha256(b)};
  if(source.bytes!==registry.field_pin.bytes||source.git_blob_sha1!==registry.field_pin.git_blob_sha1||source.sha256!==registry.field_pin.sha256)throw new Error("Frozen source mismatch");
  const records=parseReduced(raw,pin),allowed=new Set(registry.allowlist.map(x=>x.doi.toLowerCase()));
  const graph=components(records,allowed,true,true),lookup=graph.lookup;
  const graphCounts={study_id2_only:components(records,allowed,false,false).count,plus_year_stem:components(records,allowed,true,false).count,plus_vetted_doi:components(records,allowed,false,true).count,full_union:graph.count};
  const directFamilies=new Set(["reproductive_count_or_set","harvest_mass_area","harvest_mass_per_plant","harvest_mass_field","harvest_mass_fixed_part"]);
  const family=r=>rules.endpoint_labels.yield_units[norm(r.yield_units)];
  const identityComplete=r=>["study_id","study_id2","site_id","sampling_year","crop"].every(k=>!miss(r[k]));
  const reviewedTaxa=r=>{const key=norm(r.taxa_recorded);return Object.hasOwn(rules.taxa_scopes,key)&&!["none","unknown","missing"].includes(rules.taxa_scopes[key]);};
  const truePercentageLabels=new Set(rules.primary_true_percentage_labels);
  const percentageViolation=r=>truePercentageLabels.has(norm(r.yield_units))&&r.outcome.above100;
  const direct=records.filter(r=>identityComplete(r)&&r.outcome.nonnegative&&!percentageViolation(r)&&directFamilies.has(family(r)?.family)&&family(r)?.construction==="direct_or_reported");
  const withVisits=direct.filter(r=>r.visits.nonnegative);
  const timed=withVisits.filter(r=>rules.visit_methods[norm(r.sampling_visitation)]==="active_observation_compatible"&&rules.visit_units[norm(r.visitation_rate_units)]?.timed===true&&reviewedTaxa(r));
  const strict=timed.filter(r=>norm(r.use_visits_or_abundance)==="use visits");
  const area=strict.filter(r=>family(r).family==="harvest_mass_area");
  const abundanceBeforeScope=direct.filter(r=>norm(r.use_visits_or_abundance)==="use abundance"&&r.abundance.nonnegative);
  const abundance=abundanceBeforeScope.filter(reviewedTaxa);
  const abundanceExcluded=abundanceBeforeScope.filter(r=>!reviewedTaxa(r));
  const reviewedAbundanceMethods=new Set(rules.abundance_methods);
  const abundanceReviewedMethods=abundance.filter(r=>reviewedAbundanceMethods.has(norm(r.sampling_abundance)));
  const abundanceMethodExcluded=abundance.filter(r=>!reviewedAbundanceMethods.has(norm(r.sampling_abundance)));
  const knownMethodLabels=new Set(["sweep net","transects","na","focal observations","other","sweep net + other","pan trap, bee bowl, blue vane trap, pitfall","sweep net + focal observations","sweep net + pan trap, bee bowl, blue vane trap, pitfall"]);
  const excludedMethods={};for(const r of abundanceMethodExcluded){const label=norm(r.sampling_abundance);const boundedLabel=knownMethodLabels.has(label)?label:"unrecognized";excludedMethods[boundedLabel]=(excludedMethods[boundedLabel]||0)+1;}
  const abundanceMethodReconciliation={before_method_requirement:frameCount(abundance,lookup),after_method_requirement:frameCount(abundanceReviewedMethods,lookup),excluded_rows:abundanceMethodExcluded.length,excluded_source_components:new Set(abundanceMethodExcluded.map(r=>lookup.get(r.study_id2))).size,excluded_study_id2_groups:new Set(abundanceMethodExcluded.map(r=>r.study_id2)).size,excluded_sampling_method_counts:excludedMethods,zero_abundance_retained_by_rule:true};
  const excludedTaxa={};for(const r of abundanceExcluded){const key=norm(r.taxa_recorded);const reason=Object.hasOwn(rules.taxa_scopes,key)?rules.taxa_scopes[key]:"unrecognized";excludedTaxa[reason]=(excludedTaxa[reason]||0)+1;}
  const abundanceScopeReconciliation={before_scope_requirement:frameCount(abundanceBeforeScope,lookup),after_scope_requirement:frameCount(abundance,lookup),excluded_rows:abundanceExcluded.length,excluded_source_components:new Set(abundanceExcluded.map(r=>lookup.get(r.study_id2))).size,excluded_study_id2_groups:new Set(abundanceExcluded.map(r=>r.study_id2)).size,excluded_taxa_scope_counts:excludedTaxa};
  const selected={all_rows:records,direct_output:direct,direct_output_plus_numeric_total_visitation:withVisits,direct_output_plus_timed_observation:timed,strict_author_use_visits:strict,strict_area_harvest_mass:area,direct_author_use_abundance:abundance,direct_author_use_abundance_reviewed_methods:abundanceReviewedMethods};
  const frameCounts=Object.fromEntries(Object.entries(selected).map(([k,v])=>[k,frameCount(v,lookup)]));
  const baselines={};
  for(const [name,frame]of [["strict_direct",strict],["strict_mass_area",area]]){
    baselines[name]={all_three:baselineAudit(frame,["management","field_size","plant_density"],lookup,rules)};
    for(const f of ["management","field_size","plant_density"])baselines[name][f]=baselineAudit(frame,[f],lookup,rules);
  }
  const domain={};for(const f of ["outcome","visits","abundance"]){domain[f]={};for(const r of records)domain[f][r[f].kind]=(domain[f][r[f].kind]||0)+1;}
  domain.primary_explicit_percentage={reviewed_label_count:truePercentageLabels.size,finite_upper_bound_violations:records.filter(percentageViolation).length};
  const directLabel=r=>directFamilies.has(family(r)?.family)&&family(r)?.construction==="direct_or_reported";
  domain.reviewed_direct_label_primary={
    negative_rows:records.filter(r=>directLabel(r)&&r.outcome.kind==="negative").length,
    missing_rows:records.filter(r=>directLabel(r)&&r.outcome.kind==="missing").length,
    invalid_syntax_rows:records.filter(r=>directLabel(r)&&r.outcome.kind==="invalid").length,
    negative_rows_outside_direct_labels:records.filter(r=>!directLabel(r)&&r.outcome.kind==="negative").length
  };
  domain.required_identity_missing_rows=records.filter(r=>!identityComplete(r)).length;
  const unknownMetadata={
    primary_outcome_label:records.filter(r=>!Object.hasOwn(rules.endpoint_labels.yield_units,norm(r.yield_units))).length,
    visit_method:records.filter(r=>!Object.hasOwn(rules.visit_methods,norm(r.sampling_visitation))).length,
    visit_unit:records.filter(r=>!Object.hasOwn(rules.visit_units,norm(r.visitation_rate_units))).length,
    taxa_scope:records.filter(r=>!Object.hasOwn(rules.taxa_scopes,norm(r.taxa_recorded))).length,
    selector:records.filter(r=>!Object.hasOwn(rules.selectors,norm(r.use_visits_or_abundance))).length
  };
  return {status:"INDEPENDENT_AGGREGATE_RECOUNT",implementation:"Standalone JavaScript implementation; production audit module not read or imported; provenance helper read only for year-token and DOI semantics.",source,source_graph:graphCounts,frames:frameCounts,abundance_scope_reconciliation:abundanceScopeReconciliation,abundance_method_reconciliation:abundanceMethodReconciliation,domain_flags:domain,unknown_metadata_row_counts:unknownMetadata,baseline:baselines,criteria:{normalization:"trim, lowercase, collapse all whitespace; no unit conversions",direct_endpoint_families:[...directFamilies],percentage_check:"Only exact normalized primary_true_percentage_labels in the committed RULES receive the <=100 bound",direct_construction:"direct_or_reported",numeric_outcome_domain:"finite and nonnegative; <=100 only for committed primary_true_percentage_labels",visit_domain:"finite and nonnegative",timed_observation:"active-observation-compatible method, RULES timed=true unit, known non-none taxa scope",strict_selector:"use visits",abundance_frame:"Broad frame: complete study_id/study_id2/site_id/year/crop, direct eligible primary outcome, finite nonnegative abundance, author selector use abundance, and reviewed non-none/non-unknown taxa scope; method not screened",abundance_reviewed_method_frame:"Broad abundance frame additionally requires normalized sampling_abundance in the committed four-item RULES.abundance_methods allowlist; zero abundance retained",block:["source_component","normalized_crop","normalized_sampling_year","normalized_exact_primary_yield_unit","normalized_visit_unit","normalized_observation_method","normalized_taxa_scope"],complete:"recognized management; field_size>0 finite; plant_density>0 finite; for single-feature audits require only that feature",size_gate:"at least five distinct raw study_id × site_id × sampling_year keys among complete rows",variation:"at least two distinct baseline vectors among complete rows",half_pair_gate:"At least half of unordered complete-row pairs have different baseline vectors; compare integer pair counts; no outcome values used",duplicates:"No rows removed or averaged; distinct keys gate block size; pair counts use retained complete rows",source_graph:"All rows before filtering; study_id2 identity, exact underscore year-token removal, and 11 vetted DOI references; transitive closure"},semantic_limits:["Candidate keys are not certified physical-field identities.","Literal metadata eligibility does not verify original outcome construction or covariate timing.","Fixed-part and field-total mass families enter direct by explicit requested rule, but only area mass enters the area-specific frame.","Counts per flower per hour remains timed because RULES timed=true; no independent semantic override.","No modelling admission or biological effect estimate is implied."]};
}

if(typeof module!=="undefined"&&module.exports)module.exports={recount};

