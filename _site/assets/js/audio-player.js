(function () {
  var el = document.getElementById('post-audio-el');
  if (!el) return;

  var playBtn   = document.getElementById('post-audio-play');
  var speedBtn  = document.getElementById('post-audio-speed');
  var track     = document.getElementById('post-audio-track');
  var fill      = document.getElementById('post-audio-fill');
  var thumb     = document.getElementById('post-audio-thumb');
  var currentEl = document.getElementById('post-audio-current');
  var durationEl = document.getElementById('post-audio-duration');
  var playIcon  = playBtn.querySelector('.post-audio-icon--play');
  var pauseIcon = playBtn.querySelector('.post-audio-icon--pause');

  var SPEEDS = [0.75, 1, 1.2, 1.5, 2];
  var speedIdx = 2;
  var loaded = false;
  var dragging = false;

  try {
    var s = parseFloat(localStorage.getItem('post-audio-speed'));
    var i = SPEEDS.indexOf(s);
    if (i !== -1) speedIdx = i;
  } catch (e) {}

  speedBtn.textContent = SPEEDS[speedIdx] + '×';

  function fmt(sec) {
    var m = Math.floor(sec / 60);
    var s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  function setPlaying(on) {
    playBtn.setAttribute('aria-pressed', on ? 'true' : 'false');
    playBtn.setAttribute('aria-label', on ? 'Pause narration' : 'Play narration');
    playIcon.style.display  = on ? 'none'  : 'block';
    pauseIcon.style.display = on ? 'block' : 'none';
  }

  function syncProgress() {
    if (!el.duration) return;
    var pct = (el.currentTime / el.duration) * 100;
    fill.style.width   = pct + '%';
    thumb.style.left   = pct + '%';
    track.setAttribute('aria-valuenow', Math.round(pct));
    currentEl.textContent = fmt(el.currentTime);
    try {
      sessionStorage.setItem('audio-pos:' + location.pathname, el.currentTime);
    } catch (e) {}
  }

  function seekTo(clientX) {
    var rect = track.getBoundingClientRect();
    var pct  = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
    el.currentTime = pct * el.duration;
    syncProgress();
  }

  function ensureLoaded() {
    if (!loaded) { el.load(); loaded = true; }
  }

  // Play / pause
  playBtn.addEventListener('click', function () {
    ensureLoaded();
    el.paused ? el.play() : el.pause();
  });

  el.addEventListener('play',  function () { setPlaying(true); });
  el.addEventListener('pause', function () { setPlaying(false); });
  el.addEventListener('ended', function () {
    setPlaying(false);
    el.currentTime = 0;
    syncProgress();
  });

  el.addEventListener('loadedmetadata', function () {
    durationEl.textContent = fmt(el.duration);
    el.playbackRate = SPEEDS[speedIdx];
    try {
      var saved = parseFloat(sessionStorage.getItem('audio-pos:' + location.pathname));
      if (saved && saved < el.duration - 5) el.currentTime = saved;
    } catch (e) {}
    syncProgress();
  });

  el.addEventListener('timeupdate', syncProgress);

  // Mouse seek on track
  track.addEventListener('mousedown', function (e) {
    ensureLoaded();
    dragging = true;
    seekTo(e.clientX);
  });
  document.addEventListener('mousemove', function (e) {
    if (dragging) seekTo(e.clientX);
  });
  document.addEventListener('mouseup', function () { dragging = false; });

  // Touch seek
  track.addEventListener('touchstart', function (e) {
    ensureLoaded();
    e.preventDefault();
    seekTo(e.touches[0].clientX);
  }, { passive: false });
  track.addEventListener('touchmove', function (e) {
    e.preventDefault();
    seekTo(e.touches[0].clientX);
  }, { passive: false });

  // Keyboard on track
  track.addEventListener('keydown', function (e) {
    if (!el.duration) return;
    if (e.key === 'ArrowLeft')  el.currentTime = Math.max(0, el.currentTime - 10);
    if (e.key === 'ArrowRight') el.currentTime = Math.min(el.duration, el.currentTime + 10);
    syncProgress();
  });

  // Speed cycle
  speedBtn.addEventListener('click', function () {
    speedIdx = (speedIdx + 1) % SPEEDS.length;
    var speed = SPEEDS[speedIdx];
    el.playbackRate = speed;
    speedBtn.textContent = speed + '×';
    try { localStorage.setItem('post-audio-speed', speed); } catch (e) {}
  });
})();
