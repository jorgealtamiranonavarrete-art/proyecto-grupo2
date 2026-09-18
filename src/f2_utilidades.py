"""Preparación descriptiva de nacimientos DEIS, Grupo 2. Sin modificar originales."""
from pathlib import Path
import hashlib
import calendar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm

ORDEN_EDAD = ['MENORES 15 AÑOS', '15 A 19 AÑOS', '20 A 24 AÑOS', '25 A 29 AÑOS',
              '30 A 34 AÑOS', '35 A 39 AÑOS', '40 A 44 AÑOS', '45 A 49 AÑOS', '50 O MAS AÑOS']
CLAVES = ['ANO_NAC','MES_NAC','GRUPO_ETARIO_MADRE','REGION_RESIDENCIA','GLOSA_REGION_RESIDENCIA','TALLA']

class DatosError(ValueError):
    """Entrada incompatible con el análisis acordado."""

def huella(ruta):
    """SHA-256 del archivo, leído por bloques."""
    h = hashlib.sha256()
    with Path(ruta).open('rb') as f:
        for b in iter(lambda:f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def cargar(ruta):
    """Lee el CSV original sin imputar; informa ausencia de archivo o columnas."""
    ruta = Path(ruta)
    if not ruta.is_file(): raise FileNotFoundError(f'Falta data/raw/{ruta.name}. Incorpore el CSV original.')
    d = pd.read_csv(ruta, sep=';', encoding='utf-8', low_memory=False)
    if d.empty: raise DatosError('El archivo no contiene filas.')
    faltan = sorted(set(CLAVES)-set(d.columns))
    if faltan: raise DatosError(f'Faltan columnas: {faltan}')
    return d

def perfil(d):
    """Dimensiones por variable, nulos y cardinalidad antes de transformar."""
    if d.empty: raise DatosError('No se puede perfilar una tabla vacía.')
    n = d.isna().sum()
    return pd.DataFrame({'tipo':d.dtypes.astype(str),'nulos':n,
        'pct_nulos':100*n/len(d),'valores_distintos':d.nunique()}).rename_axis('variable').reset_index()

def faltantes_region(d):
    """Tabla larga: denominador = todos los nacidos vivos de la región."""
    if d['REGION_RESIDENCIA'].isna().any() or d['GLOSA_REGION_RESIDENCIA'].isna().any():
        raise DatosError('Hay registros sin región; resolver su tratamiento antes de agrupar.')
    grupo = d.groupby(['REGION_RESIDENCIA','GLOSA_REGION_RESIDENCIA'], observed=True, sort=True)
    n = grupo.size().rename('nacimientos')
    validos = grupo.count()
    faltantes = validos.apply(lambda x:n-x)
    largo = faltantes.rename_axis(columns='variable').stack().rename('nulos').reset_index()
    largo = largo.merge(n.reset_index(), on=['REGION_RESIDENCIA','GLOSA_REGION_RESIDENCIA'], validate='many_to_one')
    largo['pct_nulos'] = 100*largo['nulos']/largo['nacimientos']
    return largo

def graficar_nulos(d, regional):
    """Dos mapas sin muestreo y barras de talla. Devuelve figuras para mostrar y guardar."""
    # Cada bloque resume registros consecutivos; no representa tiempo.
    matriz = d.isna().groupby(np.arange(len(d))//2500).mean()*100
    fig,ax = plt.subplots(figsize=(12,6.5),layout='constrained')
    im=ax.imshow(matriz,aspect='auto',interpolation='nearest',cmap='magma',norm=PowerNorm(.4,vmin=0,vmax=100))
    ax.set_xticks(range(len(d.columns)),d.columns,rotation=65,ha='right',fontsize=8)
    ax.set_ylabel('Bloques consecutivos de hasta 2.500 registros')
    ax.set_title('Nulos en toda la base — porcentaje por variable y bloque\nOrden original del CSV; no es una secuencia temporal')
    cb=fig.colorbar(im,ax=ax);cb.set_label('% de nulos — escala de color no lineal');cb.set_ticks([0,.1,1,10,50,100])
    variables=d.columns[d.isna().any()].tolist()
    if not variables: variables=['TALLA']
    tabla=regional[regional.variable.isin(variables)].pivot(index='GLOSA_REGION_RESIDENCIA',columns='variable',values='pct_nulos').reindex(columns=variables)
    fig2,ax2=plt.subplots(figsize=(12,8),layout='constrained')
    im2=ax2.imshow(tabla,aspect='auto',cmap='YlOrRd',vmin=0,vmax=max(1,float(tabla.max().max())))
    ax2.set_xticks(range(len(variables)),variables,rotation=25,ha='right')
    ax2.set_yticks(range(len(tabla)),tabla.index,fontsize=9)
    for i in range(len(tabla)):
        for j in range(len(variables)):
            v=float(tabla.iloc[i,j]);ax2.text(j,i,f'{v:.3f}%',ha='center',va='center',fontsize=8,color='white' if v>im2.norm.vmax*.65 else 'black')
    ax2.set_title('Porcentaje de nulos dentro de cada región, 2020–2023\nSolo variables con algún nulo en la base')
    fig2.colorbar(im2,ax=ax2,label='% de nacimientos de la región')
    t=regional[regional.variable.eq('TALLA')].sort_values('pct_nulos')
    fig3,ax3=plt.subplots(figsize=(12,7),layout='constrained')
    ax3.barh(t.GLOSA_REGION_RESIDENCIA,t.pct_nulos,color='#2b678a')
    for i,row in enumerate(t.itertuples()):
        ax3.text(row.pct_nulos+.005,i,f'{row.pct_nulos:.3f}% ({row.nulos:,}/{row.nacimientos:,})',va='center',fontsize=8)
    ax3.set_xlim(0,max(.1,float(t.pct_nulos.max()))*1.65)
    ax3.set_xlabel('% de nacimientos de la región con talla ausente')
    ax3.set_title('Faltantes de talla por residencia de la madre\nEtiquetas: porcentaje y cantidad / total regional')
    ax3.tick_params(axis='y',labelsize=9)
    return {'mapa_nulos_bloques':fig,'mapa_nulos_regiones':fig2,'talla_nulos_regiones':fig3}

def preparar(d):
    """Prepara seis variables y derivadas sin borrar filas ni imputar claves."""
    faltan=set(CLAVES)-set(d.columns)
    if faltan: raise DatosError(f'Faltan columnas: {sorted(faltan)}')
    out=d[CLAVES].copy()
    for c in ['ANO_NAC','MES_NAC','REGION_RESIDENCIA']:
        v=pd.to_numeric(out[c],errors='coerce')
        if v.isna().any() or not np.isfinite(v).all() or (v%1!=0).any(): raise DatosError(f'{c}: valores no enteros o ausentes.')
        out[c]=v.astype('int64')
    if not out.ANO_NAC.isin([2020,2021,2022,2023]).all(): raise DatosError('Año fuera de 2020–2023.')
    if not out.MES_NAC.between(1,12).all(): raise DatosError('Mes fuera de 1–12.')
    if not out.REGION_RESIDENCIA.between(1,16).all(): raise DatosError('Región fuera del catálogo 1–16.')
    edad=out.GRUPO_ETARIO_MADRE.astype('string').str.strip()
    glosa=out.GLOSA_REGION_RESIDENCIA.astype('string').str.strip()
    if edad.isna().any() or not edad.isin(ORDEN_EDAD).all(): raise DatosError('Edad materna desconocida: no clasificar silenciosamente como adulta.')
    if glosa.isna().any() or glosa.eq('').any(): raise DatosError('Glosa regional ausente.')
    out['GLOSA_REGION_RESIDENCIA']=glosa
    if out.groupby('REGION_RESIDENCIA').GLOSA_REGION_RESIDENCIA.nunique().gt(1).any(): raise DatosError('Un código regional tiene más de una glosa.')
    out['GRUPO_ETARIO_MADRE']=pd.Categorical(edad,categories=ORDEN_EDAD,ordered=True)
    out['grupo_etario_orden']=out.GRUPO_ETARIO_MADRE.cat.codes
    out['madre_menor_20']=edad.isin(ORDEN_EDAD[:2]).astype(bool)
    talla=pd.to_numeric(out.TALLA,errors='coerce')
    invalida=out.TALLA.notna() & (talla.isna() | ~np.isfinite(talla) | talla.le(0))
    out['talla_original']=out.TALLA
    out['talla_observada_cm']=talla.mask(invalida)
    out['talla_ausente_original']=out.TALLA.isna()
    out['talla_invalida_tecnica']=invalida
    # No se inventa un día de nacimiento: periodo mensual, no fecha individual.
    out['periodo_mes']=pd.PeriodIndex(out.ANO_NAC.astype(str)+'-'+out.MES_NAC.astype(str).str.zfill(2),freq='M')
    return out

def comparar_imputacion(p):
    """Compara casos observados, media, mediana general y mediana regional; no elige automáticamente."""
    x=p.talla_observada_cm.astype(float)
    if x.notna().sum()==0: raise DatosError('No hay tallas válidas para calcular valores de imputación.')
    med_grupo=p.groupby('REGION_RESIDENCIA').talla_observada_cm.transform('median')
    respaldo=x.isna() & med_grupo.isna()
    escenarios={'sin_imputar':x.copy(),'media_general':x.fillna(x.mean()),
        'mediana_general':x.fillna(x.median()),'mediana_region':x.fillna(med_grupo).fillna(x.median())}
    resumen=[];regionales=[]
    base=x.std(ddof=1)
    for nombre,s in escenarios.items():
        resumen.append({'metodo':nombre,'n_validos':int(s.count()),'n_imputados':int((x.isna() & s.notna()).sum()),
            'excluidos_solo_calculo_talla':int(s.isna().sum()),'media_cm':s.mean(),'mediana_cm':s.median(),
            'desv_cm':s.std(ddof=1),'cambio_desv_pct':100*(s.std(ddof=1)/base-1) if base else np.nan,
            'asimetria':s.skew(),'respaldo_mediana_general':int(respaldo.sum()) if nombre=='mediana_region' else 0})
        t=p[['REGION_RESIDENCIA','GLOSA_REGION_RESIDENCIA']].assign(valor=s).groupby(['REGION_RESIDENCIA','GLOSA_REGION_RESIDENCIA'],observed=True).valor.agg(['mean','count']).reset_index()
        t['metodo']=nombre;regionales.append(t)
    detalle=pd.concat(regionales,ignore_index=True)
    base_reg=detalle[detalle.metodo.eq('sin_imputar')][['REGION_RESIDENCIA','mean']].rename(columns={'mean':'media_observada_cm'})
    detalle=detalle.merge(base_reg,on='REGION_RESIDENCIA',validate='many_to_one')
    detalle['cambio_media_cm']=detalle['mean']-detalle.media_observada_cm
    return escenarios,pd.DataFrame(resumen),detalle

def resumen_atipicos(x):
    """Identifica extremos estadísticos con RIC; no diagnostica errores clínicos."""
    x=x.dropna();q1=x.quantile(.25);q3=x.quantile(.75);ric=q3-q1
    bajo=q1-1.5*ric;alto=q3+1.5*ric
    return {'minimo':float(x.min()),'maximo':float(x.max()),'q1':float(q1),'q3':float(q3),
        'limite_ric_inferior':float(bajo),'limite_ric_superior':float(alto),
        'n_fuera_ric':int(((x<bajo)|(x>alto)).sum()),'pct_fuera_ric':float(100*((x<bajo)|(x>alto)).mean())}

def calendario_periodo():
    """Calendario completo independiente de los registros observados."""
    return pd.DataFrame([(a,m,calendar.monthrange(a,m)[1]) for a in range(2020,2024) for m in range(1,13)],columns=['ANO_NAC','MES_NAC','dias'])

def comparar_escalas(x):
    """Compara representaciones para la rúbrica sin cambiar los centímetros de la base preparada."""
    x=x.astype(float);q1=x.quantile(.25);q3=x.quantile(.75)
    escalas={'centimetros':x,'z_score':(x-x.mean())/x.std(ddof=0) if x.std(ddof=0)>0 else x*0,
        'minmax':(x-x.min())/(x.max()-x.min()) if x.max()>x.min() else x*0,
        'robusta':(x-x.median())/(q3-q1) if q3>q1 else x*0}
    return pd.DataFrame([{'escala':k,'media':s.mean(),'desv_poblacional':s.std(ddof=0),'minimo':s.min(),
        'mediana':s.median(),'maximo':s.max()} for k,s in escalas.items()])

def aplanar(obj,prefijo=''):
    """Convierte metadatos anidados en pares ruta-valor mediante recursividad."""
    salida={}
    for clave,valor in obj.items():
        ruta=f'{prefijo}.{clave}' if prefijo else str(clave)
        if isinstance(valor,dict): salida.update(aplanar(valor,ruta))
        else: salida[ruta]=valor
    return salida

def validar(original,p,escenarios,cal):
    """Verifica preservación de filas y observados, escenarios y calendario."""
    assert len(original)==len(p) and original.index.equals(p.index)
    assert p.madre_menor_20.notna().all()
    validas=p.talla_observada_cm.notna()
    for nombre,s in escenarios.items():
        assert s.loc[validas].equals(p.talla_observada_cm.astype(float).loc[validas]),nombre
        if nombre!='sin_imputar': assert s.notna().all(),nombre
    assert p.groupby('REGION_RESIDENCIA',observed=True).size().sum()==len(original)
    assert len(cal)==48 and cal.dias.sum()==1461
    assert cal.loc[cal.MES_NAC.eq(2),'dias'].sum()==113
    return True
