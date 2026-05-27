const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const searchInput = document.querySelector("#site-search");
const specialtyFilter = document.querySelector("#specialty-filter");
const cityFilter = document.querySelector("#city-filter");
const resetButton = document.querySelector("#reset-filters");
const heroTreatment = document.querySelector("#hero-treatment");
const heroCountry = document.querySelector("#hero-country");
const heroWhatsapp = document.querySelector("#hero-whatsapp");

const filterableCards = Array.from(
  document.querySelectorAll(".treatment-card, .provider-card, .doctor-card, .package-row:not(.table-head)")
);

function normalize(value) {
  return value.trim().toLowerCase();
}

function applyFilters() {
  const query = normalize(searchInput.value);
  const specialty = specialtyFilter.value;
  const city = cityFilter.value;

  filterableCards.forEach((card) => {
    const text = normalize(card.textContent);
    const cardSpecialty = card.dataset.specialty || "";
    const cardCity = card.dataset.city || "all";
    const matchesQuery = !query || text.includes(query);
    const matchesSpecialty = specialty === "all" || cardSpecialty === specialty;
    const matchesCity = city === "all" || cardCity === city || !card.dataset.city;

    card.classList.toggle("is-hidden", !(matchesQuery && matchesSpecialty && matchesCity));
  });
}

function updateHeroWhatsappLink() {
  const treatment = heroTreatment.value;
  const country = heroCountry.value.trim() || "my country";
  const message = `Hi FlyCure, I need help with ${treatment} in India. I am contacting from ${country}. Please guide me on suitable hospitals and quotations.`;
  heroWhatsapp.href = `https://wa.me/919999999999?text=${encodeURIComponent(message)}`;
}

navToggle.addEventListener("click", () => {
  const isOpen = header.classList.toggle("nav-open");
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

document.querySelectorAll(".site-nav a").forEach((link) => {
  link.addEventListener("click", () => {
    header.classList.remove("nav-open");
    navToggle.setAttribute("aria-expanded", "false");
  });
});

[searchInput, specialtyFilter, cityFilter].forEach((control) => {
  control.addEventListener("input", applyFilters);
});

resetButton.addEventListener("click", () => {
  searchInput.value = "";
  specialtyFilter.value = "all";
  cityFilter.value = "all";
  applyFilters();
});

[heroTreatment, heroCountry].forEach((control) => {
  control.addEventListener("input", updateHeroWhatsappLink);
});

updateHeroWhatsappLink();
