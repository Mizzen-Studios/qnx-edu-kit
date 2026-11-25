// Explicit HOST browser QA. Uses an installed Playwright-compatible package.
const {chromium}=require(process.env.EDU_QA_PLAYWRIGHT||'playwright');
const fs=require('fs'),path=require('path'),url=require('url'),cp=require('child_process'),http=require('http');
(async()=>{
 const root=path.resolve(__dirname,'..'),scratch=path.resolve(root,'.openclaw/trap-browser');fs.mkdirSync(scratch,{recursive:true});
 const server=http.createServer((req,res)=>{const file=path.resolve(root,'docs/site','.'+decodeURIComponent(req.url.split('?')[0]));if(!file.startsWith(path.join(root,'docs/site')+path.sep)){res.writeHead(403).end();return;}try{res.setHeader('Content-Type',file.endsWith('.js')?'application/javascript':'text/html');res.end(fs.readFileSync(file));}catch{res.writeHead(404).end();}});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const origin='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true,downloadsPath:path.join(scratch,'downloads'),executablePath:'/usr/bin/chromium-browser',args:['--no-sandbox']});
 const receipts=[];
 try{
 for(const width of [360,520,768,1280]){
 const context=await browser.newContext({viewport:{width,height:900},acceptDownloads:true}),page=await context.newPage(),errors=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url())&&!r.url().startsWith(origin+'/'))external.push(r.url());});
 await page.goto(origin+'/index.html');
 const entry=page.getByRole('link',{name:'Open the five-step worksheet'});const box=await entry.boundingBox();if(box.y>900)throw Error('worksheet link below mobile first screen');await entry.click();
 await page.waitForSelector('fieldset');
 await page.getByRole('button',{name:'Check all steps',exact:true}).click();if(!(await page.locator('#summary').textContent()).startsWith('0/5'))throw Error('missing answers');
 const data=await page.locator('#trap-data').textContent(),catalog=JSON.parse(data);
 for(const step of catalog.steps){
 const field=page.locator('#'+step.id),wrong=Object.keys(step.options).find(k=>k!==step.answer);
 await field.locator('input[value="'+wrong+'"]').check();await field.getByRole('button').click();if(!(await field.getByRole('status').textContent()).includes('RETRY'))throw Error('wrong answer accepted');
 await field.locator('input[value="'+step.answer+'"]').check();await field.getByRole('button').click();if(!(await field.getByRole('status').textContent()).includes('CORRECT'))throw Error('correct answer rejected');
 }
 await page.getByRole('button',{name:'Check all steps',exact:true}).click();if(!(await page.locator('#summary').textContent()).startsWith('5/5'))throw Error('all correct');
 const downloadEvent=page.waitForEvent('download');await page.getByRole('button',{name:'Download answers for CLI'}).click();const download=await downloadEvent;const answerPath=path.join(scratch,'answers-'+width+'.json');await download.saveAs(answerPath);
 const report=JSON.parse(cp.execFileSync('python3',['scripts/check_traps.py','--answers',answerPath],{cwd:root,encoding:'utf8'}));if(!report.complete||report.native_validation!=='NOT_RUN')throw Error('CLI parity');
 await page.locator('#receive input[value="error"]').check();if(!(await page.locator('#summary').textContent()).includes('changed'))throw Error('stale summary');
 await page.reload();await page.waitForSelector('fieldset');if(await page.locator('input:checked').count())throw Error('unexpected persistence');
 await page.keyboard.press('Tab');
 if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('overflow');
 await page.screenshot({path:path.join(scratch,'worksheet-'+width+'.png'),fullPage:true});
 await page.getByRole('link',{name:'Codelab instructions',exact:true}).click();if(!await page.getByRole('heading',{name:'Catch five QNX traps before the native lab',exact:true}).isVisible())throw Error('codelab navigation');
 if(errors.length||external.length)throw Error(JSON.stringify({errors,external}));
 receipts.push({width,height:900,entryY:box.y,missing:true,wrongAndCorrectEachStep:true,downloadCLIParity:true,staleFeedbackCleared:true,reloadResets:true,instructionsNavigation:true,overflow:false,pageErrors:errors,externalRequests:external,native_validation:'NOT_RUN'});
 await context.close();
 }
 fs.writeFileSync(path.join(scratch,'receipt.json'),JSON.stringify({scope:'HOST_BROWSER',receipts},null,2));console.log(JSON.stringify(receipts,null,2));
 }finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1});
