import { spawn } from 'node:child_process';
const CHROME='C:/Program Files/Google/Chrome/Application/chrome.exe';
export const sleep=ms=>new Promise(r=>setTimeout(r,ms));
export async function open(w=1400,h=1000){
  const port=9000+Math.floor(Math.random()*4000);
  const ch=spawn(CHROME,['--headless=new','--disable-gpu','--mute-audio',
    `--user-data-dir=${process.env.TEMP}/cdp-${port}`,`--remote-debugging-port=${port}`,
    `--window-size=${w},${h}`,'about:blank'],{stdio:'ignore'});
  await sleep(2800);
  const list=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  const ws=new WebSocket(list.find(x=>x.type==='page').webSocketDebuggerUrl);
  let id=0;const pend=new Map();const evs=[];
  ws.addEventListener('message',e=>{const m=JSON.parse(e.data);
    if(m.id&&pend.has(m.id)){pend.get(m.id)(m.result);pend.delete(m.id);}
    else if(m.method) evs.push(m);});
  await new Promise(r=>ws.addEventListener('open',r));
  const send=(m,p={})=>new Promise(res=>{const n=++id;pend.set(n,res);ws.send(JSON.stringify({id:n,method:m,params:p}));});
  const evalJS=async src=>{const r=await send('Runtime.evaluate',{expression:src,returnByValue:true,awaitPromise:true});return r?.result?.value;};
  const close=()=>{try{ws.close();}catch(e){} ch.kill(); spawn('taskkill',['/PID',String(ch.pid),'/T','/F'],{stdio:'ignore'});};
  await send('Page.enable');await send('Runtime.enable');
  return {send,evalJS,close,evs,sleep};
}
