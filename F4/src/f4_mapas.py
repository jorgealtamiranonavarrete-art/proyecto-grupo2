"""Create two self-contained, exploratory HTML maps of the 16 Chilean regions."""

from __future__ import annotations

import html
import json
from pathlib import Path


def _blend(a: str, b: str, fraction: float) -> str:
    fraction = max(0.0, min(1.0, fraction))
    first = tuple(int(a[i:i + 2], 16) for i in (1, 3, 5))
    last = tuple(int(b[i:i + 2], 16) for i in (1, 3, 5))
    return '#' + ''.join(f'{round(x + (y-x)*fraction):02x}' for x, y in zip(first, last))


def _region_path(feature: dict) -> str:
    def xy(lon: float, lat: float) -> tuple[float, float]:
        return 80 + (lon + 76) * 34, 70 + (-17 - lat) * 21.8

    commands = []
    for polygon in feature['geometry']['coordinates']:
        for ring in polygon:
            for index, (lon, lat) in enumerate(ring):
                x, y = xy(lon, lat)
                commands.append(f'{"M" if index == 0 else "L"}{x:.1f},{y:.1f}')
            commands.append('Z')
    return ' '.join(commands)


def generar_mapa(geometry_path: Path, records: list[dict], output_path: Path,
                 *, title: str, unit: str, explanation: str,
                 low_color: str, high_color: str) -> Path:
    """Render validated regional values in one offline HTML file.

    Each record has: region_code, name, value, n, detail. A missing region or
    non-finite value stops generation instead of silently leaving a blank area.
    """
    from math import isfinite

    geometry = json.loads(Path(geometry_path).read_text(encoding='utf-8'))
    features = geometry['features']
    shape_codes = [int(f['properties']['region_code']) for f in features]
    record_codes = [int(r['region_code']) for r in records]
    expected = set(range(1, 17))
    if set(shape_codes) != expected or len(shape_codes) != 16:
        raise ValueError('La capa debe contener una vez cada una de las 16 regiones.')
    if set(record_codes) != expected or len(record_codes) != 16:
        raise ValueError('Los datos deben contener una vez cada una de las 16 regiones.')
    if any(not isfinite(float(r['value'])) or int(r['n']) <= 0 for r in records):
        raise ValueError('El mapa requiere valores finitos y denominadores positivos.')

    by_code = {int(r['region_code']): r for r in records}
    values = [float(r['value']) for r in records]
    lo, hi = min(values), max(values)
    if hi <= lo:
        raise ValueError('La escala de color necesita al menos dos valores distintos.')
    shapes = []
    for feature in features:
        code = int(feature['properties']['region_code'])
        record = by_code[code]
        fraction = (float(record['value']) - lo) / (hi - lo)
        label = html.escape(str(record['name']), quote=True)
        shapes.append(
            f'<path class="region" d="{_region_path(feature)}" '
            f'fill="{_blend(low_color, high_color, fraction)}" '
            f'data-code="{code}" tabindex="0" role="button" '
            f'aria-label="{label}: {float(record["value"]):.2f} {html.escape(unit)}"/>'
        )
    entries = {str(int(r['region_code'])): {
        'name': str(r['name']), 'value': round(float(r['value']), 5),
        'n': int(r['n']), 'detail': str(r['detail'])
    } for r in records}
    safe_json = json.dumps(entries, ensure_ascii=False).replace('<', '\\u003c')
    ordered = sorted(records, key=lambda r: float(r['value']), reverse=True)
    items = '\n'.join(
        f'<button class="list-item" data-code="{int(r["region_code"])}">'
        f'<span>{html.escape(str(r["name"]))}</span><strong>{float(r["value"]):.2f} {html.escape(unit)}</strong></button>'
        for r in ordered
    )
    source_url = html.escape(geometry['attribution']['source_url'], quote=True)
    page = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root{{--navy:#173f59;--ink:#182c38;--muted:#526574;--line:#d9e3e9;--red:#a62834}}
*{{box-sizing:border-box}}body{{margin:0;background:#f5f8fa;color:var(--ink);font:16px/1.45 system-ui,Segoe UI,Arial,sans-serif}}
header{{background:white;border-top:7px solid var(--red);padding:20px max(22px,calc((100vw - 1200px)/2));border-bottom:1px solid var(--line)}}
h1{{font-size:26px;line-height:1.15;color:var(--navy);margin:0 0 8px}}header p{{margin:0;color:var(--muted)}}
main{{max-width:1200px;margin:18px auto;display:grid;grid-template-columns:minmax(360px,520px) minmax(320px,1fr);gap:18px;padding:0 16px}}
.card{{background:white;border:1px solid var(--line);border-radius:12px;box-shadow:0 2px 10px #163f5810}}
.map-card{{padding:12px;position:relative}}.toolbar{{display:flex;justify-content:space-between;gap:8px;align-items:center;margin:0 3px 8px}}
button{{font:inherit;cursor:pointer}}.reset{{border:1px solid var(--line);border-radius:7px;background:#fff;color:var(--navy);padding:5px 10px}}
.map-wrap{{height:min(76vh,850px);min-height:600px;overflow:hidden;touch-action:none;cursor:grab}}.map-wrap:active{{cursor:grabbing}}
svg{{width:100%;height:100%;display:block}}.region{{stroke:#fff;stroke-width:1.3;vector-effect:non-scaling-stroke;fill-rule:evenodd;cursor:pointer}}
.region:hover,.region.active{{stroke:#122c3f;stroke-width:2.5;filter:brightness(1.05)}}
.legend{{display:flex;align-items:center;gap:8px;padding:8px 3px 1px;font-size:13px}}.ramp{{flex:1;height:13px;background:linear-gradient(90deg,{low_color},{high_color});border-radius:4px}}
.side{{display:grid;grid-template-rows:auto 1fr;gap:16px}}.detail{{padding:20px}}.detail h2{{font-size:22px;color:var(--navy);margin:0 0 10px}}
.big{{font-size:32px;font-weight:700;color:var(--red);margin:0}}.meta{{color:var(--muted);margin:3px 0 0}}.explain{{margin:14px 0 0}}
.list{{padding:8px 16px 16px;overflow:auto;max-height:610px}}.list h2{{font-size:17px;color:var(--navy);margin:7px 0 10px}}
.list-item{{width:100%;display:flex;align-items:center;justify-content:space-between;text-align:left;gap:10px;background:#fff;border:0;border-bottom:1px solid var(--line);padding:8px 3px;color:var(--ink);font-size:14px}}
.list-item:hover,.list-item.active{{background:#edf4f8}}.list-item strong{{white-space:nowrap;color:var(--navy)}}
.tooltip{{position:fixed;z-index:9;background:#173f59;color:#fff;border-radius:6px;padding:5px 9px;pointer-events:none;font-size:13px;display:none}}
footer{{max-width:1200px;margin:0 auto 30px;padding:0 18px;color:var(--muted);font-size:13px}}a{{color:#174a67}}
@media(max-width:850px){{main{{grid-template-columns:1fr}}.map-wrap{{height:68vh;min-height:500px}}.side{{grid-template-rows:auto auto}}.list{{max-height:300px}}}}
</style></head><body>
<header><h1>{html.escape(title)}</h1><p>Chile, 2020–2023 · Grupo 2 · MCDI500 · Mapa exploratorio complementario</p></header>
<main><section class="card map-card" aria-label="Mapa regional interactivo">
<div class="toolbar"><strong>Seleccione o pase el cursor sobre una región</strong><button class="reset" id="reset">Restablecer vista</button></div>
<div class="map-wrap" id="mapWrap"><svg id="map" viewBox="0 0 500 960" aria-label="Mapa de 16 regiones de Chile">
<g id="mapLayer">{''.join(shapes)}</g></svg></div>
<div class="legend"><span>{lo:.2f}</span><div class="ramp"></div><span>{hi:.2f} {html.escape(unit)}</span></div>
</section><aside class="side"><section class="card detail" aria-live="polite"><h2 id="regionName">Región</h2>
<p class="big" id="regionValue"></p><p class="meta" id="regionN"></p><p id="regionDetail" class="explain"></p></section>
<section class="card list"><h2>Las 16 regiones, ordenadas por valor</h2>{items}</section></aside></main>
<footer><p>{html.escape(explanation)}</p>
<p>Fuente de nacimientos: DEIS/MINSAL, Serie 2020–2023. Límites: <a href="{source_url}">geoBoundaries gbOpen CHL ADM1</a> (origen BCN/OCHA ROLAC; atribución geoBoundaries CC BY 4.0 y fuente CC BY 3.0 IGO). Geometría simplificada; islas oceánicas lejanas de Valparaíso no se dibujan en la vista principal. La forma y el color no deben usarse para comparar áreas ni inferir causalidad. Archivo autónomo: funciona sin conexión.</p></footer>
<div class="tooltip" id="tip"></div>
<script>
const data={safe_json};const unit={json.dumps(unit,ensure_ascii=False)};
const paths=[...document.querySelectorAll('.region')],buttons=[...document.querySelectorAll('.list-item')];
const nameEl=document.getElementById('regionName'),valueEl=document.getElementById('regionValue'),nEl=document.getElementById('regionN'),detailEl=document.getElementById('regionDetail'),tip=document.getElementById('tip');
function choose(code){{const r=data[String(code)];nameEl.textContent=r.name;valueEl.textContent=r.value.toLocaleString('es-CL',{{minimumFractionDigits:2,maximumFractionDigits:2}})+' '+unit;nEl.textContent='Nacidos vivos: '+r.n.toLocaleString('es-CL');detailEl.textContent=r.detail;paths.forEach(p=>p.classList.toggle('active',p.dataset.code==code));buttons.forEach(b=>b.classList.toggle('active',b.dataset.code==code));}}
paths.forEach(p=>{{p.addEventListener('click',()=>choose(p.dataset.code));p.addEventListener('keydown',e=>{{if(e.key==='Enter'||e.key===' '){{e.preventDefault();choose(p.dataset.code)}}}});p.addEventListener('pointermove',e=>{{const r=data[p.dataset.code];tip.textContent=r.name+': '+r.value.toLocaleString('es-CL',{{minimumFractionDigits:2,maximumFractionDigits:2}})+' '+unit;tip.style.display='block';tip.style.left=(e.clientX+14)+'px';tip.style.top=(e.clientY+14)+'px'}});p.addEventListener('pointerleave',()=>tip.style.display='none')}});
buttons.forEach(b=>b.addEventListener('click',()=>choose(b.dataset.code)));
const svg=document.getElementById('map'),wrap=document.getElementById('mapWrap');let vb={{x:0,y:0,w:500,h:960}},drag=null;
function draw(){{svg.setAttribute('viewBox',`${{vb.x}} ${{vb.y}} ${{vb.w}} ${{vb.h}}`)}};
document.getElementById('reset').addEventListener('click',()=>{{vb={{x:0,y:0,w:500,h:960}};draw()}});
wrap.addEventListener('wheel',e=>{{e.preventDefault();const f=e.deltaY>0?1.12:0.89;const nw=Math.max(90,Math.min(900,vb.w*f)),nh=nw*960/500;const rect=svg.getBoundingClientRect();const rx=(e.clientX-rect.left)/rect.width,ry=(e.clientY-rect.top)/rect.height;vb.x+=(vb.w-nw)*rx;vb.y+=(vb.h-nh)*ry;vb.w=nw;vb.h=nh;draw()}},{{passive:false}});
wrap.addEventListener('pointerdown',e=>{{if(e.target.classList.contains('region'))return;drag={{x:e.clientX,y:e.clientY,vx:vb.x,vy:vb.y}};wrap.setPointerCapture(e.pointerId)}});
wrap.addEventListener('pointermove',e=>{{if(!drag)return;const r=svg.getBoundingClientRect();vb.x=drag.vx-(e.clientX-drag.x)*vb.w/r.width;vb.y=drag.vy-(e.clientY-drag.y)*vb.h/r.height;draw()}});
wrap.addEventListener('pointerup',()=>drag=null);wrap.addEventListener('pointercancel',()=>drag=null);
choose({int(ordered[0]['region_code'])});
</script></body></html>'''
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(page, encoding='utf-8')
    return output_path
