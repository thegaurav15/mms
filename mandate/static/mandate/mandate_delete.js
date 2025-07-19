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

function changeDeleteInProgress(elem) {
    elem.classList.add('disabled');
}

function resetDeleteInProgress(elem) {
    elem.classList.remove('disabled');
}

function markRowDeleted(elem) {
    elem.previousElementSibling.remove();
    elem.closest('tr').classList.add('text-muted');
    elem.classList.add('disabled');
    elem.innerText = 'Deleted!';
}

async function callDelete(e) {
    let id = e.target.getAttribute("dataId");
    console.log("delete called on " + id);
    // change button to disabled
    changeDeleteInProgress(e.target)

    let url = '/mandates/mandate/' + id + '/delete_mandate/'
    let deleteReqOptions = {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }
    let response = await fetch(url, deleteReqOptions);
    let responseText = await response.text();

    if (response.ok) {
        // alert(responseText);
        markRowDeleted(e.target);
    } else {
        alert('Error: ' + responseText);
        resetDeleteInProgress(e.target);
    }
}

for (elem of document.getElementsByClassName("deleteButton")) {
    elem.addEventListener('click', async function deleteAfterConfirm(e) {
        if (confirm('Mandate will be deleted. Are you sure?')) {
            callDelete(e);
        }
    });
};