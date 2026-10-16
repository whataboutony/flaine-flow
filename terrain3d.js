// Flaine Flow topographic terrain controller.
// Visual terrain context only; analytical piste elevation remains COP30-derived.
(function(){
  let contoursReady=false;

  function addContours(map){
    if(contoursReady || !window.maplibreContour) return;
    const {DemSource, contourProtocolUrl}=window.maplibreContour;
    if(!maplibregl.__flaineContourProtocol){
      maplibregl.addProtocol('flaine-contour', DemSource.contourProtocol);
      maplibregl.__flaineContourProtocol=true;
    }
    const dem=new DemSource({
      url:'https://demotiles.maplibre.org/terrain-tiles/{z}/{x}/{y}.png',
      encoding:'mapbox',
      maxzoom:12,
      worker:true
    });
    dem.setupMaplibre(maplibregl);
    if(!map.getSource('topo-contours')) map.addSource('topo-contours',{
      type:'vector',
      tiles:[contourProtocolUrl({
        demUrlPattern:'https://demotiles.maplibre.org/terrain-tiles/{z}/{x}/{y}.png',
        encoding:'mapbox',
        maxzoom:12,
        thresholds:{11:[100,500],12:[50,200],13:[50,200],14:[25,100],15:[25,100]},
        elevationKey:'ele',
        levelKey:'level',
        contourLayer:'contours'
      })]
    });
    const before=map.getStyle().layers.find(l=>l.type==='symbol')?.id;
    if(!map.getLayer('topo-contour-lines')) map.addLayer({
      id:'topo-contour-lines',type:'line',source:'topo-contours','source-layer':'contours',
      paint:{
        'line-color':['case',['==',['get','level'],1],'rgba(93,72,50,.76)','rgba(112,91,66,.46)'],
        'line-width':['case',['==',['get','level'],1],1.35,.7],
        'line-opacity':['interpolate',['linear'],['zoom'],11,.55,14,.9]
      }
    },before);
    if(!map.getLayer('topo-contour-labels')) map.addLayer({
      id:'topo-contour-labels',type:'symbol',source:'topo-contours','source-layer':'contours',
      filter:['==',['get','level'],1],
      layout:{
        'symbol-placement':'line',
        'text-field':['concat',['to-string',['get','ele']],' m'],
        'text-size':10,
        'text-font':['Noto Sans Regular'],
        'symbol-spacing':350,
        'text-rotation-alignment':'map'
      },
      paint:{'text-color':'#5d4832','text-halo-color':'rgba(255,255,255,.88)','text-halo-width':1.3}
    });
    contoursReady=true;
  }

  function enable(map, button){
    if(!map.getSource('terrain-dem-v2')) map.addSource('terrain-dem-v2',{
      type:'raster-dem',url:'https://demotiles.maplibre.org/terrain-tiles/tiles.json',tileSize:256
    });
    if(!map.getLayer('terrain-hillshade-v2')){
      const before=map.getStyle().layers.find(l=>l.type==='symbol')?.id;
      map.addLayer({id:'terrain-hillshade-v2',type:'hillshade',source:'terrain-dem-v2',paint:{
        'hillshade-exaggeration':0.9,
        'hillshade-shadow-color':'#39454b',
        'hillshade-highlight-color':'#fffdf7',
        'hillshade-accent-color':'#7d887c',
        'hillshade-illumination-direction':315
      }},before);
    }
    try{ addContours(map); }catch(e){ console.warn('Topographic contours unavailable',e); }
    map.setTerrain({source:'terrain-dem-v2',exaggeration:1.8});
    map.easeTo({pitch:68,bearing:-32,zoom:14.1,duration:1100});
    button.textContent='🗺️ 2D';
  }

  function disable(map, button){
    map.setTerrain(null);
    map.easeTo({pitch:0,bearing:0,zoom:13.7,duration:800});
    button.textContent='🏔️ 3D';
  }
  window.FlaineTerrain3D={enable,disable};
})();