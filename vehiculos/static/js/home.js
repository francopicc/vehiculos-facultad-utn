// Solo destinado a la funcionalidad web de la pagina home "/"

// Boton Home Scrolling a Ofertas Destacadas

const boton = document.querySelector(".seeOffer");

boton.addEventListener('click', () => {
    document.querySelector(".ofertasTitle").scrollIntoView();
})