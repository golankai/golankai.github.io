---
title: IdioLink
permalink: /idiolink/
---

{% include custom_style.html %}

<style>
  .article--page > h1:first-child { display: none; }

  .idiolink-hero {
    max-width: 680px;
    margin: 0 auto 28px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 36px 40px;
    text-align: center;
  }
  .typeset .idiolink-venue {
    display: inline-block;
    font-size: 0.8em;
    font-weight: 700;
    line-height: 1.4;
    letter-spacing: 0.4px;
    color: #1a4b8c;
    background: #e6eef8;
    border-radius: 999px;
    padding: 4px 14px;
    margin: 0 0 16px;
  }
  .typeset .idiolink-title {
    font-size: clamp(1.5em, 4.5vw, 1.9em);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -0.6px;
    color: #1a4b8c;
    margin: 0 0 14px;
    padding: 0;
  }
  .typeset .idiolink-authors {
    font-size: 0.98em;
    font-weight: 500;
    line-height: 1.6;
    color: #64748b;
    margin: 0 0 28px;
    padding: 0;
  }
  .idiolink-links {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
  }
  .idiolink-links a {
    display: inline-block;
    min-width: 7em;
    padding: 10px 22px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95em;
    text-align: center;
    text-decoration: none !important;
    color: #fff !important;
    background: #1a4b8c;
    transition: background 0.15s;
  }
  .idiolink-links a:hover {
    background: #6a9bd0;
    color: #fff !important;
  }

  .typeset .idiolink-back {
    text-align: center;
    font-size: 0.9em;
    margin: 0;
  }

  @media (max-width: 640px) {
    .idiolink-hero { padding: 28px 20px; }
    .idiolink-links { gap: 8px; }
    .idiolink-links a { min-width: 0; padding: 10px 16px; }
  }
</style>

<div class="idiolink-hero">
  <p class="idiolink-venue">EMNLP 2026</p>
  <p class="idiolink-title">IdioLink: Retrieving Meaning Beyond Words Across Idiomatic and Literal Expressions</p>
  <p class="idiolink-authors">Kai Golan Hashiloni, Daniel Fadlon, Lior Livyatan, Ofri Hefetz, Jiahuan Pei, Kfir Bar</p>

  <div class="idiolink-links">
    <a href="https://drive.google.com/file/d/1SBXyarzc8NnTYHsTew2yP01qXABICHRm/view?usp=sharing">Paper</a>
    <a href="https://github.com/Intellexus-DSI/IdioLink">Code</a>
    <a href="https://huggingface.co/datasets/Intellexus/IdioLink">Dataset</a>
  </div>
</div>

<p class="idiolink-back"><a href="/">← Kai Golan Hashiloni</a></p>
