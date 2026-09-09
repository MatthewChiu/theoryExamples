---
layout: default
title: Music Theory Examples
---

# Music Theory Examples

{% for category in site.data.theory %}

## {{ category.category }}

{% for example in category.examples %}

{% assign song = site.data.songs | where: "id", example.song | first %}

<div class="theory-entry">

<a href="{{ song.page }}" class="example-title">
  {{ song.composer }} — "{{ song.title }}"
</a>

<div class="techniques">
{% for technique in example.techniques %}
<span>{{ technique }}</span>
{% endfor %}
</div>

</div>

{% endfor %}
{% endfor %}