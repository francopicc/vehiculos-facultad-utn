// Funcionamiento del pago de mercadopago en la pagina de checkout

const precioimp2 = Number((document.getElementById("precioimp").textContent).replace("$", ""))
const precioximp2 = Number((document.getElementById("precioximp").textContent).replace("$", ""))
const final = (precioimp2 + precioximp2).toString()

document.getElementById("transactionAmount").value = final
document.getElementById("transactionAmount_RAPI").value = final

// Configuracion del sistema de pagos

document.getElementById("optionPayment").addEventListener("change", (evt) => {
  if(evt.target.value == "tarjeta") {
    document.getElementById("tarjeta").style.display = "initial"
    document.getElementById("rapipago").style.display = "none"
    document.getElementById("efectivoSelection").style.display = "none"
  } else {
    document.getElementById("rapipago").style.display = "flex"
    document.getElementById("tarjeta").style.display = "none"
    document.getElementById("efectivoSelection").style.display = "flex"
  }
})

// Configuracion de pago en efectivo

// Este pequeño trozo de codigo es solo para comprobar si se reinicia la pagina y si no llega a detectar el evento change.

if(document.getElementById("efectivoSeleccionSelect").value == "pagoFacilCheck") {
  document.getElementById("payment_method").value = "pagofacil"
} else {
  document.getElementById("payment_method").value = "rapipago"
}

document.getElementById("efectivoSeleccionSelect").addEventListener("change", (evt) => {
  if(evt.target.value == "rapipagoCheck") {
    document.getElementById("payment_method").value = "rapipago"
  } else {
    document.getElementById("payment_method").value = "pagofacil"
  }
})

// MercadoPago

const mp = new MercadoPago("TEST-2b832490-3d65-4fb9-bc6e-1f06b374ef6a");

const cardNumberElement = mp.fields.create('cardNumber', {
  placeholder: "Número de la tarjeta"
}).mount('form-checkout__cardNumber');
const expirationDateElement = mp.fields.create('expirationDate', {
  placeholder: "MM/YY",
}).mount('form-checkout__expirationDate');
const securityCodeElement = mp.fields.create('securityCode', {
  placeholder: "Código de seguridad"
}).mount('form-checkout__securityCode');

(async function getIdentificationTypes() {
  try {
    const identificationTypes = await mp.getIdentificationTypes();
    const identificationTypeElement = document.getElementById('form-checkout__identificationType');

    createSelectOptions(identificationTypeElement, identificationTypes);
  } catch (e) {
    return console.error('Error getting identificationTypes: ', e);
  }
})();

function createSelectOptions(elem, options, labelsAndKeys = {
  label: "name",
  value: "id"
}) {
  const {
    label,
    value
  } = labelsAndKeys;

  elem.options.length = 0;

  const tempOptions = document.createDocumentFragment();

  options.forEach(option => {
    const optValue = option[value];
    const optLabel = option[label];

    const opt = document.createElement('option');
    opt.value = optValue;
    opt.textContent = optLabel;

    tempOptions.appendChild(opt);
  });

  elem.appendChild(tempOptions);
}

const paymentMethodElement = document.getElementById('paymentMethodId');
const issuerElement = document.getElementById('form-checkout__issuer');
const installmentsElement = document.getElementById('form-checkout__installments');

const issuerPlaceholder = "Banco emisor";
const installmentsPlaceholder = "Cuotas";

let currentBin;
cardNumberElement.on('binChange', async (data) => {
  const {
    bin
  } = data;
  try {
    if (!bin && paymentMethodElement.value) {
      clearSelectsAndSetPlaceholders();
      paymentMethodElement.value = "";
    }

    if (bin && bin !== currentBin) {
      const {
        results
      } = await mp.getPaymentMethods({
        bin
      });
      const paymentMethod = results[0];

      paymentMethodElement.value = paymentMethod.id;
      updatePCIFieldsSettings(paymentMethod);
      updateIssuer(paymentMethod, bin);
      updateInstallments(paymentMethod, bin);
    }

    currentBin = bin;
  } catch (e) {
    console.error('error getting payment methods: ', e)
  }
});

