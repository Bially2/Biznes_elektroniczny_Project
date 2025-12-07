
document.addEventListener("DOMContentLoaded", function () {
    // Pobieramy wszystkie produkty
    const products = document.querySelectorAll(".product-miniature");

    products.forEach(product => {
        const quickView = product.querySelector(".highlighted-informations");
        const price = product.querySelector(".product-price-and-shipping");

        if (quickView && price) {
            // Przenosimy szybki podgląd bezpośrednio pod cenę
            price.insertAdjacentElement("afterend", quickView);
        }
    });
});
window.addEventListener('scroll', function () {
    const headerTop = document.querySelector('.header-top');
    const scrollY = window.scrollY;

    // jeśli nie ma placeholdera, tworzymy go
    if (!headerTop.nextElementSibling || !headerTop.nextElementSibling.classList.contains('header-placeholder')) {
        const placeholder = document.createElement('div');
        placeholder.className = 'header-placeholder';
        placeholder.style.height = headerTop.offsetHeight + 'px';
        placeholder.style.display = 'none'; // domyślnie ukryty
        headerTop.after(placeholder);
    }

    const placeholder = headerTop.nextElementSibling;

    if (scrollY > 90) {
        headerTop.classList.add('fixed');
        placeholder.style.display = 'block'; // wstawiamy przestrzeń
    } else {
        headerTop.classList.remove('fixed');
        placeholder.style.display = 'none';
    }
});
