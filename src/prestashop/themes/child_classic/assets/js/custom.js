document.addEventListener("DOMContentLoaded", function () {

    const headers = [
        { text: "Wyróżnione", url: "/bialko" },
        { text: "Białko", url: "/kawa" },
        { text: "Kreatyna", url: "/przekaski" },
        { text: "Zdrowie i kondycja", url: "/kreatyna" },
        { text: "Zdrowa żywność", url: "/aminokwasy" },
        { text: "Nowości", url: "/witaminy" }

    ];

    const productsContainer = document.querySelector(".products");

    if (!productsContainer) return;

    const products = productsContainer.querySelectorAll(".product");

    headers.forEach((header, index) => {

        let position = index * 6;

        if (products[position]) {
            const titleDiv = document.createElement("div");
            titleDiv.className = "category-header";
            titleDiv.innerHTML = `
                <a href="${header.url}">
                    ${header.text}
                </a>
            `;
            products[position].before(titleDiv);
        }
    });
});
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
