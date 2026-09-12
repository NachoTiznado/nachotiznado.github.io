---
layout: page
permalink: /talks/
title: Talks
description: Conferences, invited lectures, keynote presentations, workshops, and guest lectures.
nav: true
nav_order: 4
---
<div class="talks-page">

<div class="talks-intro">
  <p>A selection of conferences, invited lectures, keynote presentations, workshops, and guest lectures.</p>
</div>

<div class="talks-summary">
  <div class="talks-summary-number">{{ site.data.talks | size }}</div>
  <div class="talks-summary-label">Presentations · 2016–2026</div>
</div>


<p class="talks-map-note">Explore the places where I have presented. Select a marker to see the presentations associated with that location.</p>

<div id="talks-map" class="talks-map" aria-label="Interactive map of presentation locations"></div>

<div class="featured-talks-header">
  <h2>Featured talks</h2>
  <p>A selection of recent conference presentations, invited lectures, and other talks.</p>
</div>

<div class="featured-talks">
{% for talk in site.data.talks %}
  {% if talk.featured %}
  <article class="featured-talk">
    <div class="featured-talk-year">{{ talk.year }}</div>
    <h3>{{ talk.citation }}</h3>
  </article>
  {% endif %}
{% endfor %}
</div>


<div class="all-talks-header">
  <h2>All talks</h2>
  <p>Conference presentations, invited lectures, workshops, and other academic talks.</p>
</div>

<div class="publications talks-publications">

{% assign categories = "Conference and symposia presentations|Invited lectures" | split: "|" %}
{% assign presentation_years = "2026,2025,2024,2023,2022,2021,2020,2019,2018,2017,2016" | split: "," %}

{% for category in categories %}
  <h3>{{ category }}</h3>

  {% for year in presentation_years %}
    {% assign year_has_talks = false %}

    {% for talk in site.data.talks %}
      {% assign talk_year = talk.year | append: "" %}

      {% if talk.category == category and talk_year == year %}
        {% assign year_has_talks = true %}
      {% endif %}
    {% endfor %}

    {% if year_has_talks %}
      <h4>{{ year }}</h4>

      <ul class="talk-list">
      {% for talk in site.data.talks %}
        {% assign talk_year = talk.year | append: "" %}

        {% if talk.category == category and talk_year == year %}
          <li>{{ talk.citation }}</li>
        {% endif %}
      {% endfor %}
      </ul>
    {% endif %}
  {% endfor %}
{% endfor %}

</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
/* Talks summary — aligned with the Research page style */

.talks-summary {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin: 1.5rem 0 2.5rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--global-divider-color);
}

.talks-summary-number {
  font-size: 2rem;
  font-weight: 500;
  line-height: 1;
  color: var(--global-text-color);
}

.talks-summary-label {
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--global-text-color-light);
}

.talks-map {
  width: 100%;
  height: 480px;
  border-radius: 12px;
  overflow: hidden;
  margin: 1rem 0 2.5rem;
  border: 1px solid var(--global-divider-color);
}

.talks-map-note {
  opacity: 0.75;
}

.featured-talks {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin: 1rem 0 2.5rem;
}

/* Featured talks heading */

.featured-talks-header {
  margin: 4rem 0 1.25rem;
}

.featured-talks-header h2 {
  margin-bottom: 0.35rem;
  font-size: 1.35rem;
  font-weight: 500;
  color: var(--global-text-color);
}

.featured-talks-header p {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--global-text-color-light);
}

/* Featured talk cards */

.featured-talk {
  padding: 1.15rem;
  border: 1px solid var(--global-divider-color);
  border-radius: 12px;
  transition:
    transform 0.2s ease,
    border-color 0.2s ease;
}

/* Subtle alternating colours */

.featured-talk:nth-child(3n + 1) {
  background: color-mix(
    in srgb,
    #4f86c6 12%,
    var(--global-bg-color)
  );
}

.featured-talk:nth-child(3n + 2) {
  background: color-mix(
    in srgb,
    #6ca56c 12%,
    var(--global-bg-color)
  );
}

