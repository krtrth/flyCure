const header = document.querySelector(".site-header");
const navToggle = document.querySelector(".nav-toggle");
const heroTreatment = document.querySelector("#hero-treatment");
const heroCountry = document.querySelector("#hero-country");
const heroWhatsapp = document.querySelector("#hero-whatsapp");
const whatsappNumber =
  document.body?.dataset?.whatsapp ||
  heroWhatsapp?.href?.match(/wa\.me\/(\d+)/)?.[1] ||
  "919999999999";

function updateHeroWhatsappLink() {
  if (!heroTreatment || !heroWhatsapp) {
    return;
  }
  const treatment = heroTreatment.value;
  const country = (heroCountry?.value || "").trim() || "my country";
  const message = `Hi FlyCure, I need help with ${treatment} in India. I am contacting from ${country}. Please guide me on suitable hospitals and quotations.`;
  heroWhatsapp.href = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;
}

if (navToggle && header) {
  navToggle.addEventListener("click", () => {
    const isOpen = header.classList.toggle("nav-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

document.querySelectorAll(".site-nav a").forEach((link) => {
  link.addEventListener("click", () => {
    header?.classList.remove("nav-open");
    navToggle?.setAttribute("aria-expanded", "false");
  });
});

[heroTreatment, heroCountry].forEach((control) => {
  control?.addEventListener("input", updateHeroWhatsappLink);
});

updateHeroWhatsappLink();
