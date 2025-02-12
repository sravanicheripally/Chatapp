document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const leftMenu = document.querySelector(".left-menu");

    menuToggle.addEventListener("click", function () {
        leftMenu.classList.toggle("active");
    });

    function adjustPageSize() {
        let width = window.innerWidth;
        let scale = 1;

        if (width >= 992 && width <= 1600) {
            scale = 0.9;
        } else if (width >= 700 && width < 992) {
            scale = 0.8;
        } else if (width >= 600 && width < 700) {
            scale = 0.75;
        } else if (width < 600) {
            scale = 0.5;
        }

        document.body.style.transform = `scale(${scale})`;
        document.body.style.transformOrigin = "top left";
    }

    window.addEventListener("resize", adjustPageSize);
    adjustPageSize();
});
