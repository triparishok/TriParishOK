(() => {
  document.querySelectorAll('[data-advent-invitation]').forEach((feature) => {
    const full = feature.querySelector('[data-advent-full]');
    const compact = feature.querySelector('.advent-compact');
    const controls = feature.querySelector('.advent-controls');
    const expand = feature.querySelector('[data-advent-expand]');
    const minimize = feature.querySelector('[data-advent-minimize]');
    const heading = feature.getAttribute('aria-labelledby');
    const key = 'triparish:invitation:' + feature.dataset.seasonKey;
    const setCollapsed = (collapsed, moveFocus = false) => {
      full.hidden = collapsed;
      compact.hidden = !collapsed;
      expand.setAttribute('aria-expanded', String(!collapsed));
      minimize.setAttribute('aria-expanded', String(!collapsed));
      feature.setAttribute('aria-labelledby', collapsed ? compact.querySelector('h2').id : heading);
      if (moveFocus) (collapsed ? expand : minimize).focus();
    };
    let seen = false;
    try {
      seen = localStorage.getItem(key) === 'seen';
      localStorage.setItem(key, 'seen');
    } catch (_) {
      // The invitation remains usable when browser storage is unavailable.
    }
    controls.hidden = false;
    // Preserve direct links into the invitation even on a return visit.
    const target = document.getElementById(location.hash.slice(1));
    setCollapsed(seen && !(target && full.contains(target)));
    expand.addEventListener('click', () => setCollapsed(false, true));
    minimize.addEventListener('click', () => setCollapsed(true, true));
    window.addEventListener('hashchange', () => {
      const target = document.getElementById(location.hash.slice(1));
      if (target && full.contains(target)) setCollapsed(false);
    });
  });
})();
