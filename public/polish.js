// Focus, responsive navigation, and a keyboard-friendly response-mode popover.
(()=>{
 const shell=document.querySelector('.shell'),focus=document.querySelector('#focusToggle'),inspector=document.querySelector('#inspectorToggle'),mobile=document.querySelector('#mobileMenu'),menu=document.querySelector('#modeMenu'),trigger=document.querySelector('#modeCycle');
 function toggleFocus(){const enabled=shell.classList.toggle('focus-mode');focus.setAttribute('aria-pressed',String(enabled));focus.title=enabled?'Exit focus mode (Alt F)':'Focus mode (Alt F)';window.relayToast?.(enabled?'Focus mode · a little more room for your work.':'Workspace panels restored.');}
 focus.onclick=toggleFocus;
 inspector.onclick=()=>{if(innerWidth<=1050){shell.classList.remove('inspector-hidden');const open=shell.classList.toggle('inspector-mobile-open');inspector.setAttribute('aria-pressed',String(open));}else{const hidden=shell.classList.toggle('inspector-hidden');inspector.setAttribute('aria-pressed',String(hidden));}};
 mobile.onclick=()=>{const open=shell.classList.toggle('mobile-nav-open');mobile.setAttribute('aria-expanded',String(open));};
 document.querySelectorAll('.nav,.side-link,.session-list').forEach(e=>e.addEventListener('click',()=>{if(innerWidth<=600){shell.classList.remove('mobile-nav-open');mobile.setAttribute('aria-expanded','false');}}));
 function closeMode(){menu.hidden=true;trigger.setAttribute('aria-expanded','false');}
 function showMode(){menu.hidden=false;trigger.setAttribute('aria-expanded','true');document.querySelectorAll('[data-mode]').forEach(e=>{e.classList.toggle('selected',Number(e.dataset.mode)===task);e.querySelector('i').textContent=Number(e.dataset.mode)===task?'✓':'';});}
 trigger.onclick=()=>menu.hidden?showMode():closeMode();
 document.querySelectorAll('[data-mode]').forEach(e=>e.onclick=()=>{task=Number(e.dataset.mode);document.querySelector('#taskModeLabel').textContent=tasks[task];document.querySelector('#inspectorMode').textContent=tasks[task];closeMode();trigger.focus();});
 trigger.addEventListener('keydown',e=>{if(e.key==='ArrowDown'){e.preventDefault();showMode();menu.querySelector('button').focus();}});
 menu.addEventListener('keydown',e=>{const buttons=[...menu.querySelectorAll('button')],index=buttons.indexOf(document.activeElement);if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();buttons[(index+(e.key==='ArrowDown'?1:-1)+buttons.length)%buttons.length].focus();}if(e.key==='Escape'){closeMode();trigger.focus();}});
 document.addEventListener('click',e=>{if(!menu.contains(e.target)&&!trigger.contains(e.target))closeMode();if(innerWidth<=600&&shell.classList.contains('mobile-nav-open')&&!document.querySelector('.sidebar').contains(e.target)&&!mobile.contains(e.target)){shell.classList.remove('mobile-nav-open');mobile.setAttribute('aria-expanded','false');}});
 document.addEventListener('keydown',e=>{if(e.altKey&&e.key.toLowerCase()==='f'){e.preventDefault();toggleFocus();}if(e.key==='Escape'){closeMode();shell.classList.remove('mobile-nav-open','inspector-mobile-open');mobile.setAttribute('aria-expanded','false');if(innerWidth<=1050)inspector.setAttribute('aria-pressed','false');}});
 // State changes are announced through the existing session status and toast components.
})();
