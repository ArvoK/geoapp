<script type="text/javascript">
var m =  L.map('m').setView([55.67, 12.55], 13);
    L.titleLayer('//{s}.title.osm.org/{z}/{x}/{y}.png').addTo(m);
    {% for e in object_list %}
        L.marker({(e.lat_lng}}).addTo(m).bindPopup('{{e}}');
    {% endfor %}