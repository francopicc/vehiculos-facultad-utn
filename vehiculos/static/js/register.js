// Estilizacion y configuracion del Form Registro

const formRegistro = document.querySelectorAll('.registroForm div')

formRegistro.forEach((item) => {
    item.classList.add("dato");
    if (item.classList.contains("termsAndButton")) {
        item.classList.remove("dato")
    }
})

document.getElementById("id_dateBirth").type = "date"

document.getElementById("id_surname").addEventListener('input', () => {
    const nombre = document.getElementById("id_name").value
    const apellido = document.getElementById("id_surname").value

    document.getElementById("namesurname").value = nombre + apellido
})