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
  {% assign pi_projects = projects | where_exp: "project", "project.role == 'pi' or project.role == 'co-pi' or project.role == 'co-lead'" %}
  {% assign coapp_projects = projects | where: "role", "co-applicant" %}
  {% assign collaborator_projects = projects | where: "role", "collaborator" %}

  <div class="projects-stats">

    <div class="projects-stat">
      <div class="projects-stat-value">{{ total_projects }}</div>
      <div class="projects-stat-label">Projects</div>
    </div>

    <div class="projects-stat">
      <div class="projects-stat-value">{{ pi_projects | size }}</div>
      <div class="projects-stat-label">PI · Co-PI · Co-lead</div>
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
        <div class="featured-project">
          <div class="featured-project-image">
            <div class="featured-project-placeholder"></div>
          </div>
          <div class="featured-project-content">
            <div class="featured-project-year">{{ project.year }}</div>
            <h3>{{ project.title }}</h3>
            <div class="featured-project-tags">
              <span>{{ project.theme }}</span>
            </div>
          </div>
        </div>
      {% endif %}
    {% endfor %}
  </div>

  <div class="project-themes-header">
    <h2>Research themes</h2>
    <p>Explore projects by research area.</p>
  </div>

  {% assign themes = "Accessibility and transport equity|Sustainable mobility & cycling|Food delivery|Teaching" | split: "|" %}

  <div class="project-themes">

    {% for theme in themes %}
      {% assign theme_projects = projects | where: "theme", theme %}

      <details class="project-theme">
        <summary>
          <div>
            <h3>{{ theme }}</h3>
            <span>{{ theme_projects | size }} projects</span>
          </div>
        </summary>

        <div class="project-theme-content">
          {% for project in theme_projects %}
            <div class="project-item">

              <div class="project-item-year">
                {% if project.year %}
                  {{ project.year }}
                {% endif %}
              </div>

              <div class="project-item-content">
                <h4>{{ project.title }}</h4>

                {% case project.role %}
                  {% when "pi" %}
                    <p><strong>Role:</strong> Principal Investigator</p>
                  {% when "co-pi" %}
                    <p><strong>Role:</strong> Co-Principal Investigator</p>
                  {% when "co-lead" %}
                    <p><strong>Role:</strong> Co-lead</p>
                  {% when "co-applicant" %}
                    <p><strong>Role:</strong> Co-Applicant</p>
                  {% when "collaborator" %}
                    <p><strong>Role:</strong> Collaborator</p>
                  {% when "other" %}
                    <p><strong>Role:</strong> Other</p>
                {% endcase %}
              </div>

            </div>
          {% endfor %}
        </div>
      </details>
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
  font-size: 0.95rem;
  font-weight: 400;
  letter-spacing: 0.03em;
  text-transform: uppercase;
  color: var(--global-text-color-light);
}

.featured-projects-header,
.project-themes-header {
  margin: 4rem 0 1.25rem;
}

.featured-projects-header h2,
.project-themes-header h2 {
  margin-bottom: 0.35rem;
  font-size: 1.35rem;
  font-weight: 500;
  color: var(--global-text-color);
}

.featured-projects-header p,
.project-themes-header p {
  margin: 0;
  font-size: 0.9rem;
  font-weight: 400;
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

.featured-project-placeholder {
  width: 100%;
  height: 100%;
  background: var(--global-divider-color);
}

.featured-project-content {
  padding: 1.15rem;
}

.featured-project-year {
  margin-bottom: 0.35rem;
  font-size: 0.85rem;
  color: var(--global-text-color-light);
}

.featured-project h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 500;
  line-height: 1.4;
}

.featured-project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 0.9rem;
}

.featured-project-tags span {
  padding: 0.2rem 0.5rem;
  border: 1px solid var(--global-divider-color);
  border-radius: 999px;
  font-size: 0.72rem;
  color: var(--global-text-color-light);
}

.project-themes {
  margin-bottom: 4rem;
}

.project-theme {
  border-top: 1px solid var(--global-divider-color);
}

.project-theme:last-child {
  border-bottom: 1px solid var(--global-divider-color);
}

.project-theme summary {
  cursor: pointer;
  padding: 1.25rem 0;
  list-style: none;
}

.project-theme summary::-webkit-details-marker {
  display: none;
}

.project-theme summary > div {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
}

.project-theme h3 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 500;
}

.project-theme summary span {
  font-size: 0.85rem;
  color: var(--global-text-color-light);
}

.project-theme-content {
  padding: 0 0 1.5rem;
}

.project-item {
  display: grid;
  grid-template-columns: 70px 1fr;
  gap: 1rem;
  padding: 1rem 0;
  border-top: 1px solid var(--global-divider-color);
}

.project-item-year {
  font-size: 0.85rem;
  color: var(--global-text-color-light);
}

.project-item h4 {
  margin: 0 0 0.5rem;
  font-size: 0.98rem;
  font-weight: 500;
  line-height: 1.45;
}

.project-item p {
  margin: 0;
  font-size: 0.9rem;
  color: var(--global-text-color-light);
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
}

@media (max-width: 600px) {
  .projects-stats {
    grid-template-columns: 1fr;
  }

  .projects-stat + .projects-stat {
    border-left: none;
    border-top: 1px solid var(--global-divider-color);
  }

  .project-item {
    grid-template-columns: 1fr;
    gap: 0.25rem;
  }
}
</style>
