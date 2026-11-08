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
  await page.locator('#step3 summary').click();
  if(!await page.locator('#step3 pre').isVisible())throw Error('commands not opened');
  await page.getByRole('link',{name:'Evidence',exact:true}).click();
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(overflow||errors.length)throw Error(JSON.stringify({width,overflow,errors}));
  await page.keyboard.press('Tab');
  receipts.push({width,height:900,draftReload:true,download:true,CLIImport:true,commands:true,evidenceNavigation:true,overflow:false,pageErrors:errors,mediaCaptured:false});
  await context.close();
 }
 const pack=path.join(scratch,'pack');cp.execFileSync('python3',[path.join(root,'scripts/learner_session.py'),'export','--work',work,'--out',pack]);
 const manifest=JSON.parse(fs.readFileSync(path.join(pack,'pack.json')));
 if(!manifest.files['session.json'])throw Error('missing own session');
 console.log(JSON.stringify({label:'HOST browser interaction QA; no native run',receipts,export:true},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
