

btn.addEventListener('click',()=>{
    
    const btn = document.getElementById('btn');
    const input = document.querySelector('.input').value;
    const alert = document.querySelector('.alert');

    let esi = '@esi.dz';
    if ( input.includes(esi) === false ){
        alert.innerHTML = 'Your email should contain @esi.dz';
        input.value = '@esi.dz';
    }
})


