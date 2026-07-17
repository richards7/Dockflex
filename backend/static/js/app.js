const fileInput = document.getElementById("fileInput");
const form = document.getElementById("uploadForm");
const dropZone = document.getElementById("dropZone");
const fileDetails = document.getElementById("fileDetails");
const fileName = document.getElementById("fileName");
const clearFile = document.getElementById("clearFile");
const convertButton = document.getElementById("convertBtn");
const buttonText = document.getElementById("buttonText");
const message = document.getElementById("message");
const accepted = ["docx", "xlsx", "pdf", "jpg", "jpeg", "png"];

function setMessage(text = "", type = "") { message.textContent = text; message.className = `status ${type}`; }
function selectedFile() { return fileInput.files[0]; }
function displayFile() {
  const file = selectedFile();
  if (!file) { fileDetails.hidden = true; convertButton.disabled = true; return; }
  const extension = file.name.split(".").pop().toLowerCase();
  if (!accepted.includes(extension)) { setMessage("Please select a supported file type.", "error"); fileInput.value = ""; return displayFile(); }
  if (file.size > 50 * 1024 * 1024) { setMessage("Files must be 50 MB or smaller.", "error"); fileInput.value = ""; return displayFile(); }
  fileName.textContent = file.name; fileDetails.hidden = false; convertButton.disabled = false; setMessage();
}
fileInput.addEventListener("change", displayFile);
clearFile.addEventListener("click", () => { fileInput.value = ""; displayFile(); setMessage(); });
["dragenter", "dragover"].forEach(event => dropZone.addEventListener(event, e => { e.preventDefault(); dropZone.classList.add("dragging"); }));
["dragleave", "drop"].forEach(event => dropZone.addEventListener(event, e => { e.preventDefault(); dropZone.classList.remove("dragging"); }));
dropZone.addEventListener("drop", event => { if (event.dataTransfer.files.length) { fileInput.files = event.dataTransfer.files; displayFile(); } });

form.addEventListener("submit", async event => {
  event.preventDefault(); const file = selectedFile(); if (!file) return;
  convertButton.disabled = true; buttonText.textContent = "Converting…"; setMessage("Preparing your PDF…");
  const data = new FormData(); data.append("file", file);
  try {
    const response = await fetch("/upload", { method: "POST", body: data });
    if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.error || "Conversion failed. Please try again."); }
    const blob = await response.blob(); const url = URL.createObjectURL(blob); const link = document.createElement("a");
    link.href = url; link.download = `${file.name.replace(/\.[^.]+$/, "")}.pdf`; document.body.append(link); link.click(); link.remove(); URL.revokeObjectURL(url);
    setMessage("Your PDF is ready — download started.", "success");
  } catch (error) { setMessage(error.message, "error"); }
  finally { convertButton.disabled = !selectedFile(); buttonText.textContent = "Convert to PDF"; }
});
if ("serviceWorker" in navigator) window.addEventListener("load", () => navigator.serviceWorker.register("/static/sw.js"));
