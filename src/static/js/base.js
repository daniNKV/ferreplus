window.onscroll = function() {
    var navbar = document.getElementById('navbar');
    if (window.scrollY > 0) {
        navbar.classList.add('fixed');
        navbar.classList.add('inset-0');
        navbar.classList.add('h-16');
    }
};