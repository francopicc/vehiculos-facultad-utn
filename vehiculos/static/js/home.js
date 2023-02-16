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

const botonform = document.getElementsByClassName("submitButtonFormHome")[0]

const checkFechaOnForm = () => {
    const fecha1 = document.getElementsByName("fechaRetiro")[0]
    const fecha2 = document.getElementsByName("fechaRegreso")[0]
    fecha2.addEventListener('change', () => {
        if(new Date(fecha1.value).getTime() > new Date(fecha2.value).getTime()) {
            botonform.disabled = 'disabled';
            document.getElementById("error").style.display = "initial"
            document.getElementById("errorMessage").innerHTML = "Ha ocurrido un error: las fechas no son correctas."
        } else {
            botonform.disabled = '';
            document.getElementById("error").style.display = "none"
            document.getElementById("errorMessage").innerHTML = ""
        }
    })
}

checkFechaOnForm();