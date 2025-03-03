let acc = '7801NG00864579';

modalMain = document.createElement('div');
modalMain.classList.add('modal-main');
document.body.append(modalMain);

modalContainer = document.createElement('div');
modalContainer.classList.add('modal-container');
modalMain.append(modalContainer);

modalBody = document.createElement('div');
modalBody.classList.add('modal-body');
modalContainer.append(modalBody);

modalButtons = document.createElement('div');
modalButtons.classList.add('modal-body');
modalContainer.append(modalButtons);

let req = await fetch(`http://127.0.0.1:8001/mandates/create/checkacc/?account=${acc}`);
if (req.ok) {
    let table_html = await req.text();
    modalBody.innerHTML = table_html;
}