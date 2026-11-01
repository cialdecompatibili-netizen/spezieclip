---
layout: single
classes: wide
author_profile: false
title: "Thank you"
description: "Thank you for your order of spices and herbs. We will email you the details."
ecommerce: true
noindex: true
ref: shop-grazie
lang: en
locale: en
tr: tradotto
tr_hash: 16v33ee
permalink: /en/grazie/
---
{% if site.ecommerce == true %}
Thank you for your order! We will write to you shortly with delivery details.
{% else %}
<p>The shop is not available at the moment.</p>
{% endif %}
