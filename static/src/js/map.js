odoo.define('your_module.leaflet_map', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.LeafletMap = publicWidget.Widget.extend({
        selector: '#mapid',
        start: function () {
            this._super.apply(this, arguments);
            var map = L.map('mapid').setView([51.505, -0.09], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(map);
        },
    });

    return publicWidget.registry.LeafletMap;
});