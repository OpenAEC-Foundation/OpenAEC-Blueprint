"""Probe exact pinned save/close callback bodies using in-memory dependencies only."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT=Path(__file__).resolve().parent.parent
SOURCE=ROOT/'work/ui-research/upstream/calc-b470427'
WORK=ROOT/'work/ui-research/probes/save'
WORK.mkdir(exist_ok=True)
app=(SOURCE/'src/App.tsx').read_text()
hook=(SOURCE/'src/hooks/useFileOperations.ts').read_text()
save_body=re.search(r'const saveFile = useCallback\(async \(\) => \{(.*?)\n  \}, \[updateDocument, addToRecentFiles\]\);',hook,re.S).group(1)
close_body=re.search(r'unlisten = await win\.onCloseRequested\(async \(event\) => \{(.*?)\n        \}\);',app,re.S).group(1)
(WORK/'callbacks.json').write_text(json.dumps({'save':save_body,'close':close_body},ensure_ascii=False,indent=2)+'\n')
script=r'''import fs from 'node:fs';
import assert from 'node:assert/strict';
const bodies=JSON.parse(fs.readFileSync(new URL('./callbacks.json',import.meta.url),'utf8'));
const AsyncFunction=Object.getPrototypeOf(async function(){}).constructor;
const results=[];
function fixture({docs=['A'],active='A',answer='save',delay=false,fail=false,cancelAs=false}={}) {
 let state={documents:docs.map(id=>({id,fileName:id,filePath:cancelAs?null:`/virtual/${id}.ifcCalc`,isModified:true})),activeDocumentId:active,items:[{revision:1}],schedule:{},projectInfo:{}};
 const log={prompt:[],writes:[],completed:[],errors:[],destroyed:false,prevented:false,waiters:[]};
 const store={getState:()=>state};
 const updateDocument=(id,partial)=>{state={...state,documents:state.documents.map(d=>d.id===id?{...d,...partial}:d)}};
 const write=async(path,json)=>{const payload=JSON.parse(json);log.writes.push({path,payload});if(delay)await new Promise((resolve,reject)=>log.waiters.push({resolve,reject}));if(fail)throw Error('simulated write failure');log.completed.push({path,payload});};
 const save=new Function('useAppStore','serializeProject','isNativeSavePath','isTauriEnvironment','saveFileToPath','updateDocument','showError','toIfcCalcPath','saveFileAsNative','fileNameFromPath','addToRecentFiles','browserDownload',`return async () => {${bodies.save}}`)(store,(_s,items)=>JSON.stringify({items}),()=>true,()=>true,write,updateDocument,async e=>log.errors.push(e),()=>'/virtual/new.ifcCalc',async()=>cancelAs?null:'/virtual/new.ifcCalc',()=> 'new',()=>{},()=>{throw Error('unexpected browser branch')});
 const close=new AsyncFunction('event','useAppStore','showUnsavedChangesDialog','saveFileForClose','win',bodies.close);
 const request=()=>close({preventDefault:()=>{log.prevented=true}},store,async name=>{log.prompt.push(name);return answer},save,{destroy:()=>{log.destroyed=true}});
 return {log,save,request,state:()=>state,change:(revision)=>{state={...state,items:[{revision}],documents:state.documents.map(d=>d.id===state.activeDocumentId?{...d,isModified:true}:d)}},activate:id=>{state={...state,activeDocumentId:id}}};
}
function row(name,f,extra={}) {results.push({name,prompt:f.log.prompt,write_paths:f.log.writes.map(w=>w.path),destroyed:f.log.destroyed,prevented:f.log.prevented,dirty_ids:f.state().documents.filter(d=>d.isModified).map(d=>d.id),...extra});}
let f=fixture();await f.request();assert.equal(f.log.destroyed,true);assert.equal(f.state().documents[0].isModified,false);row('single_success',f);
f=fixture({answer:'cancel'});await f.request();assert.equal(f.log.destroyed,false);assert.equal(f.log.writes.length,0);row('single_cancel',f);
f=fixture({fail:true});await f.request();assert.equal(f.log.destroyed,false);assert.equal(f.state().documents[0].isModified,true);assert.equal(f.log.errors.length,1);row('write_failure_keeps_window',f);
f=fixture({cancelAs:true});await f.request();assert.equal(f.log.destroyed,false);assert.equal(f.state().documents[0].isModified,true);row('save_as_cancelled',f);
f=fixture({docs:['A','B']});await f.request();assert.equal(f.log.destroyed,true);assert.deepEqual(f.state().documents.filter(d=>d.isModified).map(d=>d.id),['B']);row('two_dirty_first_is_active',f);
f=fixture({docs:['A','B'],active:'B'});await f.request();assert.deepEqual(f.log.prompt,['A']);assert.equal(f.log.writes[0].path,'/virtual/B.ifcCalc');assert.equal(f.log.destroyed,false);row('two_dirty_first_is_inactive',f);
f=fixture({docs:['A','B'],answer:'discard'});await f.request();assert.equal(f.log.destroyed,true);assert.deepEqual(f.log.prompt,['A']);row('discard_first_of_two_dirty',f);
f=fixture({delay:true});let pending=f.save();assert.equal(f.log.waiters.length,1);f.change(2);f.log.waiters[0].resolve();await pending;assert.equal(f.log.completed[0].payload.items[0].revision,1);assert.equal(f.state().items[0].revision,2);assert.equal(f.state().documents[0].isModified,false);row('edit_during_save',f,{persisted_revision:1,current_revision:2});
f=fixture({docs:['A','B'],delay:true});pending=f.save();f.activate('B');f.log.waiters[0].resolve();await pending;assert.deepEqual(f.state().documents.filter(d=>d.isModified).map(d=>d.id),['B']);row('switch_tab_during_save_preserves_target_id',f);
f=fixture({delay:true});let older=f.save();f.change(2);let newer=f.save();f.log.waiters[1].resolve();await newer;f.log.waiters[0].resolve();await older;assert.deepEqual(f.log.completed.map(w=>w.payload.items[0].revision),[2,1]);assert.equal(f.state().documents[0].isModified,false);row('overlapping_saves_complete_out_of_order',f,{completed_revisions:[2,1],last_completed_revision:1,current_revision:2});
process.stdout.write(JSON.stringify({node:process.version,scenarios:results}));
'''
(WORK/'run.mjs').write_text(script)
node='/home/aia08/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
r=subprocess.run([node,str(WORK/'run.mjs')],check=True,capture_output=True,text=True)
result=json.loads(r.stdout)
result['assertions']=len(re.findall(r'assert\.(?:equal|deepEqual)\(',script))
result.update({'checked_at':'2026-10-22','commit':'b47042704efa388d95eb59ce77d23aeb5ee0e44c','method':'Exacte saveFile- en onCloseRequested-callbackbodies uit gepinde Calc-bron, met in-memory store, dialoog-, serializer- en schrijfstubs. Echte controlflow; geen React/Tauri-event, schijf-I/O of productieapp.','source_hashes':{p:hashlib.sha256((SOURCE/p).read_bytes()).hexdigest() for p in ['src/App.tsx','src/hooks/useFileOperations.ts']},'limitations':['De serializer en bestanden worden niet uitgevoerd; uitkomsten beschrijven de callbacklogica onder gecontroleerde scenario’s.','Er is geen echt venster gesloten of bestand gewijzigd.','Of overige productlagen een scenario uitsluiten, moet end-to-end worden getoetst.','De parallelle schrijfvolgorde is bewust geforceerd om de ontbrekende volgorde-/revisiecontrole in deze callback zichtbaar te maken.']})
(WORK/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
out=ROOT/'outputs/OpenAEC-UI-proeven.json';data=json.loads(out.read_text());data['save_controlflow']=result;out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(result,ensure_ascii=False))
