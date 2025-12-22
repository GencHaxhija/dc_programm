
    def export_multi_dxf(self, layer_ids, rectangle, out_dir, filename):
        """Export multiple vector layers into a single DXF file"""
        from qgis.core import QgsVectorLayer, QgsDxfExport
        
        if not layer_ids:
            QtWidgets.QMessageBox.warning(None, "Fehler", "Keine Layer ausgewählt!")
            return
        
        # Get all selected layers
        layers = []
        for lid in layer_ids:
            layer = QgsProject.instance().mapLayer(lid)
            if layer and isinstance(layer, QgsVectorLayer):
                layers.append(layer)
        
        if not layers:
            QtWidgets.QMessageBox.warning(None, "Fehler", "Keine gültigen Vektor-Layer gefunden!")
            return
        
        # Create output filename
        safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in filename)
        output_file = os.path.join(out_dir, f"{safe_name}.dxf")
        
        print(f"DEBUG: Exporting {len(layers)} layers to DXF: {output_file}")
        
        # QGIS DXF export for multiple layers
        dxf_export = QgsDxfExport()
        dxf_export.setDestinationCrs(layers[0].crs())  # Use first layer's CRS
        
        # Add all layers to export
        dxf_layers = []
        for layer in layers:
            dxf_layer = QgsDxfExport.DxfLayer(layer)
            dxf_layers.append(dxf_layer)
        
        dxf_export.setLayers(dxf_layers)
        
        # Set extent filter
        dxf_export.setExtent(rectangle)
        
        # Export
        result = dxf_export.writeToFile(output_file, "UTF-8")
        
        if result == QgsDxfExport.Success:
            print(f"Multi-DXF exportiert: {output_file}")
            QtWidgets.QMessageBox.information(None, "Erfolg", 
                f"DXF erfolgreich exportiert:\n{output_file}\n\n"
                f"{len(layers)} Layer kombiniert.")
        else:
            error_messages = {
                QgsDxfExport.DeviceNotWritableError: "Datei kann nicht geschrieben werden",
                QgsDxfExport.EmptyExtent: "Leerer Exportbereich",
            }
            error_msg = error_messages.get(result, f"Unbekannter Fehler ({result})")
            QtWidgets.QMessageBox.warning(None, "Fehler", 
                f"DXF-Export fehlgeschlagen:\n{error_msg}")
