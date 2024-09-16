odoo.define('property_management.MapView', ['@web/core/utils/patch', '@web/views/legacy_view_registry', 'web.core'], function(require) {
    "use strict";

    const { patch } = require('@web/core/utils/patch');
    const legacyViewRegistry = require('@web/views/legacy_view_registry');
    const { ListRenderer } = require('web.ListRenderer');

    const { useEffect, onWillStart } = owl;

    // تعريف View الخريطة
    const PropertyMapView = {
        template: 'PropertyMapView',

        setup() {
            this.map = null;
            onWillStart(async () => {
                await this._loadMap();
            });

            useEffect(() => {
                if (!this.map) {
                    this._initializeMap();
                }
            });
        },

        async _loadMap() {
            const mapContainer = document.getElementById('property_map');
            if (mapContainer) {
                this._initializeMap(mapContainer);
            }
        },

        _initializeMap(mapContainer) {
            // إعداد الخريطة
            this.map = L.map(mapContainer).setView([0, 0], 2);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 19,
            }).addTo(this.map);

            this._addMarkers();
        },

        _addMarkers() {
            // إحضار بيانات العقارات وإضافة ماركرات
            const properties = this.props.records;
            properties.forEach(property => {
                const lat = property.latitude;
                const lng = property.longitude;

                if (lat && lng) {
                    const marker = L.marker([lat, lng]).addTo(this.map);
                    marker.bindPopup(property.name);
                }
            });
        }
    };

    legacyViewRegistry.add('property_map', PropertyMapView);

    // Patch لإضافة دعم عرض الخريطة إلى الـ ListRenderer
    patch(ListRenderer.prototype, 'property_management.MapView', {
        setup() {
            this._super(...arguments);

            // تحقق من وجود الخريطة في العرض الشجري
            const mapViewElement = this.el.querySelector('.o_map_view');
            if (mapViewElement) {
                this._initializeMapView(mapViewElement);
            }
        },

        _initializeMapView(mapViewElement) {
            // تهيئة الخريطة داخل العرض الشجري
            const mapContainer = mapViewElement.querySelector('#property_map');
            if (mapContainer) {
                new PropertyMapView(mapContainer).mount();
            }
        }
    });

    return PropertyMapView;
});
