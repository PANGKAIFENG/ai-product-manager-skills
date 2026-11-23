(() => {
  const bar = document.getElementById('location-bar');
  const clear = () => {
    document.querySelectorAll('.located').forEach(element => element.classList.remove('located'));
    bar.hidden = true;
  };
  function reveal() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    for (let ancestor = target.parentElement; ancestor; ancestor = ancestor.parentElement) {
      if (ancestor instanceof HTMLDetailsElement) ancestor.open = true;
    }
    if (target instanceof HTMLDetailsElement) target.open = true;
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href^="#"]');
    if (!anchor) return;
    clear();
    if (anchor.hasAttribute('data-locate')) {
      const target = document.getElementById(anchor.hash.slice(1));
      target?.classList.add('located');
      document.getElementById('location-label').textContent = `定位记录 ${anchor.hash.slice(1)}`;
      document.getElementById('location-return').href = `#${anchor.dataset.return}`;
      bar.hidden = false;
    }
    if (anchor.hash === location.hash) reveal();
  });
  document.getElementById('clear-location').addEventListener('click', clear);
  document.addEventListener('keydown', event => { if (event.key === 'Escape') clear(); });
  addEventListener('hashchange', reveal);
  reveal();
})();
