---
layout: default
title: Music Theory Examples
---

# Music Theory

SONG TEST:

{% assign test_song = site.data.songs["shes-always-a-woman"] %}

{{ test_song.composer }}
{{ test_song.title }}

{% for category in site.data.theory %}

## {{ category.category }}

{% for example in category.examples %}

{% assign song = site.data.songs[example.song] %}

### [{{ song.composer }} — "{{ song.title }}"]({{ song.page }})

<div class="techniques">
{% for technique in example.techniques %}
<span>{{ technique }}</span>
{% endfor %}
</div>

{% endfor %}
{% endfor %}