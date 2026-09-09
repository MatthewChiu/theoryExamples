---
layout: default
title: Music Theory Examples
---

# Music Theory Examples

{% for category in site.data.theory %}

## {{ category.category }}

{% for example in category.examples %}

{% assign song = site.data.songs[example.song] %}

### [{{ song.composer }} — "{{ song.title }}"]({{ song.page | relative_url }})

<div class="techniques">
{% for technique in example.techniques %}
<span>{{ technique }}</span>
{% endfor %}
</div>

{% endfor %}
{% endfor %}