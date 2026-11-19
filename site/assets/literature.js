(function(){
  const state={q:'',topic:'',role:'',ver:'',oa:'',sort:'year',dir:-1};
  const byId=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let papers=[],topics={};
  function verBadge(v){
    if(v==='VERIFIED')return '<span class="badge ok" title="Crossref record matches title, first author and year">verified (Crossref)</span>';
    if(v==='ARXIV_API_VERIFIED')return '<span class="badge ok" title="arXiv record matches title, first author and year">verified (arXiv)</span>';
    return '<span class="badge pre" title="Not yet matched to a primary metadata record">'+esc(v.toLowerCase().replace(/_/g,' '))+'</span>';
  }
  function row(p){
    const links=[];
    if(p.doi)links.push('<a href="https://doi.org/'+esc(p.doi)+'" rel="noopener">DOI</a>');
    if(p.arxiv)links.push('<a href="https://arxiv.org/abs/'+esc(p.arxiv)+'" rel="noopener">arXiv</a>');
    if(p.oa_pdf)links.push('<a href="'+esc(p.oa_pdf)+'" rel="noopener">open PDF</a>');
    if(!links.length&&p.url)links.push('<a href="'+esc(p.url)+'" rel="noopener">page</a>');
    const tps=p.topics.map(t=>'<span class="badge topic">'+esc(topics[t]||t)+'</span>').join('');
    return '<tr><td><div class="title">'+esc(p.title)+'</div><div class="muted small">'+esc(p.first_author)+(p.venue?' &middot; '+esc(p.venue):'')+'</div>'+
      (p.key_idea?'<div class="small" style="margin-top:4px">'+esc(p.key_idea)+'</div>':'')+
      '<div>'+tps+'<span class="badge">'+esc(p.role.toLowerCase())+'</span>'+(p.peer_review==='preprint'?'<span class="badge pre">preprint</span>':'')+verBadge(p.verification)+'</div></td>'+
      '<td>'+esc(p.year)+'</td><td class="links">'+links.join('')+'</td></tr>';
  }
  function render(){
    const q=state.q.toLowerCase();
    let list=papers.filter(p=>(!state.topic||p.topics.includes(state.topic))&&(!state.role||p.role===state.role)&&
      (!state.ver||(state.ver==='verified'?/VERIFIED$/.test(p.verification):!/VERIFIED$/.test(p.verification)))&&
      (!state.oa||(state.oa==='yes'?!!p.oa_pdf:!p.oa_pdf))&&
      (!q||(p.title+' '+p.first_author+' '+p.venue+' '+p.key_idea+' '+p.method).toLowerCase().includes(q)));
    const k=state.sort;
    list.sort((a,b)=>{const x=k==='year'?(+a.year||0)-(+b.year||0):String(a[k]).localeCompare(String(b[k]));return x*state.dir;});
    byId('count').textContent=list.length+' of '+papers.length+' papers';
    byId('rows').innerHTML=list.map(row).join('');
  }
  function opt(sel,values,label){sel.innerHTML='<option value="">'+label+'</option>'+values.map(v=>'<option value="'+esc(v[0])+'">'+esc(v[1])+'</option>').join('');}
  fetch('data/papers.json').then(r=>r.json()).then(d=>{
    papers=d.papers;topics=d.topics;
    opt(byId('topic'),Object.entries(topics).filter(([k])=>papers.some(p=>p.topics.includes(k))),'All topics');
    opt(byId('role'),[...new Set(papers.map(p=>p.role))].sort().map(r=>[r,r.toLowerCase()]),'All roles');
    const h=new URLSearchParams(location.hash.slice(1));if(h.get('topic')){state.topic=h.get('topic');byId('topic').value=state.topic;}
    ['q','topic','role','ver','oa'].forEach(id=>byId(id).addEventListener('input',e=>{state[id]=e.target.value;render();}));
    document.querySelectorAll('th[data-k]').forEach(th=>th.addEventListener('click',()=>{const k=th.dataset.k;state.dir=state.sort===k?-state.dir:(k==='year'?-1:1);state.sort=k;render();}));
    byId('built').textContent=d.built;render();
  }).catch(()=>{byId('count').textContent='The paper list could not be loaded.';});
})();
