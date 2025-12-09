
document.addEventListener("DOMContentLoaded", function () {

    const products = document.querySelectorAll(".product-miniature");

    products.forEach(product => {
        const quickView = product.querySelector(".highlighted-informations");
        const price = product.querySelector(".product-price-and-shipping");

        if (quickView && price) {

            price.insertAdjacentElement("afterend", quickView);
        }
    });
});
window.addEventListener('scroll', function () {
    const headerTop = document.querySelector('.header-top');
    const scrollY = window.scrollY;

    if (!headerTop.nextElementSibling || !headerTop.nextElementSibling.classList.contains('header-placeholder')) {
        const placeholder = document.createElement('div');
        placeholder.className = 'header-placeholder';
        placeholder.style.height = headerTop.offsetHeight + 'px';
        placeholder.style.display = 'none';
        headerTop.after(placeholder);
    }

    const placeholder = headerTop.nextElementSibling;

    if (scrollY > 90) {
        headerTop.classList.add('fixed');
        placeholder.style.display = 'block';
    } else {
        headerTop.classList.remove('fixed');
        placeholder.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('#_desktop_top_menu.menu.js-top-menu.position-static>ul.top-menu>li');

    menuItems.forEach(item => {
        let hideTimeout;
        const submenu = item.querySelector('.sub-menu');

        if (!submenu) return;


        item.addEventListener('mouseenter', function () {
            clearTimeout(hideTimeout);
            submenu.style.display = 'block';
        });


        item.addEventListener('mouseleave', function () {
            hideTimeout = setTimeout(() => {
                submenu.style.display = 'none';
            }, 800);
        });


        submenu.addEventListener('mouseenter', function () {
            clearTimeout(hideTimeout);
            submenu.style.display = 'block';
        });


        submenu.addEventListener('mouseleave', function () {
            hideTimeout = setTimeout(() => {
                submenu.style.display = 'none';
            }, 800);
        });
    });
});
