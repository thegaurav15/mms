let { pdfjsLib } = globalThis;

let overlay = document.getElementById('overlay');
overlay.style.display = 'none';

let prev = document.getElementById('prev');
let next = document.getElementById('next');
let sel = document.getElementById('sel');

async function getDoc(pdf) {
    let doc_promise = pdfjsLib.getDocument(pdf).promise;
    let doc = await doc_promise;
    return doc;
};

async function pageRender(doc, page_num, dim) {
    let page = await doc.getPage(page_num);
    let viewport = page.getViewport({ scale: 1 });
    let new_scale = null;
    if (dim.height/dim.width > viewport.height/viewport.width) {
        new_scale = dim.width/viewport.width;
    } else {
        new_scale = dim.height/viewport.height;
    }
    viewport = page.getViewport({ scale: new_scale });
    let canvas = document.createElement('canvas');
    const ctx = canvas.getContext("2d");
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    const renderContext = {
        canvasContext: ctx,
        viewport: viewport
    };
    page.render(renderContext);
    return canvas
}

function clearElem(elem) {
    for (let child of elem.querySelectorAll('canvas')) child.remove();
}

let currentPage = 1;
let dim = {
    height: 400,
    width: 300
};
let thumbContainer = document.getElementById('thumb-container');
let doc;

async function pdf_init(file) {
    overlay.style.display = '';
    doc = await getDoc(file);
    console.log(doc.numPages);
    showPage(1);
}

async function showPage(page_num) {
    clearElem(thumbContainer);
    let canvas = await pageRender(doc, page_num, dim);
    thumbContainer.append(canvas);
    sel.innerHTML = `Select (${page_num})`;
    overlay.style.display = 'none';
}

let input = document.getElementById('input');
input.addEventListener('change', async function(){
    let file = input.files[0];
    overlay.style.display = '';
    file.arrayBuffer().then(function(file_arrayBuffer){
        pdf_init(file_arrayBuffer);
    });
});

prev.addEventListener('click', prevPage);
next.addEventListener('click', nextPage);

function prevPage() {
    if (currentPage == 1) return;
    overlay.style.display = '';
    currentPage--;
    setTimeout(showPage, 0, currentPage);
}

function nextPage() {
    if (currentPage == doc.numPages) return;
    overlay.style.display = '';
    currentPage++;
    setTimeout(showPage, 0, currentPage);
}