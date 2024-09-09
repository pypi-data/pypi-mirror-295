/*
    Copyright (c) 2021 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

import { LitElement, html } from "lit";
import { customElement, property } from "lit/decorators.js";

/**
 * Displays a PCB and BOM for assistance in assemblying.
 *
 * TODO: This should eventually just be KiCanvas, but it's not quite ready for
 * it yet.
 */
@customElement("winter-pcb-assembly")
export class WinterPCBAssemblyElement extends LitElement {
    private pcbData: any;
    private bom: BOM;
    private renderer: PCBRenderer;

    @property()
    src: string;

    @property({ type: Boolean })
    rotate: boolean;

    protected override createRenderRoot() {
        // TODO: For now, this renders to light DOM but should eventually use
        // shadow DOM.
        return this;
    }

    override connectedCallback(): void {
        super.connectedCallback();

        if (this.src) {
            this.loadSrc();
        }
    }

    protected async loadSrc() {
        const resp = await fetch(this.src, {
            mode: "same-origin",
        });

        if (!resp.ok) {
            console.error(
                `Could not fetch ${this.src}: ${resp.status} ${resp.statusText}`,
            );
        }

        this.pcbData = await resp.json();
        this.prepData();
        this.requestUpdate();
    }

    protected prepData() {
        this.bom = new BOM(this.pcbData);
        this.renderer = new PCBRenderer(this, this.pcbData, this.rotate);
    }

    protected override render() {
        if (!this.pcbData) {
            return html`<p>loading...</p>`;
        }
        return html`
            ${this.renderer.front.canvas}
            <winter-pcb-assembly-bom-table
                .renderer=${this.renderer}
                .items=${this.bom
                    .frontItemsGroupedByValue}></winter-pcb-assembly-bom-table>
            ${this.renderer.back.canvas}
            <winter-pcb-assembly-bom-table
                .renderer=${this.renderer}
                .items=${this.bom
                    .backItemsGroupedByValue}></winter-pcb-assembly-bom-table>
        `;
    }
}

@customElement("winter-pcb-assembly-bom-table")
export class WinterPCBAssemblyBOMTableElement extends LitElement {
    protected override createRenderRoot() {
        // TODO: For now, this renders to light DOM but should eventually use
        // shadow DOM.
        return this;
    }

    @property({ attribute: false })
    renderer: PCBRenderer;

    @property({ attribute: false })
    items: Map<string, BOMItem[]>;

    public override connectedCallback() {
        super.connectedCallback();

        this.addEventListener("click", (e: MouseEvent) => {
            const target = e.target as HTMLElement;
            const row = target.closest("tr");

            if (!row) {
                return;
            }

            const itemValue = row.dataset["bomItemValue"]!;
            const items = this.items.get(itemValue);

            if (!items) {
                return;
            }

            const refs = items.map((x) => x.ref);
            this.renderer.highlight(refs);

            for (const tr of this.querySelectorAll("tr[aria-selected]")) {
                tr.ariaSelected = null;
            }
            row.ariaSelected = "true";
        });
    }