function clearSelectsAndSetPlaceholders() {
  clearHTMLSelectChildrenFrom(issuerElement);
  createSelectElementPlaceholder(issuerElement, issuerPlaceholder);

  clearHTMLSelectChildrenFrom(installmentsElement);
  createSelectElementPlaceholder(installmentsElement, installmentsPlaceholder);
}

function clearHTMLSelectChildrenFrom(element) {
  const currOptions = [...element.children];
  currOptions.forEach(child => child.remove());
}

function createSelectElementPlaceholder(element, placeholder) {
  const optionElement = document.createElement('option');
  optionElement.textContent = placeholder;
  optionElement.setAttribute('selected', "");
  optionElement.setAttribute('disabled', "");

  element.appendChild(optionElement);
}

// Este paso mejora las validaciones de cardNumber y securityCode
function updatePCIFieldsSettings(paymentMethod) {
  const {
    settings
  } = paymentMethod;

  const cardNumberSettings = settings[0].card_number;
  cardNumberElement.update({
    settings: cardNumberSettings
  });

  const securityCodeSettings = settings[0].security_code;
  securityCodeElement.update({
    settings: securityCodeSettings
  });
}

async function updateIssuer(paymentMethod, bin) {
  const {
    additional_info_needed,
    issuer
  } = paymentMethod;
  let issuerOptions = [issuer];

  if (additional_info_needed.includes('issuer_id')) {
    issuerOptions = await getIssuers(paymentMethod, bin);
  }

  createSelectOptions(issuerElement, issuerOptions);
}

async function getIssuers(paymentMethod, bin) {
  try {
    const {
      id: paymentMethodId
    } = paymentMethod;
    return await mp.getIssuers({
      paymentMethodId,
      bin
    });
  } catch (e) {
    console.error('error getting issuers: ', e)
  }
};

async function updateInstallments(paymentMethod, bin) {
  try {
    const installments = await mp.getInstallments({
      amount: document.getElementById('transactionAmount').value,
      bin,
      paymentTypeId: 'credit_card'
    });
    const installmentOptions = installments[0].payer_costs;
    const installmentOptionsKeys = {
      label: 'recommended_message',
      value: 'installments'
    };
    createSelectOptions(installmentsElement, installmentOptions, installmentOptionsKeys);
  } catch (error) {
    console.error('error getting installments: ', e)
  }
}

const formElement = document.getElementById('form-checkout');
formElement.addEventListener('submit', createCardToken);

async function createCardToken(event) {
  try {
    const tokenElement = document.getElementById('token');
    if (!tokenElement.value) {
      event.preventDefault();
      const token = await mp.fields.createCardToken({
        cardholderName: document.getElementById('form-checkout__cardholderName').value,
        identificationType: document.getElementById('form-checkout__identificationType').value,
        identificationNumber: document.getElementById('form-checkout__identificationNumber').value,
      });
      tokenElement.value = token.id;
      formElement.requestSubmit();
    }
  } catch (e) {
    console.error('error creating card token: ', e)
  }
}

function createSelectOptions(elem, options, labelsAndKeys = { label : "name", value : "id"}){
  const {label, value} = labelsAndKeys;

  elem.options.length = 0;

  const tempOptions = document.createDocumentFragment();

  options.forEach( option => {
      const optValue = option[value];
      const optLabel = option[label];

      const opt = document.createElement('option');
      opt.value = optValue;
      opt.textContent = optLabel;

      tempOptions.appendChild(opt);
  });

  elem.appendChild(tempOptions);
}

// Get Identification Types
(async function getIdentificationTypes () {
  try {
      const identificationTypes = await mp.getIdentificationTypes();
      const docTypeElement = document.getElementById('docType');

      createSelectOptions(docTypeElement, identificationTypes)
  }catch(e) {
      return console.error('Error getting identificationTypes: ', e);
  }
})()