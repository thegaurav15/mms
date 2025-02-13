id_start_date.setAttribute('disabled', '');
id_end_date.setAttribute('disabled', '');
let d2 = document.getElementById('id_debtor_name_2');
let d3 = document.getElementById('id_debtor_name_3');
let ct_d2 = d2.parentElement.parentElement;
let ct_d3 = d3.parentElement.parentElement;

// initially hide account name 2, 3
d2.setAttribute('disabled', true);
ct_d2.style.display = 'none';
d3.setAttribute('disabled', true);
ct_d3.style.display = 'none';
d2.setAttribute('required', 'true');

function validIcon(elem) {
    if (elem.value == '') {
        resetValidIcon(elem);
        return;
    }
    let elem_y = document.getElementById(elem.id + '_y');
    let elem_n = document.getElementById(elem.id + '_n');
    if (elem.checkValidity()) {
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

function resetValidIcon(elem) {
    let elem_y = document.getElementById(elem.id + '_y');
    let elem_n = document.getElementById(elem.id + '_n');
    if (!elem_n.classList.contains('d-none')) {
        elem_n.classList.add('d-none');
    }
    if (!elem_y.classList.contains('d-none')) {
        elem_y.classList.add('d-none');
    }
}

form.addEventListener('change', function(e) {
    // console.log(e.target.id);
    if (e.target.name == 'debtor_joint') {
        jointToggle(e.target.checked);
        return;
    }
    validIcon(e.target);
});

id_date.addEventListener('change', dateChange);
function dateChange(e) {
    if (id_date.value == '') {
        id_start_date.value = '';
        id_start_date.dispatchEvent(new Event('change', {bubbles: true}));
        id_start_date.setAttribute('disabled', '');
        return;
    }
    if (e.target.checkValidity()) {
        id_start_date.setAttribute('min', id_date.value);
        id_start_date.removeAttribute('disabled');
        validIcon(id_start_date);
    }
}

id_start_date.addEventListener('change', startDateChange);
function startDateChange(e) {
    if (id_start_date.value == '') {
        console.log('inside if (start date value is null)');
        id_end_date.value = '';
        id_end_date.dispatchEvent(new Event('change', {bubbles: true}));
        id_end_date.setAttribute('disabled', '');
        return
    }
    
    if (e.target.checkValidity()) {
        id_end_date.setAttribute('min', id_start_date.value);
        
        let d = new Date(id_start_date.value);
        d.setFullYear(d.getFullYear() + 40);
        d.setDate(d.getDate() - 1);
        // console.log(d.toISOString().split('T')[0]);
        id_end_date.setAttribute('max', d.toISOString().split('T')[0]);

        id_end_date.removeAttribute('disabled');
        validIcon(id_end_date);
    }
}

id_debtor_acc_ifsc.addEventListener('change', function() {
    this.value = this.value.toUpperCase();
});

id_credit_account.addEventListener('change', function() {
    this.value = this.value.toUpperCase();
});

function jointToggle(checked) {
    if(checked) {
        d2.removeAttribute('disabled');
        ct_d2.style.display = '';
        d3.removeAttribute('disabled');
        ct_d3.style.display = '';
    } else {
        d2.setAttribute('disabled', true);
        d2.value = '';
        d2.dispatchEvent(new Event('change', {bubbles: true}));
        ct_d2.style.display = 'none';

        d3.setAttribute('disabled', true);
        d3.value = '';
        ct_d3.style.display = 'none';
        d3.dispatchEvent(new Event('change', {bubbles: true}));
    };
}