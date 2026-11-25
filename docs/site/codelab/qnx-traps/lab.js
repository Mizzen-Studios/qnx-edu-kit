'use strict';
// Original HOST worksheet. No eval, shell, remote requests, persistence or log import.
const catalog=JSON.parse(document.getElementById('trap-data').textContent);
const form=document.getElementById('worksheet');
const answers={};
for(const step of catalog.steps){
 const field=document.createElement('fieldset');field.id=step.id;
 const legend=document.createElement('legend');legend.textContent=step.title;field.append(legend);
 const question=document.createElement('p');question.textContent=step.question;field.append(question);
 for(const [value,label] of Object.entries(step.options)){
  const row=document.createElement('label'),radio=document.createElement('input');
  radio.type='radio';radio.name=step.id;radio.value=value;
  radio.addEventListener('change',()=>{answers[step.id]=value;feedback.textContent='Answer changed. Check this step again.';summary.textContent='Worksheet changed; check all steps for current feedback.';});
  row.append(radio,document.createTextNode(label));field.append(row);
 }
 const button=document.createElement('button');button.type='button';button.textContent='Check this step';
 const feedback=document.createElement('div');feedback.setAttribute('role','status');feedback.setAttribute('aria-live','polite');
 const check=()=>{
  const choice=answers[step.id];
  feedback.textContent=(choice===undefined?'MISSING: Choose an answer.':choice===step.answer?'CORRECT — HOST reasoning only.':'RETRY — Revisit this distinction.')+' Observation: '+step.observation+' Diagnosis: '+step.diagnosis+' Fix: '+step.fix;
  return choice===step.answer;
 };
 button.addEventListener('click',check);field.append(button,feedback);
 const source=document.createElement('a');source.textContent='Read the source';source.href=step.source;field.append(source);
 field.checkAnswer=check;form.append(field);
}
const summary=document.getElementById('summary');
document.getElementById('check-all').addEventListener('click',()=>{
 let correct=0;for(const field of form.querySelectorAll('fieldset'))if(field.checkAnswer())correct++;
 summary.textContent=correct+'/'+catalog.steps.length+' correct. HOST_STATIC_REASONING; native validation NOT_RUN. This is not compiler, runtime or independent learning acceptance.';
});
document.getElementById('download').addEventListener('click',()=>{
 const blob=new Blob([JSON.stringify({version:1,catalog_sha256:catalog.sha256,answers},null,2)],{type:'application/json'});
 const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='qnx-trap-answers.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
