const fileInput=document.getElementById("fileInput");

const button=document.getElementById("convertBtn");

const loader=document.getElementById("loader");

const message=document.getElementById("message");

button.onclick=async()=>{

if(fileInput.files.length===0){

alert("Select a file");

return;

}

loader.style.display="block";

message.innerHTML="";

const formData=new FormData();

formData.append("file",fileInput.files[0]);

try{

const response=await fetch("http://127.0.0.1:7000/upload", {

method:"POST",

body:formData

});

if(!response.ok){

throw new Error("Conversion Failed");

}

const blob=await response.blob();

const url=window.URL.createObjectURL(blob);

const a=document.createElement("a");

a.href=url;

a.download="converted.pdf";

document.body.appendChild(a);

a.click();

a.remove();

loader.style.display="none";

message.innerHTML="✅ Download Started";

}catch(e){

loader.style.display="none";

message.innerHTML="❌ Conversion Failed";

}

}

if("serviceWorker" in navigator){

window.addEventListener("load",()=>{

navigator.serviceWorker.register("sw.js");

});

}