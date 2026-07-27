(() => {
  const carousel = document.querySelector("[data-home-carousel]");
  if (!carousel) return;

  const slides = Array.from(carousel.querySelectorAll("[data-carousel-slide]"));
  const dots = Array.from(carousel.querySelectorAll("[data-carousel-dot]"));
  const previous = carousel.querySelector("[data-carousel-previous]");
  const next = carousel.querySelector("[data-carousel-next]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let current = 0;
  let timer;

  const show = (index) => {
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === current;
      slide.hidden = !active;
      slide.classList.toggle("is-active", active);
    });
    dots.forEach((dot, dotIndex) => {
      const active = dotIndex === current;
      dot.classList.toggle("is-active", active);
      if (active) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
  };

  const stop = () => window.clearInterval(timer);
  const start = () => {
    stop();
    if (!reduceMotion) timer = window.setInterval(() => show(current + 1), 6500);
  };

  previous?.addEventListener("click", () => {
    show(current - 1);
    start();
  });
  next?.addEventListener("click", () => {
    show(current + 1);
    start();
  });
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      show(index);
      start();
    });
  });
  carousel.addEventListener("mouseenter", stop);
  carousel.addEventListener("mouseleave", start);
  carousel.addEventListener("focusin", stop);
  carousel.addEventListener("focusout", start);

  show(0);
  start();
})();
