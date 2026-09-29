---
layout: page
permalink: /projects/
title: Projects
description: Research projects, funded initiatives, and collaborations spanning transport equity, accessibility, sustainable mobility, cycling, and urban mobility.
nav: true
nav_order: 5
---

<div class="projects-page">

  {% assign projects = site.data.projects %}
  {% assign total_projects = projects | size %}
  {% assign pi_projects = projects | where: "role", "pi" %}
  {% assign coppi_projects = projects | where: "role", "co-pi" %}
  {% assign coapp_projects = projects | where: "role", "co-applicant" %}
  {% assign collaborator_projects = projects | where: "role", "collaborator" %}

  <div class="projects-stats">
    <div class="projects-stat">
      <div class="projects-stat-value">{{ total_projects }}</div>
      <div class="projects-stat-label">Projects</div>
    </div>
    <div class="projects-stat">
      <div class="projects-stat-value">{{ pi_projects | size | plus: coppi_projects.size }}</div>
      <div class="projects-stat-label">PI · Co-PI</div>
    </div>
    <div class="projects-stat">
      <div class="projects-stat-value">{{ coapp_projects | size }}</div>
      <div class="projects-stat-label">Co-Applicant</div>
    </div>
    <div class="projects-stat">
      <div class="projects-stat-value">{{ collaborator_projects | size }}</div>
      <div class="projects-stat-label">Collaborator</div>
    </div>
  </div>

  <div class="featured-projects-header">
    <h2>Featured projects</h2>
    <p>A selection of current and recent research projects.</p>
  </div>

  <div class="featured-projects">
    {% for project in projects %}
      {% if project.featured %}
        <article class="featured-project">
          <div class="featured-project-image">
            <img src="{{ project.image | relative_url }}" alt="{{ project.title }}">
          </div>
          <div class="featured-project-content">
            <div class="featured-project-year">{{ project.year }}</div>
            <h3>{{ project.title }}</h3>
            <div class="featured-project-tags">
              <span>{{ project.theme }}</span>
            </div>
          </div>
        </article>
      {% endif %}
    {% endfor %}
  </div>

  <div class="project-themes-header">
    <h2>Research themes</h2>
    <p>Explore projects by research area.</p>
  </div>

  <div class="project-themes">
    {% assign themes = "Accessibility and transport equity|Sustainable mobility & cycling|Food delivery" | split: "|" %}
    {% assign theme_images = "/assets/img/theme-accessibility.jpg|/assets/img/theme-cycling.jpg|/assets/img/theme-food-delivery.jpg" | split: "|" %}

    {% for theme in themes %}
      {% assign theme_index = forloop.index0 %}
      {% assign theme_projects = projects | where: "theme", theme %}

      <section class="project-theme">
        <div class="project-theme-image">
          <img src="{{ theme_images[theme_index] | relative_url }}" alt="{{ theme }}">
        </div>

        <div class="project-theme-main">
          <div class="project-theme-intro">
            <h3>{{ theme }}</h3>
          </div>

          <div class="project-theme-list">
            {% for project in theme_projects %}
              <details class="project-item">
                <summary>
                  <span class="project-item-title">{{ project.title }}</span>
                  <span class="project-item-year">{{ project.year }}</span>
                </summary>

                <div class="project-item-content">
                  {% case project.role %}
                    {% when "pi" %}
                      {% assign role_label = "Principal Investigator" %}
                    {% when "co-pi" %}
                      {% assign role_label = "Co-Principal Investigator" %}
                    {% when "co-applicant" %}
                      {% assign role_label = "Co-Applicant" %}
                    {% when "collaborator" %}
                      {% assign role_label = "Collaborator" %}
                  {% endcase %}

                  <p><strong>Role:</strong> {{ role_label }}</p>
                  <p><strong>Funded by:</strong> {{ project.funder }}</p>

                  {% if project.duration %}
                    <p><strong>Duration:</strong> {{ project.duration }}</p>
                  {% endif %}

                  <p><strong>Awarded:</strong> {{ project.awarded }}</p>

                  <div class="project-team">
                    <strong>Team:</strong>
                    <ul>
                      {% for member in project.team %}
                        <li>{{ member }}</li>
                      {% endfor %}
                    </ul>
                  </div>
                </div>
              </details>
            {% endfor %}
          </div>
        </div>
      </section>
    {% endfor %}
  </div>