    protected override render() {
        const rows = [];

        for (const [value, items] of this.items.entries()) {
            const refs = items.map((x) => x.ref).join(", ");
            rows.push(
                html`<tr data-bom-item-value=${value}>
                    <td>
                        ${html`<input
                            type="checkbox"
                            class="checkbox"
                            aria-label="Mark row ${rows.length +
                            1} complete" />`}
                    </td>
                    <td>${refs}</td>
                    <td>${value}</td>
                    <td>${items[0]?.rating}</td>
                </tr>`,
            );
        }

        return html`<table
            class="bom-table is-high-density"
            aria-label="Table of components">
            <thead>
                <tr>
                    <th aria-label="Completed"></th>
                    <th>References</th>
                    <th>Value</th>
                    <th>Rating</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>`;
    }
}

interface BOMItem {
    ref: string;
    value: string;
    footprint: string;
    rating: string;
    side: "front" | "back" | undefined;
}

interface PCBData {
    edges_bbox: any;
    drawings: any;
    footprints: PCBFootprint[];
    edges: PCBEdge[];
    bom: {
        B: any;
        F: any;
        both: any;
        fields: { [x: string]: any };
    };
}

class BOM {
    public frontItems: BOMItem[] = [];
    public backItems: BOMItem[] = [];
    public frontItemsGroupedByValue: Map<string, BOMItem[]> = new Map();
    public backItemsGroupedByValue: Map<string, BOMItem[]> = new Map();

    constructor(public pcbData: PCBData) {
        this.extract();
    }

    private extract() {
        const frontRefs = new Set<string>();

        for (const group of this.pcbData.bom.F) {
            for (const [ref, _] of group) {
                frontRefs.add(ref);
            }
        }

        for (const group of this.pcbData.bom.both) {
            for (const [ref, index] of group) {
                const fields = this.pcbData.bom.fields[index];
                const dstList = frontRefs.has(ref)
                    ? this.frontItems
                    : this.backItems;
                const dstMap = frontRefs.has(ref)
                    ? this.frontItemsGroupedByValue
                    : this.backItemsGroupedByValue;
                const item: BOMItem = {
                    ref: ref,
                    value: fields[0],
                    footprint: fields[1],
                    rating: fields[2],
                    side: frontRefs.has(ref) ? "front" : "back",
                };

                dstList.push(item);

                if (!dstMap.has(item.value)) {
                    dstMap.set(item.value, []);
                }
                dstMap.get(item.value)?.push(item);
            }
        }
    }
}

//////////////////////

export class PCBRenderer {
    public readonly scale = 10;
    public readonly colors: PCBColors = {
        edge_cuts: "#ff99ce",
        board: "#ffb9dd",
        pad: "gold",
        hole: "white",
        pin1: "#6bd280",
        silk: "black",
        highlight_stroke: "#7ce4f4",
        highlight_fill: "#7ce4f488",
    };
    public width: number;
    public height: number;
    public front: PCBDraw;
    public back: PCBDraw;
    public highlighted: Set<string> = new Set();

    constructor(
        public parent: HTMLElement,
        public pcbData: PCBData,
        public rotate: boolean = false,
    ) {
        this.width =
            this.pcbData.edges_bbox.maxx - this.pcbData.edges_bbox.minx;
        this.height =
            this.pcbData.edges_bbox.maxy - this.pcbData.edges_bbox.miny;

        if (this.rotate) {
            const height = this.height;
            this.height = this.width;
            this.width = height;
        }

        this.back = new PCBDraw(this.makeCanvas("back"), this.colors);
        this.front = new PCBDraw(this.makeCanvas("front"), this.colors);

        this.draw();
    }

    private makeCanvas(className: string, scale = 10) {
        const canvas = document.createElement("canvas");
        canvas.classList.add(className);
        canvas.width = this.width * window.devicePixelRatio * scale;
        canvas.height = this.height * window.devicePixelRatio * scale;
        canvas.dataset["scale"] = `${scale}`;
        return canvas;
    }

    public highlight(refs: string[]) {
        this.highlighted.clear();
        for (const ref of refs) {
            this.highlighted.add(ref);
        }
        this.draw();
    }

    /* Drawing */

    draw() {
        this.setTransforms(this.front.canvas);
        this.front.clear();
        this.front.items(this.pcbData.drawings.silkscreen.F, this.colors.silk);
        this.front.footprints(this.pcbData.footprints, "F", this.highlighted);
        this.front.items(this.pcbData.edges, this.colors.edge_cuts);

        this.setTransforms(this.back.canvas);
        this.back.clear();
        this.back.items(this.pcbData.drawings.silkscreen.B, this.colors.silk);
        this.back.footprints(this.pcbData.footprints, "B", this.highlighted);
        this.back.items(this.pcbData.edges, this.colors.edge_cuts);
    }

    setTransforms(canvas: HTMLCanvasElement) {
        var ctx = canvas.getContext("2d")!;
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(
            this.scale * window.devicePixelRatio,
            this.scale * window.devicePixelRatio,
        );
        if (this.rotate) {
            const x = this.width / 2;
            const y = this.height / 2;
            ctx.translate(x, y);
            ctx.rotate(deg2rad(90));
            ctx.translate(-y, -x);
        }
        ctx.translate(
            -this.pcbData.edges_bbox.minx,
            -this.pcbData.edges_bbox.miny,
        );
    }
}

/////////////////////

interface PCBColors {
    edge_cuts: string;
    board: string;
    pad: string;
    hole: string;
    pin1: string;
    silk: string;
    highlight_stroke: string;
    highlight_fill: string;
}

interface PCBItem {
    thickness: number;
    svgpath: string | Path2D | undefined;
    layer: string;
    path2d: Path2D;
    type: string | undefined;
    text: string;
}

interface PCBShape extends PCBItem {
    pos: [number, number];
    angle: number;
    filled: boolean;
    width: number;
}

interface PCBPolygon extends PCBShape {
    thickness: number;
    path2d: Path2D;
    polygons: [number, number][][];
}

interface PCBEdge extends PCBShape {
    start: [number, number];
    end: [number, number];
    radius: number;
    startangle: number;
    endangle: number;
    cpa: [number, number];
    cpb: [number, number];
}

interface PCBPad {
    layers: string;
    pin1: boolean;
    path2d: Path2D;
    polygons: [number, number][][];
    type: string;
    shape: string;
    pos: [number, number];
    angle: number;
    offset: [number, number];
    drillshape: string;
    drillsize: [number, number];
    size: [number, number];
    radius: number;
    chamfpos: number;
    chamfratio: number;
}

interface PCBFootprint {
    ref: string;
    drawings: PCBItem[];
    pads: PCBPad[];
    layer: string;
    bbox: {
        pos: [number, number];
        relpos: [number, number];
        size: [number, number];
        angle: number;
    };
}

class PCBDraw {
    public ctx: CanvasRenderingContext2D;

    constructor(
        public canvas: HTMLCanvasElement,
        public colors: PCBColors,
    ) {
        this.ctx = canvas.getContext("2d")!;
    }

    /* Public methods */

    public clear() {
        this.ctx.save();
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        this.ctx.fillStyle = this.colors.board;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.restore();
    }

    public footprints(
        footprints: PCBFootprint[],
        layer: string,
        highlighted: Set<string>,
    ) {
        const ctx = this.ctx;
        ctx.lineWidth = 1 / 4;

        for (let i = 0; i < footprints.length; i++) {
            const mod = footprints[i]!;
            this.footprint(layer, mod, highlighted.has(mod.ref));
        }
    }

    public items(items: PCBItem[], color: string) {
        for (const item of items) {
            this.item(item, color);
        }
    }

    /* Drawing commands. */

    private item(item: PCBItem, color: string) {
        if (item.text) {
            console.warn("pcb-assembly doesn't support text items", item);
        } else if (item.type == "polygon") {
            this.polygon(item as PCBPolygon, color);
        } else if (item.type !== undefined) {
            this.edge(item as PCBEdge, color);
        } else if (Object.hasOwn(item, "svgpath")) {
            this.svgpath(item as PCBItem, color);
        } else if (Object.hasOwn(item, "polygons")) {
            this.polygons(item as PCBPolygon, color);
        } else {
            console.error("Unknown drawing item", item);
        }
    }

    private footprint(
        layer: string,
        footprint: PCBFootprint,
        highlight: boolean,
    ) {
        const ctx = this.ctx;

        const highlightPinOne =
            footprint.ref.startsWith("D") ||
            footprint.ref.startsWith("U") ||
            footprint.ref.startsWith("CP");

        for (var item of footprint.drawings) {
            if (item.layer == layer) {
                this.item(item, this.colors.pad);
            }
        }

        for (var pad of footprint.pads) {
            if (pad.layers.includes(layer)) {
                this.pad(pad, this.colors.pad, false);
                if (pad.pin1 && highlightPinOne) {
                    this.pad(pad, this.colors.pin1, true);
                }
            }
        }

        for (var pad of footprint.pads) {
            this.padHole(pad, this.colors.hole);
        }

        if (highlight) {
            // draw bounding box
            if (footprint.layer == layer) {
                ctx.save();
                ctx.translate(...footprint.bbox.pos);
                ctx.rotate(deg2rad(-footprint.bbox.angle));
                ctx.translate(...footprint.bbox.relpos);
                ctx.fillStyle = this.colors.highlight_fill;
                ctx.fillRect(0, 0, ...footprint.bbox.size);
                ctx.strokeStyle = this.colors.highlight_stroke;
                ctx.strokeRect(0, 0, ...footprint.bbox.size);
                ctx.restore();
            }
        }
    }

    private edge(edge: PCBEdge, color: string) {
        const ctx = this.ctx;

        ctx.strokeStyle = color;
        ctx.fillStyle = color;
        ctx.lineWidth = edge.width;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";

        ctx.beginPath();
        if (edge.type == "segment") {
            ctx.moveTo(...edge.start);
            ctx.lineTo(...edge.end);
        }
        if (edge.type == "rect") {
            ctx.moveTo(...edge.start);
            ctx.lineTo(edge.start[0], edge.end[1]);
            ctx.lineTo(...edge.end);
            ctx.lineTo(edge.end[0], edge.start[1]);
            ctx.lineTo(...edge.start);
        }
        if (edge.type == "arc") {
            ctx.arc(
                ...edge.start,
                edge.radius,
                deg2rad(edge.startangle),
                deg2rad(edge.endangle),
            );
        }
        if (edge.type == "circle") {
            ctx.arc(...edge.start, edge.radius, 0, 2 * Math.PI);
            ctx.closePath();
        }
        if (edge.type == "curve") {
            ctx.moveTo(...edge.start);
            ctx.bezierCurveTo(...edge.cpa, ...edge.cpb, ...edge.end);
        }
        if ("filled" in edge && edge.filled) {
            ctx.fill();
        } else {
            ctx.stroke();
        }
    }

    private polygon(shape: PCBPolygon, color: string) {
        const ctx = this.ctx;
        ctx.save();
        ctx.translate(...shape.pos);
        ctx.rotate(deg2rad(-shape.angle));

        if ("filled" in shape && !shape.filled) {
            ctx.strokeStyle = color;
            ctx.lineWidth = shape.width;
            ctx.lineCap = "round";
            ctx.lineJoin = "round";
            ctx.stroke(this.makePolygonPath(shape));
        } else {
            ctx.fillStyle = color;
            ctx.fill(this.makePolygonPath(shape));
        }
        ctx.restore();
    }

    private polygons(item: PCBPolygon, color: string) {
        this.ctx.save();
        this.ctx.strokeStyle = color;
        this.ctx.fillStyle = color;
        this.ctx.lineCap = "round";
        this.ctx.lineJoin = "round";
        this.ctx.lineWidth = item.thickness;
        var path = new Path2D();
        for (var polygon of item.polygons) {
            path.moveTo(...polygon[0]!);
            for (var i = 1; i < polygon.length; i++) {
                path.lineTo(...polygon[i]!);
            }
            path.closePath();
        }
        item.filled !== false ? this.ctx.fill(path) : this.ctx.stroke(path);
        this.ctx.restore();
    }

    private svgpath(item: PCBItem, color: string) {
        this.ctx.save();
        this.ctx.strokeStyle = color;
        this.ctx.lineCap = "round";
        this.ctx.lineJoin = "round";
        this.ctx.lineWidth = item.thickness;
        this.ctx.stroke(new Path2D(item.svgpath));
        this.ctx.restore();
    }

    private pad(pad: PCBPad, color: string, outline: boolean) {
        const ctx = this.ctx;

        ctx.save();
        ctx.translate(...pad.pos);
        ctx.rotate(deg2rad(pad.angle));
        if (pad.offset) {
            ctx.translate(...pad.offset);
        }
        ctx.fillStyle = color;
        ctx.strokeStyle = color;
        var path = this.makePadPath(pad);
        if (outline) {
            ctx.stroke(path);
        } else {
            ctx.fill(path);
        }
        ctx.restore();
    }

    private padHole(pad: PCBPad, color: string) {
        const ctx = this.ctx;

        if (pad.type != "th") return;
        ctx.save();
        ctx.translate(...pad.pos);
        ctx.rotate(deg2rad(pad.angle));
        ctx.fillStyle = color;
        if (pad.drillshape == "oblong") {
            ctx.fill(this.makeOblongPath(pad.drillsize));
        } else {
            ctx.fill(this.makeCirclePath(pad.drillsize[0] / 2));
        }
        ctx.restore();
    }

    /* Path generation commands */

    private makeChamferedRectPath(
        size: [number, number],
        radius: number,
        chamfpos: number,
        chamfratio: number,
    ): Path2D {
        // chamfpos is a bitmask, left = 1, right = 2, bottom left = 4, bottom right = 8
        var path = new Path2D();
        var width = size[0];
        var height = size[1];
        var x = width * -0.5;
        var y = height * -0.5;
        var chamfOffset = Math.min(width, height) * chamfratio;
        path.moveTo(x, 0);
        if (chamfpos & 4) {
            path.lineTo(x, y + height - chamfOffset);
            path.lineTo(x + chamfOffset, y + height);
            path.lineTo(0, y + height);
        } else {
            path.arcTo(x, y + height, x + width, y + height, radius);
        }
        if (chamfpos & 8) {
            path.lineTo(x + width - chamfOffset, y + height);
            path.lineTo(x + width, y + height - chamfOffset);
            path.lineTo(x + width, 0);
        } else {
            path.arcTo(x + width, y + height, x + width, y, radius);
        }
        if (chamfpos & 2) {
            path.lineTo(x + width, y + chamfOffset);
            path.lineTo(x + width - chamfOffset, y);
            path.lineTo(0, y);
        } else {
            path.arcTo(x + width, y, x, y, radius);
        }
        if (chamfpos & 1) {
            path.lineTo(x + chamfOffset, y);
            path.lineTo(x, y + chamfOffset);
            path.lineTo(x, 0);
        } else {
            path.arcTo(x, y, x, y + height, radius);
        }
        path.closePath();
        return path;
    }

    private makeOblongPath(size: [number, number]): Path2D {
        return this.makeChamferedRectPath(
            size,
            Math.min(size[0], size[1]) / 2,
            0,
            0,
        );
    }

    private makePolygonPath(shape: PCBPolygon | PCBPad): Path2D {
        if (shape.path2d) {
            return shape.path2d;
        }

        const path = new Path2D();
        for (const polygon of shape.polygons) {
            path.moveTo(...polygon[0]!);
            for (let i = 1; i < polygon.length; i++) {
                path.lineTo(...polygon[i]!);
            }
            path.closePath();
        }

        shape.path2d = path;

        return shape.path2d;
    }

    private makeCirclePath(radius: number): Path2D {
        var path = new Path2D();
        path.arc(0, 0, radius, 0, 2 * Math.PI);
        path.closePath();
        return path;
    }

    private makePadPath(pad: PCBPad): Path2D {
        if (pad.path2d) {
            return pad.path2d;
        }

        if (pad.shape == "rect") {
            const start = pad.size.map((c) => -c * 0.5) as [number, number];
            pad.path2d = new Path2D();
            pad.path2d.rect(...start, ...pad.size);
        } else if (pad.shape == "oval") {
            pad.path2d = this.makeOblongPath(pad.size);
        } else if (pad.shape == "circle") {
            pad.path2d = this.makeCirclePath(pad.size[0] / 2);
        } else if (pad.shape == "roundrect") {
            pad.path2d = this.makeChamferedRectPath(pad.size, pad.radius, 0, 0);
        } else if (pad.shape == "chamfrect") {
            pad.path2d = this.makeChamferedRectPath(
                pad.size,
                pad.radius,
                pad.chamfpos,
                pad.chamfratio,
            );
        } else if (pad.shape == "custom") {
            pad.path2d = this.makePolygonPath(pad);
        }

        return pad.path2d;
    }
}

function deg2rad(deg: number): number {
    return (deg * Math.PI) / 180;
}
