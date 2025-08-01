import {pdf_init, selectPage, sel} from './pdf_image.mjs';
export {container};

let container = document.getElementById('preview-container');
let input = document.getElementById('id_mandate_image');
let form = input.form;
let uncropped;
let cropper = null;
let croppedCanvas = null;
container.style.height = '0px';

let message = {
    initial: "Mandate image is not uploaded, upload it here:",
    pdf: "Please select the page that contains the mandate image.",
    crop: "Crop the image properly such that <b>only the mandate</b> is present in the final image.",
    final: "This is the final image that will be uploaded to NPCI and sent to the Debtor Bank."
}

input.setAttribute('accept', 'application/pdf, image/*');

function initCropper() {
    container.append(uncropped);
    container.style.display = 'block';
    container.style.height = '';
    guideMessage.innerHTML = message.crop;

    resetBtn.style.display = 'inline-block';
    rotateBtn.style.display = 'inline-flex';
    cropBtn.style.display = 'inline-block';
    originalBtn.style.display = 'inline-block';
    submitBtn.style.display = 'none';

    let params = {
        viewMode: 2,
        responsive: false,
        dragMode: 'move',
        cropBoxMovable: false,
        toggleDragModeOnDblclick: false
    }
    cropper = new Cropper(uncropped, params);
    loadingModal.style.display = 'none';
}

function formReset() {
    if (document.getElementById('pdfThumbnail')) {
        document.getElementById('pdfThumbnail').remove();
    }
    if (cropper) {
        if (cropper.ready) {
            cropper.destroy();
        }
    }
    if (document.getElementById('previewImg')) {
        document.getElementById('previewImg').remove();
    }
    if (croppedCanvas) {
        if (croppedCanvas.parentElement) {croppedCanvas.remove();}
    }
    
    guideMessage.innerHTML = message.initial

    pdfButtons.style.display = 'none';
    resetBtn.style.display = 'none';
    rotateBtn.style.display = 'none';
    cropBtn.style.display = 'none';
    originalBtn.style.display = 'none';
    submitBtn.style.display = 'none';
    container.style.display = 'none';
    container.style.height = '0px';
    input.parentElement.style.display = '';
}

cropBtn.onclick = function() {
    croppedCanvas = cropper.getCroppedCanvas();
    croppedCanvas.style.cssText = "width:100%;object-fit:contain;object-position: 50% 50%;border: solid lightgrey 4px";
    cropper.destroy();
    uncropped.remove();

    guideMessage.innerHTML = message.final;
    container.style.display = 'none';
    form.before(croppedCanvas);
    rotateBtn.style.display = 'none';
    cropBtn.style.display = 'none';
    originalBtn.style.display = 'none';
    submitBtn.style.display = 'inline-block';
}

originalBtn.onclick = function() {
    cropper.destroy();
    form.before(uncropped);
    
    guideMessage.innerHTML = message.final;
    uncropped.style.cssText = "width:100%;object-fit:contain;object-position: 50% 50%;border: solid lightgrey 4px";
    container.style.display = 'none';
    rotateBtn.style.display = 'none';
    cropBtn.style.display = 'none';
    originalBtn.style.display = 'none';
    submitBtn.style.display = 'inline-block';
}

function centerCanvas(cropper, ratio) {
    cropper.clear();
    let ctnrData = cropper.getContainerData();
    let cnvsData = cropper.getCanvasData();
    if (cnvsData.height > ctnrData.height) {
        cropper.setCanvasData({height: ctnrData.height});
        cropper.setCanvasData({left: ctnrData.width/2 - cropper.getCanvasData().width/2});
    }
    else {
        cropper.setCanvasData({width: ctnrData.width});
        cropper.setCanvasData({top: ctnrData.height/2 - cropper.getCanvasData().height/2});
    }

    let c = cropper.getCanvasData();
    let obj = {
        left: c.left + c.width * (1 - ratio)/2,
        top: c.top + c.height * (1 - ratio)/2,
        width: c.width * ratio,
        height: c.height * ratio
    }

    cropper.crop();
    cropper.setCropBoxData(obj);
}

rotateLeft.onclick = function() {
    cropper.rotate(-90);
    centerCanvas(cropper, 0.8);
}

rotateRight.onclick = function() {
    cropper.rotate(90);
    centerCanvas(cropper, 0.8);
}

fitWidth.onclick = function() {
    cropper.setCanvasData({
        width: cropper.getContainerData().width,
        left: 0,
        top: cropper.getCropBoxData().top
    });
}

fitCanvas.onclick = function() {
    centerCanvas(cropper, 0.8);
}

async function uploadForm(formData) {
    let response = await fetch(form.getAttribute('action'), {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        let result = await response.text();
        // alert('Image uploaded successfully.\n' + result);
        window.location.reload();
    } else {
        alert("HTTP-Error: " + response.status);
    }
}

submitBtn.onclick = async function() {
    if (!confirm('This mandate will be submitted. Click OK to proceed.')) {
        return;
    }
    
    loadingModal.style.display = 'grid';
    let formData = new FormData(form);

    if (form.previousSibling == uncropped) {
        
        if (uncropped.tagName == 'IMG') {
            uploadForm(formData);
        } else if (uncropped.tagName == 'CANVAS') {
            uncropped.toBlob(function(blob) {
                formData.set("mandate_image", blob, ref.innerText + "_pdf_uncropped.png");
                uploadForm(formData);
            }, 'image/png');
        }
    }

    else if (form.previousSibling == croppedCanvas) {
        //upload cropped image
        croppedCanvas.toBlob(function(blob) {
            formData.set("mandate_image", blob, ref.innerText + "_cropped.png");
            uploadForm(formData);
        }, 'image/png');
    }

    else {
        alert('Some error has occured, please reload the page and try again.');
        window.location.reload();
    }
}

input.addEventListener('change', checkFile);
form.addEventListener('reset', formReset);

function checkFile(e) {
    loadingModal.style.display = 'grid';
    console.log(e.target.files[0].type);
    input.parentElement.style.display = 'none';
    if (e.target.files[0].type.startsWith('image/')) {
        uncropped = document.createElement('img');
        uncropped.setAttribute('id', 'previewImg');
        uncropped.style.cssText = ("width:100%;object-fit:contain;object-position: 50% 50%");
        uncropped.src = URL.createObjectURL(input.files[0]);
        initCropper(uncropped);
    } else if (e.target.files[0].type == 'application/pdf') {
        startPdf(e.target.files[0]);
        pdfButtons.style.display = 'inline-block';
        resetBtn.style.display = 'inline-block';
    }
}

async function startPdf(file) {
    file.arrayBuffer().then(
        async function(file_arrayBuffer) {
            try {
                container.style.display = 'block';
                await pdf_init(file_arrayBuffer);
                guideMessage.innerHTML = message.pdf;
            } catch (err) {
                alert(err);
                input.value = '';
            }
        },
        function (err) {
            alert('err');
            input.value = '';
        }
    );
}

sel.addEventListener('click', async function() {
    loadingModal.style.display = 'grid';
    pdfButtons.style.display = 'none';
    document.getElementById('pdfThumbnail').remove();
    uncropped = await selectPage();
    uncropped.setAttribute('id', 'previewImg');
    uncropped.style.cssText = ("width:100%;object-fit:contain;object-position: 50% 50%");
    initCropper(uncropped);
})