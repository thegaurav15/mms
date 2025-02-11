import '../pdfjs/pdf.min.mjs';
let { pdfjsLib } = globalThis;
pdfjsLib.GlobalWorkerOptions.workerSrc = '/static/pdfjs/pdf.worker.min.mjs';

let prev = document.getElementById('prev');
let next = document.getElementById('next');
let sel = document.getElementById('sel');

let currentPage = 1;
let dim = {
    height: 600,
    width: 792
};
let doc;
let container;

async function pdf_init(file, ctnr) {
    let doc_promise = pdfjsLib.getDocument(file).promise;
    try {
        doc = await doc_promise;
    } catch (err) {
        throw err;
    }
    
    console.log(doc.numPages);
    container = ctnr;
    currentPage = 1;
    showPage(currentPage);
}

async function pageRender(page_num, dim) {
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

async function showPage(page_num) {
    let canvas = await pageRender(page_num, dim);
    if (container.hasChildNodes()) {
        container.firstElementChild.replaceWith(canvas);
    } else {
        container.append(canvas);
    }
    container.style.height = canvas.height + 'px';
}

prev.addEventListener('click', prevPage);
next.addEventListener('click', nextPage);

function prevPage() {
    if (!doc) return;
    if (currentPage == 1) return;
    let p = currentPage - 1;
    setTimeout(showPage, 0, p);
    currentPage = p;
}

function nextPage() {
    if (!doc) return;
    if (currentPage == doc.numPages) return;
    let p = currentPage + 1;
    setTimeout(showPage, 0, p);
    currentPage = p;
}

export {pdf_init}