// Este archivo servira solo para modificar algunas cosas en los detalles para que sean agradables a la UI y UX del usuario.


// Convertimos los strings de fechas a texto entendible.

const fechaRetiro = document.getElementById("fechaRetiro");
const fechaRegreso = document.getElementById("fechaRegreso");

const fechaConvertidaRetiro = new Date(fechaRetiro.textContent)
const fechaConvertidaRegreso = new Date(fechaRegreso.textContent)

fechaRetiro.innerText = fechaConvertidaRetiro.toLocaleDateString("es-ES", { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'})
fechaRegreso.innerText = fechaConvertidaRegreso.toLocaleDateString("es-ES", { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })

// Cantidad de dias entre esas dos fechas

const oneDay = 24 * 60 * 60 * 1000;
const diffDays = Math.round(Math.abs((fechaConvertidaRetiro.getTime() - fechaConvertidaRegreso.getTime()) / (oneDay)));
document.getElementById("daysCountBetween").innerText = "| " + diffDays + " dias"

// Resumen de la reserva

const impuestos = 105;

const precioFinalReserva = Number(document.getElementById("precioFinalDiaValor").textContent) * diffDays 
// Calculamos el precio por dias
document.getElementById("precioFinalDiaTexto").innerText = "Precio por " + diffDays + " dias"
document.getElementById("precioFinalDiaValor").innerText = "$" + precioFinalReserva

// Precio de los impuestos (105%)
const precioImpuestos = Number((document.getElementById("precioFinalDiaValor").textContent).replace("$",""))
document.getElementById("impuestosValor").innerText = "$" + (precioImpuestos * impuestos) / 100

// Precio Final

document.getElementById("finalValor").innerText = "$" + parseInt(precioFinalReserva + (precioImpuestos * impuestos) / 100)


document.getElementsByName("precioFinal")[0].value = precioFinalReserva
document.getElementsByName("precioImpuestos")[0].value = (precioImpuestos * impuestos) / 100
