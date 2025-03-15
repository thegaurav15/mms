let nav = document.getElementById('nav');

for (elem of nav.querySelectorAll('a')) {
    elem.setAttribute('href', elem.getAttribute('href') + (new URL(window.location.href)).search);
}