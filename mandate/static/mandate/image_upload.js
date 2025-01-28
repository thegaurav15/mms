let id = document.currentScript.getAttribute('id');
console.log(id);
let container = document.getElementById('preview-container');
let input = document.getElementById('id_mandate_image');
let form = input.form;
let img = document.createElement('img');
img.setAttribute('id', 'previewImg');
img.style.cssText = ("width:100%;object-fit:contain;object-position: 50% 50%");
let cropper = null;
let canvas = null;

function changePreview(event) {
    img.src = URL.createObjectURL(input.files[0]);

    if (cropper) {
        if (cropper.ready) {
            cropper.destroy();
        }
    }
    if (document.getElementById('previewImg')) {
        document.getElementById('previewImg').remove();
    }

    if (canvas) {
        if (canvas.parentElement) {canvas.remove();}
    }
    submitBtn.style.display = 'none';
    
    container.append(img);
    cropper = new Cropper(img, {viewMode: 2, responsive: false, dragMode: 'move', cropBoxMovable: false, toggleDragModeOnDblclick: false});

    container.style.display = 'block';
    resetBtn.style.display = 'inline-block';
    rotateBtn.style.display = 'inline-flex';
    cropBtn.style.display = 'inline-block';
    originalBtn.style.display = 'inline-block';

    input.parentElement.style.display = 'none';
}

function formReset() {
    if (cropper) {
        if (cropper.ready) {
            cropper.destroy();
        }
    }
    if (document.getElementById('previewImg')) {
        document.getElementById('previewImg').remove();
    }
    if (canvas) {
        if (canvas.parentElement) {canvas.remove();}
    }
    
    resetBtn.style.display = 'none';
    rotateBtn.style.display = 'none';
    cropBtn.style.display = 'none';
    originalBtn.style.display = 'none';
    submitBtn.style.display = 'none';
    container.style.display = 'none';
    input.parentElement.style.display = '';
}

cropBtn.onclick = function() {
    canvas = cropper.getCroppedCanvas();
    canvas.style.cssText = "width:100%;object-fit:contain;object-position: 50% 50%;border: solid lightgrey 4px";
    cropper.destroy();
    img.remove();
    container.style.display = 'none';
    form.before(canvas);
    rotateBtn.style.display = 'none';
    cropBtn.style.display = 'none';
    originalBtn.style.display = 'none';
    submitBtn.style.display = 'inline-block';
}

originalBtn.onclick = function() {
    cropper.destroy();
    form.before(img);
    img.style.cssText = "width:100%;object-fit:contain;object-position: 50% 50%;border: solid lightgrey 4px";
    container.style.display = 'none';
    rotateBtn.style.display = 'none';
    cropBtn.style.display = 'none';
    originalBtn.style.display = 'none';
    submitBtn.style.display = 'inline-block';
}

function centerCanvas(cropper, ratio) {
    cropper.clear();
    ctnrData = cropper.getContainerData();
    cnvsData = cropper.getCanvasData();
    if (cnvsData.height > ctnrData.height) {
        cropper.setCanvasData({height: ctnrData.height});
        cropper.setCanvasData({left: ctnrData.width/2 - cropper.getCanvasData().width/2});
    }
    else {
        cropper.setCanvasData({width: ctnrData.width});
        cropper.setCanvasData({top: ctnrData.height/2 - cropper.getCanvasData().height/2});
    }

    c = cropper.getCanvasData();
    obj = {
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
    let response = await fetch('/mandates/mandate/' + id + '/', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        let result = await response.text();
        alert('Image uploaded successfully.\n' + result);
        window.location.reload();
    } else {
        alert("HTTP-Error: " + response.status);
    }
}

submitBtn.onclick = async function() {
    loadingModal.style.display = 'grid';
    let formData = new FormData(form);

    if (form.previousSibling == img) {
        //upload original image
        uploadForm(formData);
    }

    else if (form.previousSibling == canvas) {
        //upload cropped image
        canvas.toBlob(function(blob) {
            formData.set("mandate_image", blob, ('000000'+id).slice(-6) + "_cropped.png");
            uploadForm(formData);
        }, 'image/png');
    }

    else {
        alert('Some error has occured, please reload the page and try again.');
        window.location.reload();
    }
}

input.addEventListener('change', changePreview);
form.addEventListener('reset', formReset);
