btn.addEventListener('click', () => {
    const email_field = document.querySelector(".input");
    const alert = document.querySelector(".alert");
    if (email_field.value.split("@")[1] !== "esi.dz"){
        alert.style.color = "red";
        alert.innerHTML = "Please provide your @esi.dz email";
        email_field.value = "@esi.dz";
    }
    else{
        fetch(`http://127.0.0.1:5000/check?email=${email_field.value}`)
        .then((response) => response.json())
        .then((data) => {
            alert.style.color = "green";
            alert.innerHTML = data.description;
        })
        .catch((error) => {
            alert.style.color = "red";
            alert.innerHTML = "An error occurred";
            log('Request failed', error);
        });
    };
})
