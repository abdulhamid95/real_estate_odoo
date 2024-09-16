document.addEventListener("DOMContentLoaded", function() {
    // جلب الأزرار
    var btnCardView = document.getElementById('btn-card-view');
    var btnListView = document.getElementById('btn-list-view');
    var btnMapView = document.getElementById('btn-map-view');

    // جلب الحاويات
    var cardView = document.getElementById('card-view');
    var listView = document.getElementById('list-view');
    var mapView = document.getElementById('map');
    var pagination = document.getElementById('pagination')

    // تهيئة الخريطة (تحديثها فقط عند عرض الخريطة)
    var map;

    function initializeMap() {
        if (!map) {
            map = L.map('map').setView([30.5, 35.5], 5);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
        }
    }

    // دالة لتحديث العرض
    function updateView(viewType) {
        // إخفاء جميع الحاويات
        cardView.classList.add('d-none');
        listView.classList.add('d-none');
        mapView.classList.add('d-none');
        pagination.classList.add('d-none')

        // عرض الحاوية المختارة
        if (viewType === 'card') {
            cardView.classList.remove('d-none');
            pagination.classList.remove('d-none');
        } else if (viewType === 'list') {
            listView.classList.remove('d-none');
            pagination.classList.remove('d-none');
        } else if (viewType === 'map') {
            initializeMap();
            fetchMapData()
            mapView.classList.remove('d-none');
             setTimeout(function() {
                map.invalidateSize();
            }, 100);
        }
    }

    // دالة لجلب البيانات من الموجه الجديد وعرضها على الخريطة
function fetchMapData() {
    // استخراج القيم من الرابط
    const params = new URLSearchParams(window.location.search);

    // إنشاء كائن يحتوي على القيم
    const filters = {
        min_price: params.get('min_price'),
        max_price: params.get('max_price'),
        property_type: params.get('property_type'),
        property_status: params.get('property_status'),
        min_area: params.get('min_area'),
        max_area: params.get('max_area'),
        number_of_rooms: params.get('number_of_rooms'),
        floor_number: params.get('floor_number')
    };

    // إرسال طلب fetch باستخدام الفلاتر
    fetch(`/properties/map?${params.toString()}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // التعامل مع البيانات المسترجعة
        data.forEach(function(property) {
            var marker = L.marker([property.latitude, property.longitude]).addTo(map);
            marker.bindPopup('<a href="/property/' + property.id + '">' + property.name + '</a>');
        });
    })
    .catch(error => console.error('Error fetching property data:', error));
}



    // إضافة حدث النقر للأزرار
    btnCardView.addEventListener('click', function() {
        updateView('card');
    });

    btnListView.addEventListener('click', function() {
        updateView('list');
    });

    btnMapView.addEventListener('click', function() {
        updateView('map');
    });
});