
let reset_btn = document.getElementById('reset-btn')
var ca = ''
reset_btn.onclick = function(){
    fetch('/reset')
    .then(response => response.json())
    .then(data =>{
         ca = data.test;
    });
    console.log(ca)
}

