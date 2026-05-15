let language="en"
/* Kannada disease names */
let diseaseKannada={
"Healthy_Leaf":"ಆರೋಗ್ಯಕರ ಎಲೆ",
"Healthy_Nut":"ಆರೋಗ್ಯಕರ ಅಡಿಕೆ",
"Healthy_Trunk":"ಆರೋಗ್ಯಕರ ಕಾಂಡ",
"Mahali_Koleroga":"ಮಹಾಳಿ ರೋಗ",
"yellow_leaf_disease":"ಹಳದಿ ಎಲೆ ರೋಗ"
}
/* language button highlight */
function setLang(lang){
language=lang
document.getElementById("btnEn").classList.remove("active")
document.getElementById("btnKn").classList.remove("active")
if(lang=="en"){
document.getElementById("btnEn").classList.add("active")
}
else{
document.getElementById("btnKn").classList.add("active")
}
translateUI()
}
/* translate UI text */
function translateUI(){
if(language=="kn"){
document.getElementById("subtitle").innerText=
"ರೋಗ ಪತ್ತೆ ಮಾಡಲು ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"
document.getElementById("uploadTitle").innerText=
"1. ಎಲೆ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ"
document.getElementById("langLabel").innerText=
"ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ"
document.getElementById("uploadTip").innerText=
"ಇಲ್ಲಿ ಕ್ಲಿಕ್ ಮಾಡಿ ಎಲೆ ಚಿತ್ರ ಆಯ್ಕೆಮಾಡಿ"
document.getElementById("predictBtn").innerText=
"ರೋಗ ಕಂಡುಹಿಡಿಯಿರಿ"
document.getElementById("resultTitle").innerText=
"2. ಫಲಿತಾಂಶ"
document.getElementById("descTitle").innerText=
"ರೋಗದ ವಿವರಣೆ"
document.getElementById("precautionTitle").innerText=
"ತಡೆಯ ಕ್ರಮ"
document.getElementById("solutionTitle").innerText=
"ಪರಿಹಾರ"
}
else{
document.getElementById("subtitle").innerText=
"Upload leaf photo to detect disease and solution"
document.getElementById("uploadTitle").innerText=
"1. Upload Leaf Image"
document.getElementById("langLabel").innerText=
"Language"
document.getElementById("uploadTip").innerText=
"Click here or upload leaf image"
document.getElementById("predictBtn").innerText=
"Predict Disease"
document.getElementById("resultTitle").innerText=
"2. Result"
document.getElementById("descTitle").innerText=
"Disease Description"
document.getElementById("precautionTitle").innerText=
"Precautions"
document.getElementById("solutionTitle").innerText=
"Solution"
}
}
/* image preview */
document.getElementById("imageInput").onchange=function(e){
let reader=new FileReader()
reader.onload=function(){
document.getElementById("preview").src=reader.result
document.getElementById("status").innerText=""
}
reader.readAsDataURL(e.target.files[0])
}
/* prediction */
async function predict(){
let file=document.getElementById("imageInput").files[0]
if(!file){
alert("Upload image first")
return
}
/* processing text */
document.getElementById("status").innerText=
(language=="kn")?
"ವಿಶ್ಲೇಷಣೆ ನಡೆಯುತ್ತಿದೆ..." :
"Processing..."
let formData=new FormData()
formData.append("file",file)
let response=await fetch(
"http://127.0.0.1:8000/predict?lang="+language,
{
method:"POST",
body:formData
})
let data=await response.json()
/* translate disease name */
if(language=="kn"){
document.getElementById("disease").innerText=
diseaseKannada[data.class]
}
else{
document.getElementById("disease").innerText=
data.class.replaceAll("_"," ")
}

/* confidence */
document.getElementById("confidence").innerText=
"Confidence: "+data.confidence+"%"
/* description */
document.getElementById("description").innerText=
data.description
/* precautions */
document.getElementById("precaution").innerText=
data.precaution
/* solution */
document.getElementById("solution").innerText=
data.solution
/* completed text */
document.getElementById("status").innerText=
(language=="kn")?
"ಪೂರ್ಣಗೊಂಡಿದೆ":
"Completed"
}