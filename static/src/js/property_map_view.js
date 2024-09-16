odoo.define('property_management.MapView', ['@web/core/utils/patch', '@web/views/form/form_controller'], function(require) {
    "use strict";

    const { patch } = require('@web/core/utils/patch');
    const { FormController } = require('@web/views/form/form_controller');

    patch(FormController.prototype, {

        async setup() {
            await super.setup(...arguments);

            this._waitForElement('.o_notebook').then((notebook) => {
                this._observeNotebookChanges(notebook);
            });
        },

        _waitForElement(selector) {
            return new Promise((resolve) => {
                const element = document.querySelector(selector);
                if (element) {
                    resolve(element);
                } else {
                    const observer = new MutationObserver(() => {
                        const element = document.querySelector(selector);
                        if (element) {
                            resolve(element);
                            observer.disconnect();
                        }
                    });

                    observer.observe(document.body, {
                        childList: true,
                        subtree: true
                    });
                }
            });
        },

        _observeNotebookChanges(notebook) {
            const observer = new MutationObserver(() => {
                const mapContainer = document.getElementById('property_map');
                if (mapContainer) {
                    this._initializeMap(mapContainer);
                }
            });

            observer.observe(notebook, {
                childList: true,
                subtree: true
            });
        },

        _initializeMap(mapContainer) {
            const latField = document.querySelector('input[id="latitude_0"]');
            const lngField = document.querySelector('input[id="longitude_0"]');

            let initialLat = 0;
            let initialLng = 0;
            let zoomLevel = 2;

            if (latField && latField.value && lngField && lngField.value) {
                initialLat = parseFloat(latField.value);
                initialLng = parseFloat(lngField.value);
                zoomLevel = 13;
            }

            if (!mapContainer._leaflet_map) {
                const map = L.map(mapContainer).setView([initialLat, initialLng], zoomLevel);

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19
                }).addTo(map);

                mapContainer._leaflet_map = map;

                let marker;
                if (latField && latField.value && lngField && lngField.value) {
                    marker = L.marker([initialLat, initialLng]).addTo(map);
                }

                map.on('contextmenu', (e) => {
                    if (marker) {
                        map.removeLayer(marker);
                    }
                    marker = L.marker(e.latlng).addTo(map);

                    if (latField) {
                        latField.value = e.latlng.lat;
                        latField.dispatchEvent(new Event('input'));  // Trigger the input event
                        latField.dispatchEvent(new Event('change'));  // Trigger the change event
                    }
                    if (lngField) {
                        lngField.value = e.latlng.lng;
                        lngField.dispatchEvent(new Event('input'));  // Trigger the input event
                        lngField.dispatchEvent(new Event('change'));  // Trigger the change event
                    }
                });
            }
        },
    });
});
