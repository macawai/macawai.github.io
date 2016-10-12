---
layout: default
title: Home
permalink: /news/
paginate:
  collection: news
  per_page: 2
  permalink: /page/:num
  reversed: true
---

<div>
  <h1><a href="/news">News</a></h1>
  {% for item in paginator.news %}
  <article>
    <a href="{{ item.source }}" target="_blank" rel="noopener">
      {{ item.title }}
    </a>
    <!--div>
        {{ item.excerpt }}
    </div -->
  </article>
  {% endfor %}
</div>

<div class="pagination">
  {% if paginator.next_page %}
    <a class="pagination-item older" href="{{ paginator.next_page_path | prepend: site.baseurl }}">Older</a>
  {% else %}
    <span class="pagination-item older">Older</span>
  {% endif %}
  {% if paginator.previous_page %}
    <a class="pagination-item newer" href="{{ paginator.previous_page_path | prepend: site.baseurl }}">Newer</a>
  {% else %}
    <span class="pagination-item newer">Newer</span>
  {% endif %}
</div>
