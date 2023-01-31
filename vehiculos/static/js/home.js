// Solo destinado a la funcionalidad web de la pagina home "/"

// Boton Home Scrolling a Ofertas Destacadas

const boton = document.querySelector(".seeOffer");

boton.addEventListener('click', () => {
    document.querySelector(".ofertasTitle").scrollIntoView();
})

// INPUT HOME POST

// Convertimos los inputs de charField a dateField (no es posible en el forms.py)

document.getElementsByName("fechaRetiro")[0].type = 'datetime-local'
document.getElementsByName("fechaRegreso")[0].type = 'datetime-local'

// Tambien se puede hacer mediante sessionStorage (creeria un toque mas seguro)
const submitDivCars = () => {
    console.log('activado')
    if(document.referrer == "http://127.0.0.1:8000/") {
        if(window.location.hash == "#show") {
            const divCars = document.getElementsByClassName("autosDisponiblesDiv")[0]
            divCars.style.display = "initial"
        }
    }
}

submitDivCars();