// Flaine Flow 3D terrain controller.
// Visual terrain context only; analytical piste elevation remains COP30-derived.
(function(){
  function enable(map, button){
    if(!map.getSource('terrain-dem-v2')) map.addSource('terrain-dem-v2',{
      type:'raster-dem',
      url:'https://demotiles.maplibre.org/terrain-tiles/tiles.json',
      tileSize:256
    });
    if(!map.getLayer('terrain-hillshade-v2')){
      const firstSymbol=map.getStyle().layers.find(l=>l.type==='symbol')?.id;
      map.addLayer({
        id:'terrain-hillshade-v2',type:'hillshade',source:'terrain-dem-v2',
        paint:{
          'hillshade-exaggeration':0.8,
          'hillshade-shadow-color':'#46515a',
          'hillshade-highlight-color':'#ffffff',
          'hillshade-accent-color':'#6b7c84',
          'hillshade-illumination-direction':315
        }
      },firstSymbol);
    }
    map.setTerrain({source:'terrain-dem-v2',exaggeration:1.8});
    map.easeTo({pitch:72,bearing:-32,zoom:14.1,duration:1100});
    button.textContent='🗺️ 2D';
  }
  function disable(map, button){
    map.setTerrain(null);
    map.easeTo({pitch:0,bearing:0,zoom:13.7,duration:800});
    button.textContent='🏔️ 3D';
  }
  window.FlaineTerrain3D={enable,disable};
})();