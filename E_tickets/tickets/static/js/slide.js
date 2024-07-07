var currentIndex = 0;
var slides = document.querySelectorAll('#slides-image .image-text');
var totalslides = slides.length;
var prevbutton = document.getElementById('prevButton');
var nextbutton = document.getElementById('nextButton');

function showslides(index) {
    for (var i = 0; i < totalslides; i++) {   // cette fonction permet de passer d'une image a une autre par incrementation
        slides[i].style.display = 'none';
        slides[i].style.animation = 'none';
    }
    slides[index].style.display = 'block';
    slides[index].style.animation = 'myapparition 2s ease-in 1 reverse';
}

function nextslides() {  // cette fontion permet de passer à l'image suivante automatique et manuellement
    currentIndex++;
    if (currentIndex >= totalslides) {
        currentIndex = 0;
    }
    showslides(currentIndex);
}
function preslides() {  // cette fontion permet de passer à l'image précedente manuellement
    currentIndex--;
    if (currentIndex < 0) {
        currentIndex = totalslides - 1;
    }
    showslides(currentIndex);
}
showslides(currentIndex);
setInterval(nextslides,8000);

nextButton.addEventListener('click', nextslides); // ici j'ai appelé la fonction pour les bouttons en y ajoutant un événément.
prevButton.addEventListener('click', preslides);

var pro = document.querySelectorAll('div .professionnels');
var par = document.querySelectorAll('div .particuliers');
function pro_par() {
    pro.style.background = '#fff';
}

par.addEventListener('click', pro_par);