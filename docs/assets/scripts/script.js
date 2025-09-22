//scrolling effect
window.addEventListener("scroll", function () {
    let navbar = document.getElementById("navbar");
    let scroll = this.scrollY;
    let nav = document.getElementById("nav");
    let header = document.getElementById("header");
    if (scroll > 300 && window.innerWidth > 768) {
        nav.style.height = "1em";
        nav.style.position = "fixed";
        nav.style.top = "0";
        nav.style.right = "0";
        header.style.justifyContent = "auto";
        navbar.style.display = "none";
        nav.addEventListener("mouseenter", function () {
            nav.style.height = "7em";
            navbar.style.display = "flex";
        });
        nav.addEventListener("mouseleave", function () {
            nav.style.height = "1em";
            navbar.style.display = "none";
        });
        let burger = document.getElementById("burger");
        let open_menu = 0;
        burger.addEventListener("click", function () {
            if (open_menu == 0) {
                navbar.style.display = "flex";
                open_menu = 1;
            } else {
                navbar.style.display = "none";
                open_menu = 0;
            }
        });
    } else if (scroll == 0 && window.innerWidth > 768) {
        nav.style.height = "7em";
        nav.style.position = "relative";
        nav.style.right = "0";
        header.style.justifyContent = "space-between";
        navbar.style.display = "flex";
        nav.addEventListener("mouseenter", function () {
            nav.style.height = "7em";
            navbar.style.display = "flex";
        });
        nav.addEventListener("mouseleave", function () {
            nav.style.height = "7em";
            navbar.style.display = "flex";
        });
    }
    //burger menu
    let burger = document.getElementById("burger");
    let open_menu = 0;
    if (window.innerWidth < 768) {
        burger.addEventListener("click", function () {
            if (open_menu == 0) {
                navbar.style.display = "flex";
                open_menu = 1;
            } else {
                navbar.style.display = "none";
                open_menu = 0;
            }
        });
    }
});