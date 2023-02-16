// Checkout detalles UI

const precioximp = Number((document.getElementById("precioximp").textContent).replace("$",""))
const precioimp = Number((document.getElementById("precioimp").textContent).replace("$",""))

document.getElementById("precioFinalCheckout").textContent = "$" + (precioimp + precioximp);

const fechaRetiro = document.getElementById("retiroFecha");
const fechaRegreso = document.getElementById("regresoFecha");

const fechaConvertidaRetiro = new Date(fechaRetiro.textContent)
const fechaConvertidaRegreso = new Date(fechaRegreso.textContent)

fechaRetiro.innerText = fechaConvertidaRetiro.toLocaleDateString("es-ES", { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'})
fechaRegreso.innerText = fechaConvertidaRegreso.toLocaleDateString("es-ES", { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })