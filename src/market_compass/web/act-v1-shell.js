(() => {
  const links = [...document.querySelectorAll('[data-act-shell-room]')];
  const targets = links.map((link) => document.querySelector(link.getAttribute('href'))).filter(Boolean);

  const select = (id) => {
    links.forEach((link) => {
      const active = link.getAttribute('href') === `#${id}`;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
  };

  links.forEach((link) => link.addEventListener('click', () => select(link.getAttribute('href').slice(1))));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) select(visible.target.id);
    }, { rootMargin: '-15% 0px -70%', threshold: [0, .2, .6] });
    targets.forEach((target) => observer.observe(target));
  }
})();
