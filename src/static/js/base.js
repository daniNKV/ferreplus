document.addEventListener('DOMContentLoaded', (event) => {
    window.onscroll = () => {
        let navbar = document.getElementById('navbar');
        if (window.scrollY > 0) {
            navbar.classList.add('h-16')
            navbar.classList.remove('h-20');
    
        }
    };    
});


