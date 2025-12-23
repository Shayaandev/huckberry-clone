async function loadProducts() {
    try {
        const response = await fetch("/products");
        const products = await response.json();

        const productsDiv = document.getElementById("products");
        productsDiv.innerHTML = ""; // clear existing content

        products.forEach(product => {
            const productCard = document.createElement("div");
            productCard.classList.add("product-card");
            productCard.innerHTML = `
                <img src="${product.image_url}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p>$${product.price.toFixed(2)}</p>
                <button onclick="addToCart(${product.id})">Add to Cart</button>
            `;
            productsDiv.appendChild(productCard);
        });

    } catch (error) {
        console.error("Error loading products:", error);
    }
}
