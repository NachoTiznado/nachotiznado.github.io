---
layout: page
permalink: /talks/
title: Talks
description: Conferences, invited lectures, keynote presentations, workshops, and guest lectures.
nav: true
nav_order: 4
---

<div class="talks-intro">
  <p>A selection of conferences, invited lectures, keynote presentations, workshops, and guest lectures.</p>
</div>

<div class="talks-summary">
  <div class="talks-summary-number">{{ site.data.talks | size }}</div>
  <div class="talks-summary-label">Presentations · 2016–2026</div>
</div>

## Presentation map

<p class="talks-map-note">Explore the places where I have presented. Select a marker to see the presentations associated with that location.</p>

<div id="talks-map" class="talks-map" aria-label="Interactive map of presentation locations"></div>

## Featured talks

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

## All talks

{% assign categories = "Conference and symposia presentations|Invited lectures" | split: "|" %}
{% assign presentation_years = "2026,2025,2024,2023,2022,2021,2020,2019,2018,2017,2016" | split: "," %}

{% for category in categories %}
  <h3>{{ category }}</h3>

  {% for year in presentation_years %}
    {% assign year_has_talks = false %}

    {% for talk in site.data.talks %}
      {% if talk.category == category %}
        {% assign talk_year = talk.year | append: "" %}
        {% if talk_year == year %}
          {% assign year_has_talks = true %}
        {% endif %}
      {% endif %}
    {% endfor %}

    {% if year_has_talks %}
      <h4>{{ year }}</h4>

      <ul class="talk-list">
        {% for talk in site.data.talks %}
          {% if talk.category == category %}
            {% assign talk_year = talk.year | append: "" %}
            {% if talk_year == year %}
              <li>{{ talk.citation }}</li>
            {% endif %}
          {% endif %}
        {% endfor %}
      </ul>
    {% endif %}
  {% endfor %}
{% endfor %}

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
/* Softer, more polished map appearance */
.talks-map {
  width: 100%;
  height: 500px;
  border-radius: 16px;
  overflow: hidden;
  margin: 1rem 0 2.5rem;
  border: 1px solid var(--global-divider-color);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

/* Improve marker popups */
.talk-map-popup-container .leaflet-popup-content-wrapper,
.talk-map-popup-container .leaflet-popup-tip {
  background: #ffffff;
}

.talk-map-popup-container .leaflet-popup-content {
  color: #000000;
  margin: 14px 16px;
  line-height: 1.5;
}

.talk-map-popup {
  color: #000000;
  font-size: 0.9rem;
}

.talk-map-popup-title {
  color: #000000;
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 0.15rem;
}

.talk-map-popup-count {
  color: #000000;
  font-size: 0.82rem;
  margin-bottom: 0.65rem;
  opacity: 0.7;
}

.talk-map-popup-list {
  max-height: 245px;
  overflow-y: auto;
  padding-left: 1.15rem;
  margin: 0;
}

.talk-map-popup-list li {
  color: #000000;
  margin-bottom: 0.7rem;
  padding-right: 0.35rem;
}

.talk-map-popup-list strong {
  color: #000000;
  font-weight: 700;
}

.talk-map-popup-list span {
  color: #000000;
}

/* Ensure the popup scrollbar is visually usable */
.talk-map-popup-list::-webkit-scrollbar {
  width: 7px;
}

.talk-map-popup-list::-webkit-scrollbar-thumb {
  background: #b5b5b5;
  border-radius: 10px;
}

.talk-map-popup-list::-webkit-scrollbar-track {
  background: #eeeeee;
}
</style>

<script>
(function () {
  const talks = {{ site.data.talks | jsonify }};
  const mappedTalks = talks.filter(t => t.lat !== undefined && t.lon !== undefined);
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

  const map = L.map('talks-map', {
    scrollWheelZoom: false,
    zoomControl: true
  }).setView([20, 0], 2);

  /*
   * CartoDB Voyager provides a softer, cleaner map style
   * than the standard OpenStreetMap tiles.
   */
  L.tileLayer(
    'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    {
      attribution:
        '&copy; OpenStreetMap contributors &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }
  ).addTo(map);

  Object.values(grouped).forEach(place => {
    const items = place.talks
      .sort((a, b) => b.year - a.year)
      .map(t => `
        <li>
          <strong>${t.year}</strong>
          <span>${t.citation}</span>
        </li>
      `)
      .join('');

    const popup = `
      <div class="talk-map-popup">
        <div class="talk-map-popup-title">
          ${place.city}${place.country ? ', ' + place.country : ''}
        </div>

        <div class="talk-map-popup-count">
          ${place.talks.length} presentation${place.talks.length === 1 ? '' : 's'}
        </div>

        <ul class="talk-map-popup-list">
          ${items}
        </ul>
      </div>
    `;

    L.marker([place.lat, place.lon])
      .addTo(map)
      .bindPopup(popup, {
        maxWidth: 460,
        minWidth: 300,
        maxHeight: 360,
        className: 'talk-map-popup-container'
      });
  });
})();
</script>
