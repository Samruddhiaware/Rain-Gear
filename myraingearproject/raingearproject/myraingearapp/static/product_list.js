bar=document.getElementsByClassName('fa-bars')[0];
console.log(bar)
sidediv=document.getElementsByClassName('sidebar')
bar.addEventListener("Click",()=>{
    sidediv.classList.add("go-left")
    console.log(sidediv)


})