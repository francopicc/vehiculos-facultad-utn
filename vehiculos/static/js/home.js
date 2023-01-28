// Solo destinado a la funcionalidad web de la pagina home "/"

// Boton Home Scrolling a Ofertas Destacadas

const boton = document.querySelector(".seeOffer");

boton.addEventListener('click', () => {
    document.querySelector(".ofertasTitle").scrollIntoView();
})

// INPUT HOME POST

// Checkbox en Input POST Home (Lista 1)

function checkSelection (id) {
    for(let i = 1; i <= 5; i++) {
        document.getElementById("check" + i).checked = false;
    }
    document.getElementById(id).checked = true;
}

// Checkbox en Input POST Home (Lista 2)

function checkSelection2 (id) {
    for(let i = 1; i <= 3; i++) {
        document.getElementById("checkbox" + i).checked = false;
    }
    document.getElementById(id).checked = true;
}
