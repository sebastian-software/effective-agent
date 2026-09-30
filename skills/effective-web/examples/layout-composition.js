const controls = document.querySelector('.demo-controls');
const products = document.querySelector('#products');
const originals = [...products.children].map((card) => card.cloneNode(true));
const options = document.querySelector('#options');
const optionOriginals = [...options.children].map((option) => option.cloneNode(true));

function updateExamples() {
  const width = document.querySelector('#region-width').value;
  document.documentElement.style.setProperty('--demo-width', `${width}px`);
  document.querySelector('#width-value').value = `${width} px`;
  document.documentElement.style.fontSize = `${document.querySelector('#font-size').value}px`;
  // Keep the test controls in the page's language direction; vary the examples.
  for (const region of document.querySelectorAll('.demo-host')) {
    region.dir = document.querySelector('#direction').value;
  }
  const count = Number(document.querySelector('#item-count').value);
  const withMedia = document.querySelector('#show-media').checked;
  products.replaceChildren(...Array.from({ length: count }, (_, index) => {
    const card = originals[index % originals.length].cloneNode(true);
    if (!withMedia) card.querySelector('.product-media').remove();
    return card;
  }));
  products.hidden = count === 0;
  document.querySelector('#empty-products').hidden = count !== 0;
  options.replaceChildren(...Array.from({ length: count }, (_, index) =>
    optionOriginals[index % optionOriginals.length].cloneNode(true)));
  options.hidden = count === 0;
  document.querySelector('#empty-options').hidden = count !== 0;
}

controls.addEventListener('input', updateExamples);
controls.addEventListener('change', updateExamples);
controls.addEventListener('submit', (event) => event.preventDefault());
document.querySelector('#order-preview').addEventListener('submit', (event) => {
  event.preventDefault();
  document.querySelector('#preview-result').value = 'Vorschau erstellt. Es wurden keine Daten versendet.';
});
updateExamples();