.featured-talk:nth-child(3n + 3) {
  background: color-mix(
    in srgb,
    #b58a54 12%,
    var(--global-bg-color)
  );
}

.featured-talk:hover {
  transform: translateY(-3px);
  border-color: var(--global-theme-color);
}

.featured-talk-year {
  font-size: 0.85rem;
  opacity: 0.65;
  margin-bottom: 0.35rem;
}

.featured-talk h3 {
  font-size: 1.05rem;
  margin: 0.2rem 0 0.7rem;
}

.featured-talk p {
  font-size: 0.9rem;
  opacity: 0.78;
  margin: 0;
}

.talk-list {
  padding-left: 1.25rem;
}

.talk-list li {
  margin-bottom: 0.8rem;
}

/* Talks list — match Research publication styling */

.all-talks-header {
  margin: 4rem 0 1.25rem;
}

.all-talks-header h2 {
  margin-bottom: 0.35rem;
  font-size: 1.35rem;
  font-weight: 500;
}

.all-talks-header p {
  margin: 0;
  color: var(--global-text-color-light);
  font-size: 0.9rem;
}

.talks-publications {
  margin-top: 1rem;
}

.talks-publications h3 {
  margin-top: 2.5rem;
  margin-bottom: 1.25rem;
  font-size: 1.25rem;
  font-weight: 500;
}

.talks-publications h4 {
  margin-top: 1.75rem;
  margin-bottom: 0.75rem;
  font-size: 1.05rem;
  font-weight: 600;
}

.talks-publications .talk-list {
  margin-bottom: 1.5rem;
  padding-left: 2rem;
}

.talks-publications .talk-list li {
  margin-bottom: 1rem;
  padding-left: 0.35rem;
  line-height: 1.65;
  font-size: 0.95rem;
  color: var(--global-text-color);
}

.talks-publications .talk-list li::marker {
  color: var(--global-text-color-light);
}

@media (max-width: 768px) {
  .talks-publications .talk-list {
    padding-left: 1.5rem;
  }

  .talks-publications .talk-list li {
    font-size: 0.92rem;
  }
}

/* --------------------------------
   Overall Talks page typography
-------------------------------- */

.talks-page {
  font-family: inherit;
  color: var(--global-text-color);
}

/* Main page title and description */
.post-title,
.page-title {
  font-size: 1.35rem;
  font-weight: 500;
  margin-bottom: 0.35rem;
}

.post-description,
.page-description {
  color: var(--global-text-color-light);
  font-size: 0.9rem;
  font-weight: 400;
}

/* Section headings throughout the page */
.talks-page h2,
.talks-page h3,
.talks-page h4 {
  font-family: inherit;
  color: var(--global-text-color);
}

.talks-page h2 {
  font-size: 1.35rem;
  font-weight: 500;
}

.talks-page h3 {
  font-size: 1.15rem;
  font-weight: 500;
}

.talks-page h4 {
  font-size: 1.05rem;
  font-weight: 600;
}

/* Introductory text, notes, and descriptions */
.talks-page p,
.talks-page .talks-map-note,
.talks-page .talks-summary-label {
  font-family: inherit;
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--global-text-color-light);
}

/* Summary number */
.talks-page .talks-summary-number {
  font-family: inherit;
  font-size: 2.2rem;
  font-weight: 500;
  color: var(--global-text-color);
}

/* Featured talks */
.talks-page .featured-talk h3 {
  font-size: 1.05rem;
  font-weight: 500;
  color: var(--global-text-color);
}

.talks-page .featured-talk p {
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--global-text-color-light);
}

.talks-page .featured-talk-year {
  font-size: 0.85rem;
  font-weight: 400;
  color: var(--global-text-color-light);
}

/* Map popup styling */

.talk-map-popup-container .leaflet-popup-content-wrapper,
.talk-map-popup-container .leaflet-popup-tip {
  background: #ffffff;
}

