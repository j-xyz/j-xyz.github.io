(() => {
  const card = document.querySelector('.field-note');
  if (!card) return;
  const art = card.querySelector('.hearth-art');
  const layer = card.querySelector('.field-note-network');
  const lines = layer.querySelector('.field-note-network-lines');
  const path = lines.querySelector('path');
  const nodes = lines.querySelector('.field-note-network-nodes');
  const fade = layer.querySelectorAll('#field-note-fade stop');

  function draw() {
    const bounds = layer.getBoundingClientRect();
    const illustration = art.getBoundingClientRect();
    const width = bounds.width;
    const height = bounds.height;
    const scale = illustration.width / 400;
    const left = illustration.left - bounds.left;
    const top = illustration.top - bounds.top;
    // Fade before the copy rather than at a fixed percentage of the card: the
    // illustration/text proportions change substantially between breakpoints.
    const artBottom = illustration.bottom - bounds.top;
    const copyTop = card.querySelector('.note-label').getBoundingClientRect().top - bounds.top - 8;
    fade[1].setAttribute('offset', artBottom / height);
    fade[2].setAttribute('offset', copyTop / height);
    card.style.setProperty('--field-note-art-bottom', `${artBottom}px`);
    card.style.setProperty('--field-note-copy-top', `${copyTop}px`);
    const anchor = (x, y) => [left + x * scale, top + y * scale];
    // These anchors match only the outer network in hearth.svg. Keeping the
    // bridge in a separate layer preserves the original illustration at any size.
    const points = [
      anchor(28, 101), anchor(85, 44), anchor(166, 27), anchor(329, 36),
      anchor(374, 108), anchor(375, 256), anchor(306, 296), anchor(213, 310),
      anchor(114, 291), anchor(35, 251),
      [-8, height * .08], [width * .3, -8], [width * .75, -6], [width + 8, height * .13],
      [-7, height * .37], [width + 8, height * .4], [width * .13, height * .53],
      [width * .75, height * .55], [width * .48, height * .65], [-8, height * .73],
      [width + 6, height * .72], [width * .2, height * .86], [width * .77, height * .91],
      [width * .43, height + 9], [-5, height + 5], [width + 5, height + 6],
    ];
    const edges = [
      [0, 10], [1, 10], [1, 11], [2, 11], [2, 12], [3, 12], [3, 13], [4, 13],
      [5, 15], [9, 14], [8, 16], [9, 16], [6, 17], [7, 16], [7, 17], [14, 16],
      [15, 17], [16, 17], [16, 18], [17, 18], [16, 19], [17, 20], [18, 19],
      [18, 20], [18, 21], [18, 22], [19, 21], [20, 22], [21, 22], [21, 23],
      [22, 23], [21, 24], [22, 25], [23, 24], [23, 25],
    ];
    layer.setAttribute('viewBox', `0 0 ${width} ${height}`);
    path.setAttribute('d', edges.map(([from, to]) => `M${points[from].join(' ')}L${points[to].join(' ')}`).join(' '));
    path.setAttribute('stroke-width', scale);
    nodes.replaceChildren(...points.slice(10).map(([x, y]) => {
      const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      circle.setAttribute('cx', x);
      circle.setAttribute('cy', y);
      circle.setAttribute('r', 4 * scale);
      circle.setAttribute('stroke-width', 2 * scale);
      return circle;
    }));
  }

  draw();
  if ('ResizeObserver' in window) new ResizeObserver(draw).observe(card);
  else window.addEventListener('resize', draw);
})();
