import React from "react";
import { MapContainer, TileLayer, useMap } from "react-leaflet";
import * as ELG from "esri-leaflet-geocoder";

function Mapp() {
  
  function Geocoder({ address }) {
    const map = useMap();
    var googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
    });
    var googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
    });
    var googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
    });
    var googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
      maxZoom: 20,
      subdomains:['mt0','mt1','mt2','mt3']
    });

    
    
    var baseLayers = {
    "Satelite": googleSat,
    "Streets": googleStreets,
    "Hybrid": googleHybrid,
    "Terrain": googleTerrain
    };
    var control= L.control.layers(baseLayers);  
    
    ELG.geocode()
      .text(address)
      .run((err, results, response) => {
        console.log(results.results[0].latlng);
        const { lat, lng } = results.results[0].latlng;
        map.setView([lat, lng], 15).addLayer(googleSat).addControl(control);
        

      });
    
    return null;
  }

  const position = [53.35, 18.8];
  
  return (
    <MapContainer
      className="map"
      center={position}
      zoom={3}
      style={{ height: 500, width: "100%" }}
    >
      <TileLayer
        attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Geocoder address= {obiekt}/>
      
    </MapContainer>
  );
}
export default Mapp;
