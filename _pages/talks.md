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
.talks-summary { display:flex; align-items:baseline; gap:1rem; margin:1.5rem 0 2rem; }
.talks-summary-number { font-size:2.5rem; font-weight:700; line-height:1; }
.talks-summary-label { opacity:.7; }
.talks-map { width:100%; height:480px; border-radius:12px; overflow:hidden; margin:1rem 0 2.5rem; border:1px solid var(--global-divider-color); }
.talks-map-note { opacity:.75; }
.featured-talks { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:1rem; margin:1rem 0 2.5rem; }
.featured-talk { padding:1.15rem; border:1px solid var(--global-divider-color); border-radius:12px; }
.featured-talk-year { font-size:.85rem; opacity:.65; margin-bottom:.35rem; }
.featured-talk h3 { font-size:1.05rem; margin:.2rem 0 .7rem; }
.featured-talk p { font-size:.9rem; opacity:.78; margin:0; }
.talk-list { padding-left:1.25rem; }
.talk-list li { margin-bottom:.8rem; }

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

</style>

<script>
(function () {
  const talks = {{ site.data.talks | jsonify }};
  const mappedTalks = talks.filter(t => t.lat !== undefined && t.lon !== undefined);
  const grouped = {};

  mappedTalks.forEach(t => {
    const key = `${t.city || ''}, ${t.country || ''}`;
    if (!grouped[key]) grouped[key] = { city: t.city || '', country: t.country || '', lat: t.lat, lon: t.lon, talks: [] };
    grouped[key].talks.push(t);
  });

  const map = L.map('talks-map', { scrollWheelZoom: false }).setView([20, 0], 2);
  L.tileLayer(
  'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  {
    attribution: '&copy; OpenStreetMap contributors',
    maxZoom: 19
  }
).addTo(map);

  Object.values(grouped).forEach(place => {
    const items = place.talks.map(t => `<li><strong>${t.year}</strong> — ${t.citation}</li>`).join('');
    const popup = `<strong>${place.city}${place.country ? ', ' + place.country : ''}</strong><br><small>${place.talks.length} presentation(s)</small><ul>${items}</ul>`;
    L.marker([place.lat, place.lon]).addTo(map).bindPopup(popup, { maxWidth: 420 });
  });
})();
</script>
