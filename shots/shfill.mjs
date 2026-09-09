import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+process.argv[2]});
await sleep(1800);
const r=await P.send('Runtime.evaluate',{expression:`(()=>{try{
  var out=[];
  var hs=document.querySelectorAll('h2');
  for(var i=0;i<hs.length;i++){var h=hs[i];
    var w=h.closest('.wrap')||h.parentElement;
    var rg=document.createRange();rg.selectNodeContents(h);
    var ink=rg.getBoundingClientRect().width, m=w.getBoundingClientRect().width;
    out.push(h.textContent.trim().slice(0,44)+' | '+Math.round(ink)+'/'+Math.round(m)+' = '+(ink/m*100).toFixed(0)+'%');
  }
  return out.join(String.fromCharCode(10));
}catch(e){return 'ERR '+e.message}})()`,returnByValue:true});
console.log(r.result?.value ?? JSON.stringify(r));
P.close();process.exit(0);
