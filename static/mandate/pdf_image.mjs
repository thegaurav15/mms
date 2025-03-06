import '../pdfjs/pdf.min.mjs';
let { pdfjsLib } = globalThis;
pdfjsLib.GlobalWorkerOptions.workerSrc = '/static/pdfjs/pdf.worker.min.mjs';
import { container } from './image_upload.js';

let prev = document.getElementById('prev');
let next = document.getElementById('next');
let sel = document.getElementById('sel');

let currentPage = 1;
let defaultDim = {
    height: 600,
    width: 792
};
let doc;

async function pdf_init(file) {
    let doc_promise = pdfjsLib.getDocument(file).promise;
    try {
        doc = await doc_promise;
    } catch (err) {
        throw err;
    }
    
    console.log(doc.numPages);
    // container = ctnr;
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
    // canvas.style.border = '1px solid lightgrey';
    const renderContext = {
        canvasContext: ctx,
        viewport: viewport
    };
    await page.render(renderContext).promise;
    return canvas
}

async function showPage(page_num, dim = defaultDim) {
    let canvas = await pageRender(page_num, dim);
    if (container.querySelector('#pdfThumbnail')) {
        container.querySelector('#pdfThumbnail').replaceWith(canvas);
    } else {
        container.append(canvas);
    }
    canvas.setAttribute('id', 'pdfThumbnail');
    sel.innerHTML = `Select (${page_num}/${doc.numPages})`;
    let rect = canvas.getBoundingClientRect();
    container.style.height = rect.height + 'px';
    loadingModal.style.display = 'none';
}

prev.addEventListener('click', prevPage);
next.addEventListener('click', nextPage);

function prevPage() {
    if (!doc) return;
    if (currentPage == 1) return;
    loadingModal.style.display = 'grid';
    let p = currentPage - 1;
    setTimeout(showPage, 0, p);
    currentPage = p;
}

function nextPage() {
    if (!doc) return;
    if (currentPage == doc.numPages) return;
    loadingModal.style.display = 'grid';
    let p = currentPage + 1;
    setTimeout(showPage, 0, p);
    currentPage = p;
}

async function selectPage() {
    let canvas = await pageRender(currentPage, {height: 1800, width: 1800});
    return canvas;
}

export {pdf_init, selectPage, sel};