if (id_start_date.value == '') {
    id_start_date.setAttribute('readonly', '');
}
if (id_end_date.value == '') {
    id_end_date.setAttribute('readonly', '');
}

let d2 = document.getElementById('id_debtor_name_2');
let d3 = document.getElementById('id_debtor_name_3');
let ct_d2 = d2.parentElement.parentElement;
let ct_d3 = d3.parentElement.parentElement;

// initially hide account name 2, 3
d2.setAttribute('disabled', true);
ct_d2.style.display = 'none';
d3.setAttribute('disabled', true);
ct_d3.style.display = 'none';

//making d2 required
d2.setAttribute('required', 'true');
span = document.createElement('span');
span.classList.add('text-danger');
span.innerHTML = ' *';
d2.parentElement.parentElement.querySelector('label').append(span);

//creating amount subtext
let amtCont = document.createElement('div');
let amtSub = document.createElement('small');
amtSub.classList.add('form-text', 'text-muted');
amtCont.append(amtSub);
id_amount.after(amtCont);
amtCont.style.cssText = 'overflow:hidden;transition:all 0.3s';
amtCont.style.height = '0px';


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
    // console.log('(change) Target: ' + e.target.id);
    if (e.target.id == '') return;
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
        id_start_date.setAttribute('readonly', '');
        return;
    }
    if (e.target.checkValidity()) {
        id_start_date.setAttribute('min', id_date.value);
        id_start_date.removeAttribute('readonly');
        validIcon(id_start_date);
    }
}

id_start_date.addEventListener('change', startDateChange);
function startDateChange(e) {
    if (id_start_date.value == '') {
        console.log('inside if (start date value is null)');
        id_end_date.value = '';
        id_end_date.dispatchEvent(new Event('change', {bubbles: true}));
        id_end_date.setAttribute('readonly', '');
        return
    }
    
    if (e.target.checkValidity()) {
        id_end_date.setAttribute('min', id_start_date.value);
        
        let d = new Date(id_start_date.value);
        d.setFullYear(d.getFullYear() + 40);
        d.setDate(d.getDate() - 1);
        // console.log(d.toISOString().split('T')[0]);
        id_end_date.setAttribute('max', d.toISOString().split('T')[0]);

        id_end_date.removeAttribute('readonly');
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
        ct_d2.style.display = 'none';

        d3.setAttribute('disabled', true);
        ct_d3.style.display = 'none';
    };
}

function currency(str) {
	function comma(str) {
		if (str.length <= 2) return str;
		else return comma(str.slice(0, -2)) + ',' + str.slice(-2)
	}

	p = str.indexOf('.');
	if (p == -1) {
		return comma(str.slice(0, -1)) + str.slice(-1) + '.00';
	} else {
		return comma(str.slice(0, p-1)) + str.slice(p-1, p+1) + str.slice(p+1).padEnd(2, '0');
	}
}

id_amount.addEventListener('change', function(e) {
    if (e.target.value == '' || !e.target.checkValidity()) {
        amtSub.innerText = '';
        amtCont.style.height = 0;
        return;
    } 
    amtSub.innerText = '₹ ' + currency(e.target.value);
    let rect = amtSub.getBoundingClientRect();
    let compStyle = getComputedStyle(amtSub);
    amtCont.style.height = Number(compStyle.marginTop.slice(0, compStyle.marginTop.indexOf('px'))) + Number(compStyle.marginBottom.slice(0, compStyle.marginTop.indexOf('px'))) + rect.height + 'px';
});