// Extraccion de codigo de la URL
const codigoMP = window.location.pathname
const match = codigoMP.match(/([\d]+)/g);
const final = Number(match[0])

// Procedemos a hacer un fetch a la url de los detalles

const extractPaymentData = async () => {
    const divDetails = document.getElementsByClassName("orderDetailsFromURL")[0]
    const response = await fetch(`https://api.mercadopago.com/v1/payments/${final}`, {
        headers: {
            "Authorization": "Bearer TEST-8850533058234489-020920-ab66fe70eafe38da2d3348e0f25452f9-415909479",
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then((data)=>data.json())
    .then((converted)=>{
        if(converted.payment_method.id == "rapipago" || converted.payment_method.id == "pagofacil") {
            console.log("Pago con dinero")
            console.log(converted)
            let pago = null;
            if(converted.payment_method_id == "rapipago") {
                pago = "Efectivo: RapiPago"
            } else {
                pago = "Efectivo: PagoFacil"
            }
            divDetails.innerHTML = `
                <p class="messageDetailFromPayment">Podras encontrar este detalle de pago junto al comprobante, en tu perfil en la pestaña de compras. ( Perfil > Compras )</p>
                <div class="detailsFinal">
                    <h2 class="titleDetailsFinal">Detalles del pago</h2>
                    <p>Aqui encontraras mas informacion sobre la compra de tu ${converted.description}</p>
                    <div class="urLDivPayment">
                        <a href="${converted.transaction_details.external_resource_url}" class="urlToGoPaymentEfectivo">Ver mas informacion sobre el pago</a>
                    </div>
                </div>
                <div class="paymentStatus" id="efectivoStatus">
                    <div class="cuadroFinalDiv" id="${converted.status}">
                        <div id="paymentFinalDivStatus">
                            <label class="labelPayment">ESTADO DEL PAGO:</label>
                            <div>
                                <p class="labelPayment" id="labelStatus">PAGO EN ESPERA</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="detailsPaymentFinal">
                <div class="cuadrosPaymentFinalResult">
                    <div class="cuadroFinal">
                        <div class="cuadroFinalDiv">
                            <div class="textPaymentChoosen">
                                <label class="labelPaymentCardTitle">METODO DE PAGO UTILIZADO:</label>
                                <p class="labelPaymentCard">Pagaste con ${pago}</p>
                            </div>
                        </div>
                        <div class="cuadroFinalDiv">
                            <div class="textPaymentChoosenDiv">
                                <label class="labelPayment">PRECIO DE LA COMPRA:</label>
                                <p>$${converted.transaction_details.total_paid_amount}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `
        } else {
            let pago_con = null;
            if(converted.payment_method_id == "master") {
                pago_con = "Tarjeta de credito: Mastercard"
            } else if (converted.payment_method_id == "visa") {
                pago_con = "Tarjeta de credito: VISA"
            } else {
                pago_con = "Tarjeta de credito: American Express"
            }
            console.log("Pago con tarjeta")
            console.log(converted)
            divDetails.innerHTML = `
                <p class="messageDetailFromPayment">Podras encontrar este detalle de pago junto al comprobante, en tu perfil en la pestaña de compras. ( Perfil > Compras )</p>
                <div class="detailsFinal">
                    <h2 class="titleDetailsFinal">Detalles del pago</h2>
                    <p>Aqui encontraras mas informacion sobre la compra de tu ${converted.description}</p>
                </div>
                <div class="paymentStatus" id="efectivoStatus">
                    <div class="cuadroFinalDiv" id="${converted.status}">
                        <div id="paymentFinalDivStatus">
                            <label class="labelPayment">ESTADO DEL PAGO:</label>
                            <div>
                                <p class="labelPayment" id="labelStatus">PAGO ACEPTADO</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="detailsPaymentFinal">
                <div class="cuadrosPaymentFinalResult">
                    <div class="cuadroFinal">
                        <div class="cuadroFinalDiv">
                            <div class="textPaymentChoosen">
                                <label class="labelPaymentCardTitle">METODO DE PAGO UTILIZADO:</label>
                                <p class="labelPaymentCard">Pagaste con ${pago_con}</p>
                            </div>
                        </div>
                        <div class="cuadroFinalDiv">
                            <div class="textPaymentChoosenDiv">
                                <label class="labelPayment">PRECIO DE LA COMPRA:</label>
                                <p>$${converted.transaction_details.total_paid_amount}</p>
                            </div>
                        </div>
                    </div>
                </div>
        `
        }
    })

}

extractPaymentData()
