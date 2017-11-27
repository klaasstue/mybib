<div class="reveal" id="detail-{{ item['pk'] }}" data-reveal>
  {{ item['content'] }}
  <button class="close-button" data-close aria-label="Close reveal" type="button">
    <img src="{{ url_for('static', filename='drop-up-arrow.svg') }}" width="12px">
  </button>
</div>
