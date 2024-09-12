/**
 * @typedef Context
 * @property {string | null} width
 * @property {string | null} height
 * @property {string | null} url
 * @property {DataView | null} data
 */

/** @typedef {import("npm:@anywidget/types").AnyModel<Context>} Model */

const SCRIPT_URL = 'https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js';

/** @type {import("npm:@anywidget/types").Initialize<Context>} */
async function initialize() {
  const script = document.querySelector(`script[src="${SCRIPT_URL}"]`);
  if (!script) {
    await new Promise((resolve, reject) => {
      const el = document.createElement('script');
      el.src = SCRIPT_URL;
      el.type = 'module';
      el.addEventListener('load', resolve);
      el.addEventListener('error', reject);
      document.head.appendChild(el);
    });
  }
}

/**
 * Updates the value of a style property.
 * Removes the style if the value is null.
 *
 * @param {HTMLElement} el
 * @param {string} property
 * @param {unknown} value
 */
function updateStyle(el, property, value) {
  if (typeof value === 'string') {
    el.style.setProperty(property, value);
  } else {
    el.style.removeProperty(property);
  }
}

/**
 * Binds a css property on an element
 *
 * @param {Model} model
 * @param {HTMLElement} el
 * @param {string} property
 * @param {keyof Context} key
 */
function bindStyleProperty(model, el, property, key) {
  updateStyle(el, property, model.get(key));
  model.on(`change:${key}`, () => updateStyle(el, property, model.get(key)));
}

/**
 * Updates the src attribute using either src or data from the model
 *
 * @param {Model} model
 * @param {HTMLElement} viewerEl
 */
function updateSrc(model, viewerEl) {
  const prev = viewerEl.getAttribute('src');
  if (prev) {
    URL.revokeObjectURL(prev);
  }

  const src = model.get('url');
  const data = model.get('data');
  if (src) {
    viewerEl.setAttribute('src', src);
  } else if (data) {
    const url = URL.createObjectURL(new Blob([data]));
    viewerEl.setAttribute('src', url);
  } else {
    viewerEl.removeAttribute('src');
  }
}

/** @type {import("npm:@anywidget/types").Render<Context>} */
async function render({ model, el }) {
  const containerEl = document.createElement('div');
  containerEl.classList.add('model-viewer-container');

  bindStyleProperty(model, containerEl, '--model-viewer-width', 'width');
  bindStyleProperty(model, containerEl, '--model-viewer-height', 'height');

  const viewerEl = document.createElement('model-viewer');
  viewerEl.classList.add('model-viewer');
  viewerEl.setAttribute('camera-controls', '');

  const boundUpdateSrc = updateSrc.bind(null, model, viewerEl);
  boundUpdateSrc();
  model.on('change:src', boundUpdateSrc);
  model.on('change:data', boundUpdateSrc);

  await new Promise((resolve, reject) => {
    viewerEl.addEventListener('load', resolve);
    viewerEl.addEventListener('error', reject);
    containerEl.appendChild(viewerEl);
    el.appendChild(containerEl);
  });
}

export default { initialize, render };
