// @ts-nocheck
// Warning: Please do not adjust this script in any other place than the upstream repo template
//
// Renders a PlantUML diagram to SVG without Java, a browser or a server:
//
//     quarto run render.ts < diagram.puml > diagram.svg
//
// It runs the official PlantUML engine compiled to JavaScript (@plantuml/core,
// MIT licence, with Graphviz as WebAssembly) on the Deno runtime that ships
// with Quarto. The engine is written for browsers, so this script provides the
// little it needs from one: an SVG element tree, a serialiser and a way to
// measure text (from a table of font widths, see font_metrics.json).
//
// The engine (about 9 MB) is not part of the repository. It is downloaded once
// into vendor/, in the pinned version below, and checked against its SHA-256
// sum before it is used.

import { createRequire } from "node:module";

const VERSION = "1.2026.6";
const FILES = [
  { name: "plantuml.js", local: "plantuml.js", sha256: "87b8c74c1b9520ee659f4d2c8de16ae19c9f21365856a53d0766a8fa602b24d8" },
  { name: "viz-global.js", local: "viz-global.cjs", sha256: "fc6ca2de83dd4e3fca967d5214122777890a5cd1ab101115a1f716fc84e6dc5e" },
];
const SOURCES = [
  `https://cdn.jsdelivr.net/npm/@plantuml/core@${VERSION}/`,
  `https://unpkg.com/@plantuml/core@${VERSION}/`,
];
// Text is measured with the widths of Helvetica, so it is drawn with a font of
// the same widths wherever the diagram is shown.
const FONT_FAMILY = "Arial, Helvetica, 'Nimbus Sans', 'Liberation Sans', Arimo, sans-serif";

const here = new URL(".", import.meta.url);
const vendor = new URL(`vendor/${VERSION}/`, here);

function fail(message) {
  console.error(`PlantUML: ${message}`);
  Deno.exit(1);
}

// -----------------------------------------------------------------------------
// The engine: download once, verify always
// -----------------------------------------------------------------------------

