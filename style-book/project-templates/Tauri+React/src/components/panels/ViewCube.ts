import * as THREE from "three";
import type { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

/** Face labels, in the order +X, -X, +Y, -Y, +Z, -Z (BoxGeometry's face order). */
export interface ViewCubeLabels {
  right: string;
  left: string;
  top: string;
  bottom: string;
  front: string;
  back: string;
  home: string;
  hint: string;
}

const SIZE = 1; // the cube spans -0.5 … 0.5
const BAND = 0.17; // edge and corner zones, measured from each side
const TURN_MS = 400;

/**
 * A view cube in the top-right corner of a 3D view, as in Revit or AutoCAD.
 * It turns with the camera; a click on a face, edge or corner turns the
 * camera to that view around the orbit target, at the same distance. The
 * home button returns to the starting view. Colours follow the 0.4 tokens.
 */
export class ViewCube {
  readonly element: HTMLDivElement;
  private renderer: THREE.WebGLRenderer;
  private scene = new THREE.Scene();
  private camera = new THREE.OrthographicCamera(-0.95, 0.95, 0.95, -0.95, 0.1, 10);
  private cube: THREE.Mesh;
  private edges: THREE.LineSegments;
  private highlight: THREE.Mesh;
  private raycaster = new THREE.Raycaster();
  private home: THREE.Vector3;
  private homeDistance: number;
  private turn: { from: THREE.Vector3; rotation: THREE.Quaternion; distance: number; start: number } | null = null;
  private labels: ViewCubeLabels;
  private homeButton: HTMLButtonElement;

  constructor(
    private view: THREE.PerspectiveCamera,
    private controls: OrbitControls,
    labels: ViewCubeLabels,
    homeIcon: string,
  ) {
    this.labels = labels;
    this.home = view.position.clone().sub(controls.target).normalize();
    this.homeDistance = view.position.distanceTo(controls.target);

    this.element = document.createElement("div");
    this.element.className = "view-cube";
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.domElement.className = "view-cube-canvas";
    this.element.appendChild(this.renderer.domElement);

    this.homeButton = document.createElement("button");
    this.homeButton.type = "button";
    this.homeButton.className = "view-cube-home";
    this.homeButton.innerHTML = homeIcon;
    this.homeButton.addEventListener("click", () => this.turnTo(this.home, this.homeDistance));
    this.element.appendChild(this.homeButton);

    this.cube = new THREE.Mesh(new THREE.BoxGeometry(SIZE, SIZE, SIZE), []);
    this.scene.add(this.cube);
    this.edges = new THREE.LineSegments(new THREE.EdgesGeometry(this.cube.geometry), new THREE.LineBasicMaterial());
    this.scene.add(this.edges);
    this.highlight = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ transparent: true, opacity: 0.45, depthWrite: false }));
    this.highlight.visible = false;
    this.scene.add(this.highlight);

    const canvas = this.renderer.domElement;
    canvas.addEventListener("pointermove", (e) => this.hover(this.zoneAt(e)));
    canvas.addEventListener("pointerleave", () => this.hover(null));
    canvas.addEventListener("click", (e) => {
      const zone = this.zoneAt(e);
      if (zone) this.turnTo(zone);
    });

    this.setLabels(labels);
  }

  /** Redraws the faces in the current theme and language. */
  setLabels(labels: ViewCubeLabels) {
    this.labels = labels;
    this.element.title = labels.hint;
    this.renderer.domElement.setAttribute("aria-label", labels.hint);
    this.homeButton.title = labels.home;
    this.homeButton.setAttribute("aria-label", labels.home);
    this.applyTheme();
  }

  applyTheme() {
    const token = (name: string) => getComputedStyle(document.documentElement).getPropertyValue(name).trim() || "#808080";
    const { right, left, top, bottom, front, back } = this.labels;
    const old = this.cube.material as THREE.MeshBasicMaterial[];
    this.cube.material = [right, left, top, bottom, front, back].map((label) => new THREE.MeshBasicMaterial({ map: this.face(label, token) }));
    old.forEach((m) => {
      m.map?.dispose();
      m.dispose();
    });
    (this.edges.material as THREE.LineBasicMaterial).color.set(token("--oa-border-strong"));
    (this.highlight.material as THREE.MeshBasicMaterial).color.set(token("--oa-accent"));
  }

  private face(label: string, token: (name: string) => string) {
    const canvas = document.createElement("canvas");
    canvas.width = canvas.height = 256;
    const g = canvas.getContext("2d")!;
    g.fillStyle = token("--oa-raised");
    g.fillRect(0, 0, 256, 256);
    g.strokeStyle = token("--oa-border");
    g.lineWidth = 6;
    g.strokeRect(BAND * 256, BAND * 256, (1 - 2 * BAND) * 256, (1 - 2 * BAND) * 256);
    g.fillStyle = token("--oa-text");
    g.textAlign = "center";
    g.textBaseline = "middle";
    let size = 48;
    g.font = `600 ${size}px Inter, sans-serif`;
    while (g.measureText(label).width > 200 && size > 24) g.font = `600 ${(size -= 2)}px Inter, sans-serif`;
    g.fillText(label.toUpperCase(), 128, 132);
    const texture = new THREE.CanvasTexture(canvas);
    texture.colorSpace = THREE.SRGBColorSpace;
    texture.anisotropy = 4;
    return texture;
  }

  /** The face, edge or corner under the pointer, as a direction with components -1, 0 or 1. */
  private zoneAt(e: PointerEvent | MouseEvent): THREE.Vector3 | null {
    const rect = this.renderer.domElement.getBoundingClientRect();
    const pointer = new THREE.Vector2(((e.clientX - rect.left) / rect.width) * 2 - 1, -((e.clientY - rect.top) / rect.height) * 2 + 1);
    this.raycaster.setFromCamera(pointer, this.camera);
    const hit = this.raycaster.intersectObject(this.cube)[0];
    if (!hit) return null;
    const zone = (v: number) => (Math.abs(v) > SIZE / 2 - BAND ? Math.sign(v) : 0);
    return new THREE.Vector3(zone(hit.point.x), zone(hit.point.y), zone(hit.point.z));
  }

  private hover(zone: THREE.Vector3 | null) {
    this.renderer.domElement.style.cursor = zone ? "pointer" : "";
    this.highlight.visible = !!zone;
    if (!zone) return;
    const lip = 0.02;
    const axis = (d: number) => ({
      size: d === 0 ? SIZE - 2 * BAND : BAND + lip,
      centre: d === 0 ? 0 : d * (SIZE / 2 - BAND / 2 + lip / 2),
    });
    const [x, y, z] = [axis(zone.x), axis(zone.y), axis(zone.z)];
    this.highlight.scale.set(x.size, y.size, z.size);
    this.highlight.position.set(x.centre, y.centre, z.centre);
  }

  /** Turns the camera to look from `direction` at the orbit target. */
  turnTo(direction: THREE.Vector3, distance = this.view.position.distanceTo(this.controls.target)) {
    const to = direction.clone().normalize();
    // Straight down or up has no "up"; a hair towards the front keeps Front at the bottom of the screen.
    if (Math.abs(to.y) > 0.999) to.set(0, Math.sign(to.y), 0.001).normalize();
    const from = this.view.position.clone().sub(this.controls.target).normalize();
    this.turn = { from, rotation: new THREE.Quaternion().setFromUnitVectors(from, to), distance, start: performance.now() };
  }

  /** Call once per frame, before rendering the main view. */
  update(width = 110, height = 110) {
    if (this.turn) {
      const t = Math.min(1, (performance.now() - this.turn.start) / TURN_MS);
      const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      const step = new THREE.Quaternion().slerp(this.turn.rotation, eased);
      const startDistance = this.view.position.distanceTo(this.controls.target);
      const distance = startDistance + (this.turn.distance - startDistance) * eased;
      this.view.position.copy(this.controls.target).add(this.turn.from.clone().applyQuaternion(step).multiplyScalar(distance));
      this.view.lookAt(this.controls.target);
      if (t === 1) this.turn = null;
    }
    const size = this.renderer.getSize(new THREE.Vector2());
    if (size.x !== width || size.y !== height) this.renderer.setSize(width, height);
    const eye = this.view.position.clone().sub(this.controls.target).normalize().multiplyScalar(3);
    this.camera.position.copy(eye);
    this.camera.up.copy(this.view.up);
    this.camera.lookAt(0, 0, 0);
    this.renderer.render(this.scene, this.camera);
  }

  dispose() {
    (this.cube.material as THREE.MeshBasicMaterial[]).forEach((m) => {
      m.map?.dispose();
      m.dispose();
    });
    this.cube.geometry.dispose();
    this.edges.geometry.dispose();
    this.highlight.geometry.dispose();
    this.renderer.dispose();
    this.element.remove();
  }
}
