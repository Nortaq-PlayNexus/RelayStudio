'use strict';
const {contextBridge,ipcRenderer}=require('electron');
const invoke=(name,...args)=>ipcRenderer.invoke('relay:'+name,...args);
contextBridge.exposeInMainWorld('relayDesktop',Object.freeze({
 info:()=>invoke('info'),openFiles:()=>invoke('open-files'),openWorkspace:()=>invoke('open-workspace'),readWorkspace:id=>invoke('read-workspace',id),
 saveCopy:data=>invoke('save-copy',data),setKey:(provider,key,remember)=>invoke('set-key',provider,key,!!remember),forgetKey:provider=>invoke('forget-key',provider),
 chatStart:(data,id)=>invoke('chat-start',data,id),chatCancel:id=>invoke('chat-cancel',id),copy:text=>invoke('clipboard',text),importArchive:()=>invoke('import-archive'),diagnostics:()=>invoke('diagnostics'),
 onChatEvent:callback=>{const listener=(_event,data)=>callback(data);ipcRenderer.on('relay:chat-event',listener);return ()=>ipcRenderer.removeListener('relay:chat-event',listener);},
 onAction:callback=>{const listener=(_event,name)=>callback(name);ipcRenderer.on('relay:action',listener);return ()=>ipcRenderer.removeListener('relay:action',listener);}
}));