async function sha256(bytes) {
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function download(file) {
  const errors = [];
  for (const source of SOURCES) {
    try {
      const response = await fetch(source + file.name);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const bytes = new Uint8Array(await response.arrayBuffer());
      if (await sha256(bytes) !== file.sha256) throw new Error("unexpected SHA-256 sum");
      return bytes;
    } catch (e) {
      errors.push(`${source}${file.name}: ${e.message}`);
    }
  }
  fail(`could not download the engine.\n  ${errors.join("\n  ")}`);
}

async function engineFile(file) {
  const target = new URL(file.local, vendor);
  try {
    if (await sha256(await Deno.readFile(target)) === file.sha256) return target;
  } catch (_) {
    // not downloaded yet
  }
  const bytes = await download(file);
  await Deno.mkdir(vendor, { recursive: true });
  const temporary = new URL(`${file.local}.${Deno.pid}.tmp`, vendor);
  await Deno.writeFile(temporary, bytes);
  await Deno.rename(temporary, target);
  return target;
}

// -----------------------------------------------------------------------------
// What the engine needs from a browser
// -----------------------------------------------------------------------------

const metrics = JSON.parse(await Deno.readTextFile(new URL("font_metrics.json", here)));

// Width of a text in pixels. `font` is a CSS font shorthand ("bold 14px Arial").
function textWidth(text, size, font) {
  const description = String(font).toLowerCase();
  if (/mono|courier/.test(description)) return [...text].length * metrics.monospace * size / 1000;
  const table = /bold|[6-9]00/.test(description) ? metrics.bold : metrics.regular;
  let width = 0;
  for (const char of text) {
    // Accented letters are as wide as their base letter.
    width += table[char] ?? table[char.normalize("NFD")[0]] ?? metrics.default;
  }
  return width * size / 1000;
}

function fontSize(font) {
  const match = /([\d.]+)px/.exec(String(font));
  return match ? parseFloat(match[1]) : 14;
}

function escapeXml(text, quotes) {
  let result = String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  if (quotes) result = result.replace(/"/g, "&quot;");
  return result;
}

class TextNode {
  constructor(data) {
    this.nodeType = 3;
    this.data = String(data);
    this.parentNode = null;
  }
  get textContent() { return this.data; }
  set textContent(value) { this.data = String(value); }
  serialize() { return escapeXml(this.data, false); }
}

class Element {
  constructor(namespace, name) {
    this.nodeType = 1;
    this.namespaceURI = namespace;
    this.tagName = name;
    this.nodeName = name;
    this.localName = name;
    this.attributes = new Map();
    this.childNodes = [];
    this.parentNode = null;
    this.style = {};
  }
  setAttribute(name, value) { this.attributes.set(name, String(value)); }
  setAttributeNS(_namespace, name, value) { this.attributes.set(name, String(value)); }
  getAttribute(name) { return this.attributes.has(name) ? this.attributes.get(name) : null; }
  hasAttribute(name) { return this.attributes.has(name); }
  removeAttribute(name) { this.attributes.delete(name); }
  appendChild(child) {
    if (child.parentNode) child.parentNode.removeChild(child);
    child.parentNode = this;
    this.childNodes.push(child);
    return child;
  }
  insertBefore(child, reference) {
    if (reference == null) return this.appendChild(child);
    if (child.parentNode) child.parentNode.removeChild(child);
    child.parentNode = this;
    this.childNodes.splice(this.childNodes.indexOf(reference), 0, child);
    return child;
  }
  removeChild(child) {
    const index = this.childNodes.indexOf(child);
    if (index >= 0) this.childNodes.splice(index, 1);
    child.parentNode = null;
    return child;
  }
  get children() { return this.childNodes.filter((node) => node.nodeType === 1); }
  get firstChild() { return this.childNodes[0] ?? null; }
  get lastChild() { return this.childNodes[this.childNodes.length - 1] ?? null; }
  get textContent() { return this.childNodes.map((node) => node.textContent).join(""); }
  set textContent(value) {
    this.childNodes = [];
    if (value != null && value !== "") this.appendChild(new TextNode(value));
  }
  get innerHTML() { return this.childNodes.map((node) => node.serialize()).join(""); }
  get outerHTML() { return this.serialize(); }
  querySelector() { return null; }
  // Only text is ever measured this way.
  getBBox() {
    const size = parseFloat(this.getAttribute("font-size") ?? "14");
    const font = `${this.getAttribute("font-weight") ?? ""} ${this.getAttribute("font-family") ?? ""}`;
    return { x: 0, y: -metrics.ascent * size, width: textWidth(this.textContent, size, font), height: (metrics.ascent + metrics.descent) * size };
  }
  serialize() {
    let attributes = "";
    if (this.tagName === "svg" && this.parentNode == null && !this.attributes.has("xmlns")) {
      attributes += ` xmlns="${this.namespaceURI}"`;
    }
    for (const [name, value] of this.attributes) attributes += ` ${name}="${escapeXml(value, true)}"`;
    const style = Object.entries(this.style).map(([key, value]) => `${key}:${value}`).join(";");
    if (style && !this.attributes.has("style")) attributes += ` style="${escapeXml(style, true)}"`;
    if (this.childNodes.length === 0) return `<${this.tagName}${attributes}/>`;
    return `<${this.tagName}${attributes}>${this.childNodes.map((node) => node.serialize()).join("")}</${this.tagName}>`;
  }
}

class Canvas {
  getContext() {
    return {
      font: "14px sans-serif",
      measureText(text) {
        const size = fontSize(this.font);
        return {
          width: textWidth(text, size, this.font),
          actualBoundingBoxAscent: metrics.ascent * size,
          actualBoundingBoxDescent: metrics.descent * size,
          fontBoundingBoxAscent: metrics.ascent * size,
          fontBoundingBoxDescent: metrics.descent * size,
        };
      },
    };
  }
}

function installBrowser() {
  const body = new Element("http://www.w3.org/1999/xhtml", "body");
  const head = new Element("http://www.w3.org/1999/xhtml", "head");
  globalThis.window = globalThis;
  globalThis.document = {
    body,
    head,
    createElementNS: (namespace, name) => new Element(namespace, name),
    createElement: (name) => name === "canvas" ? new Canvas() : new Element("http://www.w3.org/1999/xhtml", name),
    createTextNode: (data) => new TextNode(data),
    getElementById: () => null,
    importNode: (node) => node,
  };
  globalThis.XMLSerializer = class {
    serializeToString(node) { return node.serialize(); }
  };
  // Sprites and embedded SVG images are parsed by the browser; they are left out here.
  globalThis.DOMParser = class {
    parseFromString() { return { documentElement: null }; }
  };
}

// -----------------------------------------------------------------------------
// Rendering
// -----------------------------------------------------------------------------

function withDefaults(source) {
  const lines = source.replace(/\r\n?/g, "\n").split("\n");
  while (lines.length && lines[0].trim() === "") lines.shift();
  while (lines.length && lines[lines.length - 1].trim() === "") lines.pop();
  if (!lines.length) fail("the diagram is empty");
  if (!/^@start/.test(lines[0].trim())) {
    lines.unshift("@startuml");
    lines.push("@enduml");
  }
  return lines;
}

const source = await new Response(Deno.stdin.readable).text();
const lines = withDefaults(source);

const [enginePath, vizPath] = await Promise.all(FILES.map(engineFile));

// The engine reports its progress with console.log; standard output is the SVG.
const debug = Deno.env.get("PLANTUML_DEBUG");
console.log = debug ? console.error : () => {};

// Graphviz first: it must not mistake this process for a browser.
globalThis.Viz = createRequire(import.meta.url)(vizPath.pathname);
installBrowser();
const { renderToString } = await import(enginePath.href);

const svg = await new Promise((resolve, reject) => {
  const timeout = setTimeout(() => reject(new Error("no result after 120 seconds")), 120000);
  const done = (callback) => (value) => { clearTimeout(timeout); callback(value); };
  try {
    renderToString(lines, done(resolve), done((message) => reject(new Error(String(message)))));
  } catch (e) {
    done(reject)(e);
  }
}).catch((e) => fail(e.message));

if (!/^\s*<svg[\s>]/.test(svg)) fail(`unexpected output: ${String(svg).slice(0, 200)}`);

// Draw the text with a font of the widths it was measured with.
const output = svg.replace(/font-family="(sans-serif|SansSerif|Dialog)"/g, `font-family="${FONT_FAMILY}"`);

await Deno.stdout.write(new TextEncoder().encode(output + "\n"));
Deno.exit(0);
