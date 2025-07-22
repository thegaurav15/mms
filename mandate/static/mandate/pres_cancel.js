var presentationId = null;

function getCookie(name) {
    let cookieValue = null
    
    if (!document.cookie || document.cookie == '') {
        return cookieValue;
    }

    let string = document.cookie;
    for (s of string.split(';')) {
        if (s.startsWith(name + '=')) {
            cookieValue = s.slice(s.indexOf('=') + 1);
        }
    }
    return cookieValue
}

function reqCancelModalShow(e) {
    modalMain = document.getElementById("cancelReqModalMain");
    document.getElementById('modalUmrn').innerText = e.target.getAttribute('dataUmrn');
    modalMain.style.display = 'grid';
    presentationId = e.target.getAttribute('dataId');
}

function hideModal() {
    document.getElementById('modalUmrn').innerText = '';
    presentationId = null;
    modalMain.style.display = 'none';
}

for (elem of document.getElementsByClassName('reqCancelButton')) {
    elem.addEventListener('click', reqCancelModalShow);
}

document.getElementById("cancelReqModalBack").addEventListener('click', hideModal);

// function for reqCancel
async function reqCancelPost(e) {
    let url = '/mandates/presentation/' + presentationId + '/cancel_request/';
    let options = {
        'method': "POST",
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }
    e.target.classList.add('disabled');
    let res = await fetch(url, options);
    let resText = await res.text();
    if (res.ok) {
        location.reload();
    } else {
        alert('There was some error. Please try again.');
        e.target.classList.remove('disabled');
    }
}

document.getElementById("cancelReqModalSubmit").addEventListener('click', reqCancelPost);

//function for marking cancelled
async function markCancelPost(e) {
    let idForMarkCancel = e.target.getAttribute('dataId');
    let url = '/mandates/presentation/' + idForMarkCancel + '/cancel_mark/';
    let options = {
        'method': "POST",
        'headers': {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }
    e.target.classList.add('disabled');
    let res = await fetch(url, options);
    let resText = await res.text();
    if (res.ok) {
        location.reload();
    } else {
        alert('There was some error. Please try again.');
        e.target.classList.remove('disabled');
    }
}

for (elem of document.getElementsByClassName('markCancelButton')) {
    elem.addEventListener('click', async function(e) {
        if (confirm('Mark Cancelled ONLY if you have cancelled this UMRN on NPCI portal. Proceed?')) {
            markCancelPost(e);
        }
    });
}