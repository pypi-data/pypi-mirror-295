/**
 * @typedef AttributeBinding
 * @property {string} attribute_name
 * @property {string} model_key
 */

/**
 * @typedef EventBinding
 * @property {string} event_name
 * @property {string[] | null} properties
 */

/**
 * @typedef BaseContext
 * @property {string} _tag_name
 * @property {string[]} _scripts
 * @property {string[]} _styles
 * @property {string} _max_height
 * @property {AttributeBinding[]} _attributes
 * @property {EventBinding[]} _events
 */

/** @typedef {BaseContext & Record<string, any>} Context */

/** @typedef {import("npm:@anywidget/types").AnyModel<Context>} Model */

/** @typedef {() => Element} MetadataElementFactory */

/**
 * Creates and inserts a metadata element in the document `<head>`
 *
 * @param {MetadataElementFactory} factory Element factory function
 * @returns {Promise<Element>}
 */
function insertMetadata(factory) {
  return new Promise((resolve, reject) => {
    const el = factory();
    el.addEventListener('load', () => resolve(el));
    el.addEventListener('error', reject);
    document.head.appendChild(el);
  });
}

/**
 * Creates and inserts a metadata element if it doesn't already exist
 *
 * @param {string} selector
 * @param {MetadataElementFactory} factory
 */
async function addMetadataOnce(selector, factory) {
  return document.querySelector(selector) ?? (await insertMetadata(factory));
}

/**
 * Add a `<script>` tag to the document `<head>`
 *
 * @param {string} url
 */
function addScriptOnce(url) {
  return addMetadataOnce(`script[src="${url}"]`, () => {
    const el = document.createElement('script');
    el.src = url;
    el.defer = true;
    return el;
  });
}

/**
 * Add a `<link>` tag to the document `<head>`
 *
 * @param {string} url
 */
function addStyleOnce(url) {
  return addMetadataOnce(`link[href="${url}"]`, () => {
    const el = document.createElement('link');
    el.href = url;
    el.rel = 'stylesheet';
    return el;
  });
}

/**@type {import("npm:@anywidget/types").Initialize<Context>} */
async function initialize({ model }) {
  const scripts = model.get('_scripts').map(addScriptOnce);
  const styles = model.get('_styles').map(addStyleOnce);
  await Promise.all([...scripts, ...styles]);
}

/**
 * Bind an attribute value
 *
 * @param {Model} model
 * @param {HTMLElement} instance
 * @param {AttributeBinding} binding
 */
function bindAttribute(model, instance, binding) {
  const { attribute_name, model_key } = binding;
  const update = () => {
    const value = model.get(model_key);
    if (value === null) {
      instance.removeAttribute(attribute_name);
    } else {
      const valueStr = typeof value === 'string' ? value : JSON.stringify(value);
      instance.setAttribute(attribute_name, valueStr);
    }
  };

  update();
  model.on(`change:${model_key}`, update);
}

/**
 * Add an event listener
 *
 * @param {Model} model
 * @param {HTMLElement} instance
 * @param {EventBinding} binding
 */
function bindEvent(model, instance, binding) {
  const { event_name, properties } = binding;
  instance.addEventListener(event_name, (e) => {
    const obj = /** @type {Record<string, any>} */ (e);
    const dataArray = (properties ?? ['detail']).map((prop) => obj[prop]);
    const data = dataArray?.length === 1 ? dataArray[0] : dataArray;
    model.send({ event: event_name, data });
  });
}

/**
 * Wait until the custom element is stable (i.e. rendering done, etc.)
 *
 * @param {HTMLElement} instance
 */
async function whenStable(instance) {
  await customElements.whenDefined(instance.localName);
  if ('whenStable' in instance && typeof instance.whenStable === 'function') {
    await instance.whenStable();
  }
}

/**
 * Wait until `durationMs` milliseconds have elapsed
 *
 * @param {number} durationMs
 */
async function timeout(durationMs) {
  await new Promise((resolve) => setTimeout(resolve, durationMs));
}

/** @type {import("npm:@anywidget/types").Render<Context>} */
async function render({ model, el }) {
  const tagName = model.get('_tag_name');
  const attributes = model.get('_attributes');
  const events = model.get('_events');
  const instance = document.createElement(tagName);

  attributes.forEach((binding) => bindAttribute(model, instance, binding));
  events.forEach((binding) => bindEvent(model, instance, binding));

  el.style.height = model.get('_max_height');
  el.style.maxHeight = model.get('_max_height');
  el.appendChild(instance);

  await Promise.race([whenStable(instance), timeout(750)]);
}

export default { initialize, render };