.talk-map-popup-container .leaflet-popup-content {
  color: #000000;
  margin: 14px 16px;
  line-height: 1.5;
}

.talk-map-popup-title {
  margin-bottom: 0.25rem;
  color: #000000;
  font-size: 1rem;
  font-weight: 700;
}

.talk-map-popup-count {
  margin-bottom: 0.7rem;
  color: #000000;
  font-size: 0.85rem;
}

.talk-map-popup-list {
  max-height: 245px;
  overflow-y: auto;
  margin: 0;
  padding-left: 1.25rem;
  color: #000000;
}

.talk-map-popup-list li {
  margin-bottom: 0.7rem;
  color: #000000;
  font-size: 0.85rem;
  line-height: 1.5;
}

.talk-map-popup-list strong {
  color: #000000;
  font-weight: 700;
}

</style>

<script>
(function () {
  const talks = {{ site.data.talks | jsonify }};

  const mappedTalks = talks.filter(
    t => t.lat !== undefined && t.lon !== undefined
  );

  const grouped = {};

  mappedTalks.forEach(t => {
    const key = `${t.city || ''}, ${t.country || ''}`;

    if (!grouped[key]) {
      grouped[key] = {
        city: t.city || '',
        country: t.country || '',
        lat: t.lat,
        lon: t.lon,
        talks: []
      };
    }

    grouped[key].talks.push(t);
  });

  /*
   * Map setup
   */
  const map = L.map('talks-map', {
    scrollWheelZoom: false,
    zoomControl: true,
    worldCopyJump: true
  }).setView([20, 0], 2);

  L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    {
      attribution:
        'Tiles &copy; Esri — Sources: Esri, Garmin, USGS, NGA, EPA, USDA, NPS, and the GIS User Community',
      maxZoom: 19
    }
  ).addTo(map);

  /*
   * Red marker inspired by the original Leaflet/MapQuest style
   */
  const redMarkerIcon = L.icon({
    iconUrl:
      'data:image/svg+xml;charset=UTF-8,' +
      encodeURIComponent(`
        <svg xmlns="http://www.w3.org/2000/svg"
             width="28"
             height="40"
             viewBox="0 0 28 40">

          <path
            d="M14 1
               C6.8 1 1 6.8 1 14
               C1 23.5 14 39 14 39
               C14 39 27 23.5 27 14
               C27 6.8 21.2 1 14 1Z"
            fill="#e31b23"
            stroke="#111111"
            stroke-width="1.5"
          />

          <circle
            cx="14"
            cy="14"
            r="5"
            fill="#111111"
          />
        </svg>
      `),
    iconSize: [28, 40],
    iconAnchor: [14, 40],
    popupAnchor: [0, -36]
  });

  /*
   * Basic HTML escaping for popup content
   */
  function escapeHtml(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  /*
   * Create one marker for each location
   */
  Object.values(grouped).forEach(place => {
    const sortedTalks = place.talks.slice().sort((a, b) => {
      return Number(b.year) - Number(a.year);
    });

    const locationName = [
      place.city,
      place.country
    ]
      .filter(Boolean)
      .join(', ');

    const items = sortedTalks
      .map(t => {
        return `
          <li>
            <strong>${escapeHtml(t.year)}</strong>
            — ${escapeHtml(t.citation)}
          </li>
        `;
      })
      .join('');

    const popup = `
      <div class="talk-map-popup">
        <div class="talk-map-popup-title">
          ${escapeHtml(locationName)}
        </div>

        <div class="talk-map-popup-count">
          ${sortedTalks.length} presentation${sortedTalks.length === 1 ? '' : 's'}
        </div>

        <ul class="talk-map-popup-list">
          ${items}
        </ul>
      </div>
    `;

    L.marker([place.lat, place.lon], {
      icon: redMarkerIcon
    })
      .addTo(map)
      .bindPopup(popup, {
        maxWidth: 460,
        minWidth: 300,
        maxHeight: 380,
        className: 'talk-map-popup-container'
      });
  });
})();
</script>

</div>