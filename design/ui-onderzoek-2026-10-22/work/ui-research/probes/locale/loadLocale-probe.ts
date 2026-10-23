import assert from 'node:assert/strict';
function makeEnvironment(failing: Set<string>) {
 const ns=['common','ribbon','backstage','settings','feedback','grid','dialogs','releases','report','units'];
 const loadedLanguages=new Set(['en','nl']);
 const isKnownLanguage=(lang:string)=>['en','nl','fr'].includes(lang);
 const attempts: Record<string,number>={}; const added:string[]=[];
 const warnings:string[]=[];
 const console={warn:(...args:unknown[])=>warnings.push(String(args[0]))};
 const localeModules:Record<string,()=>Promise<{default:Record<string,string>}>>={};
 for (const n of ns) localeModules[`./locales/fr/${n}.json`]=async()=>{
   attempts[n]=(attempts[n]||0)+1;
   if(failing.has(n))throw new Error('injected importer failure');
   return {default:{label:n}};
 };
 const i18next={addResourceBundle:(_lang:string,n:string,..._rest:unknown[])=>{added.push(n);}};
async function loadLocale(lng: string): Promise<void> {
  const base = (lng || "").split("-")[0];
  if (!base || loadedLanguages.has(base) || !isKnownLanguage(base)) return;
  await Promise.all(
    ns.map(async (n) => {
      const importer = localeModules[`./locales/${base}/${n}.json`];
      if (!importer) return;
      try {
        const mod = await importer();
        i18next.addResourceBundle(base, n, mod.default ?? mod, true, true);
      } catch (err) {
        console.warn(`[i18n] Kan ${base}/${n}.json niet laden:`, err);
      }
    }),
  );
  loadedLanguages.add(base);
}
 return {loadLocale,attempts,added,warnings,loadedLanguages};
}
const rows=[];
const good=makeEnvironment(new Set());await good.loadLocale('fr');await good.loadLocale('fr');
assert.equal(good.added.length,10);assert.equal(Object.values(good.attempts).reduce((a,b)=>a+b,0),10);
rows.push({scenario:'success_then_repeat',attempts:good.attempts,bundles:good.added.length});
const failures=new Set(['common']);const partial=makeEnvironment(failures);await partial.loadLocale('fr');failures.clear();await partial.loadLocale('fr');
assert.equal(partial.loadedLanguages.has('fr'),true);assert.equal(partial.added.includes('common'),false);assert.equal(partial.attempts.common,1);
rows.push({scenario:'partial_failure_then_retry_after_repair',attempts:partial.attempts,bundles:partial.added,markedLoaded:partial.loadedLanguages.has('fr'),warnings:partial.warnings.length});
const skipped=makeEnvironment(new Set());await skipped.loadLocale('unknown');await skipped.loadLocale('en');
assert.equal(Object.keys(skipped.attempts).length,0);
rows.push({scenario:'unknown_and_bundled_skipped',attempts:skipped.attempts});
process.stdout.write(JSON.stringify({scenarios:rows,assertions:6},null,2));
