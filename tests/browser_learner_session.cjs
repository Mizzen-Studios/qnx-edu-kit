// Explicit local QA only. No server, screenshots, recording or target invocation.
const {chromium}=require('playwright');
const fs=require('fs');
const path=require('path');
const cp=require('child_process');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const scratch=process.argv[2];if(!scratch)throw Error('external QA scratch directory required');
 fs.mkdirSync(scratch,{recursive:true});
 const work=path.join(scratch,'own');
 cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'init','--work',work]);
 const browser=await chromium.launch({headless:true,executablePath:process.env.EDU_QA_CHROMIUM||'/usr/bin/chromium-browser',args:['--no-sandbox']});
 const receipts=[];
 try{
 for(const width of [1280,768,520,360]){
  const context=await browser.newContext({viewport:{width,height:900},acceptDownloads:true});
  const page=await context.newPage();page.setDefaultTimeout(8000);const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(require('url').pathToFileURL(work+'/cockpit.html').href);
  const form=page.locator('form[data-stage="step3"]');
  await form.getByLabel('Prediction',{exact:true}).fill('Wrong complement edcba986; app exit0 cannot pass stage.');
  await form.getByLabel('Diagnosis',{exact:true}).fill('Change the write operand, not the oracle.');
  await form.getByLabel('Explanation',{exact:true}).fill('The fixed oracle requires edcba987.');
  await form.getByRole('button',{name:'Save local draft',exact:true}).click();
  await page.reload();
  if(!(await form.getByLabel('Prediction',{exact:true}).inputValue()).includes('edcba986'))throw Error('draft lost');
  const event=page.waitForEvent('download');
  await form.getByRole('button',{name:'Download notes for CLI import',exact:true}).click();
  const download=await event;const notes=path.join(scratch,'notes-'+width+'.json');await download.saveAs(notes);
  cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'notes','--work',work,'--file',notes]);
  await page.goto(require('url').pathToFileURL(work+'/cockpit.html').href);
  // CLI-authoritative changes must not silently restore a stale browser draft.
  await form.getByLabel('Prediction',{exact:true}).fill('INTENTIONAL LOCAL DRAFT');
  await form.getByRole('button',{name:'Save local draft',exact:true}).click();
  const authoritative=path.join(scratch,'authoritative-'+width+'.json');
  const session=JSON.parse(fs.readFileSync(work+'/session.json'));
  fs.writeFileSync(authoritative,JSON.stringify({session_id:session.id,stage:'step3',prediction:'NEW AUTHORITATIVE CLI NOTE'}));
  cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'notes','--work',work,'--file',authoritative]);
  await page.reload();
  if(await form.getByLabel('Prediction',{exact:true}).inputValue()!=='NEW AUTHORITATIVE CLI NOTE')throw Error('stale draft replaced CLI note');
  if(!await form.getByRole('alert').isVisible())throw Error('missing explicit draft conflict');
  await form.getByRole('button',{name:'Restore conflicting draft',exact:true}).click();
  await page.reload();
  if(await form.getByLabel('Prediction',{exact:true}).inputValue()!=='INTENTIONAL LOCAL DRAFT')throw Error('intentional restore lost');
  const notesData=JSON.parse(fs.readFileSync(authoritative));notesData.prediction='NEWER AUTHORITATIVE NOTE';fs.writeFileSync(authoritative,JSON.stringify(notesData));
  cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'notes','--work',work,'--file',authoritative]);
  await page.reload();
  await form.getByRole('button',{name:'Discard conflicting draft',exact:true}).click();
  await page.reload();
  if(await form.getByLabel('Prediction',{exact:true}).inputValue()!=='NEWER AUTHORITATIVE NOTE')throw Error('discard failed');
  // Legacy drafts without revision require explicit handling, too.
  await page.evaluate(id=>localStorage.setItem(id+':step3',JSON.stringify({prediction:'LEGACY'})),session.id);
  await page.reload();
  if(await form.getByLabel('Prediction',{exact:true}).inputValue()!=='NEWER AUTHORITATIVE NOTE')throw Error('legacy override');
  await form.getByRole('button',{name:'Discard conflicting draft',exact:true}).click();
  const finalDownload=page.waitForEvent('download');
  await form.getByRole('button',{name:'Download notes for CLI import',exact:true}).click();
  const finalNotes=path.join(scratch,'resolved-'+width+'.json');await (await finalDownload).saveAs(finalNotes);
  if(JSON.parse(fs.readFileSync(finalNotes)).prediction!=='NEWER AUTHORITATIVE NOTE')throw Error('resolved download reverted notes');
  cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'notes','--work',work,'--file',finalNotes]);
  // Render a fixture historical PASS, then edit the current source; no target invoked.
  cp.execFileSync('python3',['-c',"import sys;from pathlib import Path;sys.path[:0]=[sys.argv[1]+'/scripts',sys.argv[1]+'/tests'];import test_learner_session as t;import learner_session as c;x=t.SessionTests();x.work=Path(sys.argv[2]);x.temp=type('T',(),{'name':sys.argv[3]})();import shutil;shutil.rmtree(x.work/'attempts',ignore_errors=True);x.native_fixture();(x.work/'step3/main.c').write_text('new current source '+str(__import__('time').time_ns()));c.render(x.work)",root,work,scratch]);
  await page.reload();
  if(!await page.getByText('step3: CURRENT_STAGE_NOT_VALIDATED',{exact:false}).isVisible())throw Error('current validation stale');
  if(!await page.getByText('HISTORICAL — SOURCE MISMATCH',{exact:false}).first().isVisible())throw Error('historical mismatch missing');
  await page.locator('#step3 summary').click();
  if(!await page.locator('#step3 pre').isVisible())throw Error('commands not opened');
  await page.getByRole('link',{name:'Evidence',exact:true}).click();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(overflow||errors.length)throw Error(JSON.stringify({width,overflow,errors}));
  await page.keyboard.press('Tab');
  receipts.push({width,height:900,draftReload:true,draftConflict:true,explicitRestore:true,explicitDiscard:true,legacyConflict:true,sourceMismatch:true,download:true,CLIImport:true,commands:true,evidenceNavigation:true,overflow:false,pageErrors:errors,mediaCaptured:false});
  await context.close();
 }
 // Drop fixture attempts before this notes-only export (fixture export covered by unit tests).
 const state=JSON.parse(fs.readFileSync(work+'/session.json'));state.attempts=[];fs.writeFileSync(work+'/session.json',JSON.stringify(state));
 const pack=path.join(scratch,'pack');cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'export','--work',work,'--out',pack]);
 const manifest=JSON.parse(fs.readFileSync(path.join(pack,'pack.json')));
 if(!manifest.files['session.json'])throw Error('missing own session');
 console.log(JSON.stringify({label:'HOST browser interaction QA; no native run',receipts,export:true},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
