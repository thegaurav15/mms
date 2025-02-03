function validIcon(e) {
    let elem_y = document.getElementById(e.target.id + '_y');
    let elem_n = document.getElementById(e.target.id + '_n');
    if (e.target.checkValidity()) {
        // valid form control/field
        if (!elem_n.classList.contains('d-none')) {
            elem_n.classList.add('d-none');
        }
        if (elem_y.classList.contains('d-none')) {
            elem_y.classList.remove('d-none');
        }
    }
    else {
        // invalid form control
        if (!elem_y.classList.contains('d-none')) {
            elem_y.classList.add('d-none');
        }
        if (elem_n.classList.contains('d-none')) {
            elem_n.classList.remove('d-none');
        }
    }
}

form.addEventListener('change', validIcon);