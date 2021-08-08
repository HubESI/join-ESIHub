const API_URL = "https://esihub.herokuapp.com";

const url_params = new URLSearchParams(window.location.search);
if(url_params.has("code")){
    const alert = document.getElementById("join-with-gh");
    fetch(`${API_URL}/check?code=${url_params.get("code")}`)
        .then((response) => response.json())
        .then((data) => {
            if(data.success) window.location.replace("https://github.com/HubESI");
            else{
                alert.style.color = "red";
                alert.innerHTML = data.description;
            }
        })
        .catch((error) => {
            alert.style.color = "red";
            alert.innerHTML = "An error occurred";
            log('Request failed', error);
        });
}

btn.addEventListener('click', () => {
    const email_field = document.querySelector(".input");
    const alert = document.getElementById("join-with-email")
    if (email_field.value.split("@")[1] !== "esi.dz"){
        alert.style.color = "red";
        alert.innerHTML = "Please provide your @esi.dz email";
        email_field.value = "@esi.dz";
    }
    else{
        fetch(`${API_URL}/check?email=${email_field.value}`)
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
