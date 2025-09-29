const navbar = document.getElementById("navbar");
const nav = document.getElementById("nav");
const header = document.getElementById("header");
const burger = document.getElementById("burger");

if (window.innerWidth > 768) {
    // Scrolling effect
    const SCROLL_LIMIT = 300;
    window.addEventListener("scroll", function () {
        if (this.scrollY > SCROLL_LIMIT) {
            nav.style.height = "1em";
            nav.style.position = "fixed";
            nav.style.top = "0";
            nav.style.right = "0";
            header.style.justifyContent = "auto";
            navbar.style.display = "none";
        }
        else if (this.scrollY === 0) {
            nav.style.height = "7em";
            nav.style.position = "relative";
            nav.style.right = "0";
            header.style.justifyContent = "space-between";
            navbar.style.display = "flex";
        }
    });
    nav.addEventListener("mouseenter", function () {
        nav.style.height = "7em";
        navbar.style.display = "flex";
    });
    nav.addEventListener("mouseleave", function () {
        const scroll = window.scrollY;
        nav.style.height = scroll > SCROLL_LIMIT ? "1em" : "7em";
        navbar.style.display = scroll > SCROLL_LIMIT ? "none" : "flex";
    });
} else {
    // Burger menu
    burger.addEventListener("click", function () {
        navbar.style.display = navbar.style.display === "flex" ? "none" : "flex";
    });
}