</div>

<style>
.projects-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  margin: 1.5rem 0 3rem;
  border-top: 1px solid var(--global-divider-color);
  border-bottom: 1px solid var(--global-divider-color);
}

.projects-stat {
  padding: 2.25rem 1rem 2rem;
  text-align: center;
}

.projects-stat + .projects-stat {
  border-left: 1px solid var(--global-divider-color);
}

.projects-stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.1;
  color: var(--global-text-color);
}

.projects-stat-label {
  margin-top: 1.1rem;
  font-size: .95rem;
  font-weight: 400;
  letter-spacing: .03em;
  text-transform: uppercase;
  color: var(--global-text-color-light);
}

.featured-projects-header,
.project-themes-header {
  margin: 4rem 0 1.25rem;
}

.featured-projects-header h2,
.project-themes-header h2 {
  margin-bottom: .35rem;
  font-size: 1.35rem;
  font-weight: 500;
  color: var(--global-text-color);
}

.featured-projects-header p,
.project-themes-header p {
  margin: 0;
  font-size: .9rem;
  color: var(--global-text-color-light);
}

.featured-projects {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
}

.featured-project {
  overflow: hidden;
  border: 1px solid var(--global-divider-color);
  border-radius: 12px;
  background: var(--global-bg-color);
}

.featured-project-image {
  height: 180px;
  overflow: hidden;
}

.featured-project-image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.featured-project-content {
  padding: 1.15rem;
}

.featured-project-year {
  margin-bottom: .35rem;
  font-size: .85rem;
  color: var(--global-text-color-light);
}

.featured-project h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.4;
}

.featured-project-tags {
  margin-top: .9rem;
}

.featured-project-tags span {
  font-size: .75rem;
  color: var(--global-text-color-light);
}

.project-themes {
  margin-bottom: 4rem;
}

.project-theme {
  display: grid;
  grid-template-columns: minmax(220px, 30%) 1fr;
  column-gap: 2rem;
  padding: 2rem 0;
  border-top: 1px solid var(--global-divider-color);
}

.project-theme:last-child {
  border-bottom: 1px solid var(--global-divider-color);
}

.project-theme-image {
  height: 360px;
  overflow: hidden;
  border-radius: 12px;
}

.project-theme-image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.project-theme-main {
  min-width: 0;
}

.project-theme-intro h3 {
  margin: 0 0 1rem;
  font-size: 1.2rem;
  font-weight: 500;
}

.project-item {
  border-top: 1px solid var(--global-divider-color);
}

.project-item summary {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  cursor: pointer;
  padding: 1rem 0;
  list-style: none;
}

.project-item summary::-webkit-details-marker {
  display: none;
}

.project-item-title {
  font-size: .98rem;
  font-weight: 500;
  line-height: 1.45;
}

.project-item-year {
  flex: 0 0 auto;
  font-size: .85rem;
  color: var(--global-text-color-light);
}

.project-item-content {
  padding: 0 0 1.25rem;
  font-size: .9rem;
  line-height: 1.6;
  color: var(--global-text-color-light);
}

.project-item-content p {
  margin: .45rem 0;
}

.project-team {
  margin-top: .65rem;
}

.project-team ul {
  margin: .4rem 0 0 1.25rem;
}

.project-team li {
  margin-bottom: .25rem;
}

@media (max-width: 900px) {
  .projects-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .projects-stat:nth-child(3) {
    border-left: none;
    border-top: 1px solid var(--global-divider-color);
  }

  .projects-stat:nth-child(4) {
    border-top: 1px solid var(--global-divider-color);
  }

  .featured-projects {
    grid-template-columns: 1fr;
  }

  .project-theme {
    grid-template-columns: 1fr;
  }

  .project-theme-image {
    height: 220px;
    margin-bottom: 1.25rem;
  }
}

@media (max-width: 600px) {
  .projects-stats {
    grid-template-columns: 1fr;
  }

  .projects-stat + .projects-stat {
    border-left: none;
    border-top: 1px solid var(--global-divider-color);
  }

  .project-item summary {
    align-items: flex-start;
  }
}
</style>