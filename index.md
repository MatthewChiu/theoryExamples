---
layout: default
title: Music Theory Examples
---

<h1>Music Theory</h1>

{% for category in site.data.theory %}
<h2>{{ category.category }}</h2>

{% if category.examples %}
<ul class="theory-list">
{% for example in category.examples %}
{% assign song = site.data.songs[example.song] %}
<li class="theory-item">
{% if song.page %}
<a href="{{ song.page | relative_url }}" class="theory-title">
{{ song.composer }} &mdash; "{{ song.title }}"
</a>
{% else %}
<span class="theory-title theory-title-nolink">
{{ song.composer }} &mdash; "{{ song.title }}"
</span>
{% endif %}
<div class="techniques-list">
{% for technique in example.techniques %}
<span class="technique-badge">{{ technique }}</span>
{% endfor %}
</div>
</li>
{% endfor %}
</ul>
{% endif %}

{% if category.subcategories %}
{% for subcategory in category.subcategories %}
<h3 class="theory-subcategory">{{ subcategory[0] }}</h3>
<ul class="theory-list">
{% for example in subcategory[1].examples %}
{% assign song = site.data.songs[example.song] %}
<li class="theory-item">
{% if song.page %}
<a href="{{ song.page | relative_url }}" class="theory-title">
{{ song.composer }} &mdash; "{{ song.title }}"
</a>
{% else %}
<span class="theory-title theory-title-nolink">
{{ song.composer }} &mdash; "{{ song.title }}"
</span>
{% endif %}
<div class="techniques-list">
{% for technique in example.techniques %}
<span class="technique-badge">{{ technique }}</span>
{% endfor %}
</div>
</li>
{% endfor %}
</ul>
{% endfor %}
{% endif %}
{% endfor %}
