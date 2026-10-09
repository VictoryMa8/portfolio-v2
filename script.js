(() => {
  const root = document.documentElement;
  let theme = 'dark';
  root.dataset.theme = theme;

  document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById('theme-toggle');
    function update() {
      const dark = theme === 'dark';
      root.dataset.theme = theme;
      button.innerHTML = `<span>${dark ? '☼' : '☾'}</span><span>${dark ? 'light' : 'dark'}</span>`;
    }
    update();
    button.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      update();
    });
  });
})();
