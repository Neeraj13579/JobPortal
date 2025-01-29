let nav = document.getElementById('nav');

window.addEventListener("scroll", function() {
    if (window.scrollY >= 100)
        nav.style.backgroundColor = "rgba(10, 10, 10, 0.364)"; 
    else 
        nav.style.backgroundColor = "transparent";
});

const backgroundImages = [
    'static/img/img1.jpeg',
    'static/img/img2.jpg',
    'static/img/img3.jpg',
    'static/img/img4.jpg',
    'static/img/img5.jpg',
    'static/img/img6.jpg',
    'static/img/img7.jpg',
    'static/img/img8.jpg',
    'static/img/img9.jpg',
    'static/img/img10.jpg',
    'static/img/img11.jpg',
    'static/img/img12.jpg',
    'static/img/img13.jpg',
];

let heroImg = document.getElementById('hero-img');

setInterval(() => {
    let randomIndex = Math.floor(Math.random() * backgroundImages.length);
    let randomImageUrl = backgroundImages[randomIndex];

    heroImg.style.background = `url('${randomImageUrl}')`;
    heroImg.style.backgroundSize = 'cover';
    heroImg.style.backgroundRepeat = 'no-repeat';
    heroImg.style.backgroundPosition = 'center';
}, 3000);