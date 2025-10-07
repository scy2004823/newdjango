/* Blackbit Web Encryptor - Frontend Logic */
(function(){
  const $ = (sel) => document.querySelector(sel);
  const $$ = (sel) => Array.from(document.querySelectorAll(sel));

  const termBody = $('#terminal-body');
  const cursor = $('#cursor');

  function timeStr() {
    const d = new Date();
    return d.toLocaleTimeString();
  }

  function logLine(msg, type='ok') {
    const line = document.createElement('div');
    line.className = `log-line ${type}`;
    line.innerHTML = `<span class="log-time">[${timeStr()}]</span><span class="log-tag">[BB]</span> ${msg}`;
    termBody.insertBefore(line, cursor);
    termBody.scrollTop = termBody.scrollHeight;
  }

  // Optional SFX: beep via WebAudio
  function beep(freq=620, dur=80) {
    try{
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'square';
      osc.frequency.value = freq;
      gain.gain.value = 0.04;
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      setTimeout(() => { osc.stop(); ctx.close(); }, dur);
    }catch(e){/* ignore */}
  }

  // Boot Sequence
  function bootSequence(){
    const lines = [
      'Initializing Blackbit Secure Node…',
      'Loading crypto modules…',
      'Checking key integrity…',
      'Wiring UI subsystems…',
      'System Ready.'
    ];
    let i = 0;
    const iv = setInterval(()=>{
      if (i < lines.length) {
        logLine(lines[i]);
        beep(520 + i*50, 50);
        i++;
      } else {
        clearInterval(iv);
      }
    }, 300);
  }

  // Typewriter subtitle via Typed.js
  function initTyped(){
    if (window.Typed) {
      new window.Typed('#typed-subtitle', {
        strings: [
          'Fernet-grade encryption. Browser-friendly.',
          'Encrypt any file. Keep your key safe.',
          'Decrypt with your .key. No server storage.'
        ],
        typeSpeed: 30,
        backSpeed: 16,
        backDelay: 1200,
        loop: true
      });
    }
  }

  // Tabs
  function initTabs(){
    const btnEnc = $('#tab-encrypt');
    const btnDec = $('#tab-decrypt');
    const panelEnc = $('#panel-encrypt');
    const panelDec = $('#panel-decrypt');

    function activate(which){
      $$('.tab').forEach(b=>b.classList.remove('active'));
      $$('.panel').forEach(p=>p.classList.remove('active'));
      if (which === 'enc') { btnEnc.classList.add('active'); panelEnc.classList.add('active'); }
      else { btnDec.classList.add('active'); panelDec.classList.add('active'); }
    }

    btnEnc.addEventListener('click', ()=> activate('enc'));
    btnDec.addEventListener('click', ()=> activate('dec'));
  }

  // Dropzones
  function makeDropzone(zone, input){
    function over(e){ e.preventDefault(); zone.classList.add('dragover'); }
    function out(e){ e.preventDefault(); zone.classList.remove('dragover'); }
    function drop(e){ e.preventDefault(); zone.classList.remove('dragover'); if (e.dataTransfer.files && e.dataTransfer.files[0]) input.files = e.dataTransfer.files; }
    zone.addEventListener('dragover', over);
    zone.addEventListener('dragleave', out);
    zone.addEventListener('drop', drop);
  }

  // Actions: Encrypt
  function initEncrypt(){
    const drop = $('#enc-drop');
    const fileInput = $('#enc-file');
    const btn = $('#btn-encrypt');
    const results = $('#enc-results');
    const stats = $('#enc-stats');
    const dlEnc = $('#dl-encrypted');
    const dlKey = $('#dl-key');

    makeDropzone(drop, fileInput);
    const ioEnc = drop.closest('.io');

    async function doEncrypt(){
      const file = fileInput.files && fileInput.files[0];
      if (!file) { logLine('No file selected for encryption', 'err'); beep(220, 120); return; }

      btn.classList.add('working');
      logLine(`Encrypting: ${file.name} (${(file.size/1024).toFixed(1)} KB)`);
      beep(640, 60);

      const fd = new FormData();
      fd.append('file', file, file.name);

      try {
        const t0 = performance.now();
        const res = await fetch('/encrypt', { method: 'POST', body: fd });
        const data = await res.json();
        const dt = (performance.now() - t0) / 1000;

        if (!data.ok) throw new Error(data.error || 'Encryption failed');
        logLine('Key generated [OK]');
        logLine('File encrypted successfully [OK]');

        // Populate results
        dlEnc.href = data.encrypted.url;
        dlEnc.download = data.encrypted.display_name;
        dlKey.href = data.key.url;
        dlKey.download = data.key.display_name;
        stats.innerHTML = `
          <div>Original: <strong>${data.stats.original_name}</strong></div>
          <div>Size: <strong>${(data.stats.original_size/1024).toFixed(1)} KB</strong> → Encrypted: <strong>${(data.stats.encrypted_size/1024).toFixed(1)} KB</strong></div>
          <div>Time (server): <strong>${data.stats.elapsed_seconds}s</strong> • Total RTT: <strong>${dt.toFixed(3)}s</strong></div>
        `;
        if (ioEnc) ioEnc.hidden = true;
        results.hidden = false;
        beep(760, 120);
      } catch (e) {
        logLine('Encryption error: ' + e.message, 'err');
        beep(200, 160);
      } finally {
        btn.classList.remove('working');
      }
    }

    btn.addEventListener('click', doEncrypt);
  }

  // Actions: Decrypt
  function initDecrypt(){
    const dropEnc = $('#dec-drop-encrypted');
    const dropKey = $('#dec-drop-key');
    const fileEnc = $('#dec-file-encrypted');
    const fileKey = $('#dec-file-key');
    const btn = $('#btn-decrypt');
    const results = $('#dec-results');
    const stats = $('#dec-stats');
    const dlDec = $('#dl-decrypted');

    makeDropzone(dropEnc, fileEnc);
    makeDropzone(dropKey, fileKey);

    const ioDec = dropEnc.closest('.io');

    async function doDecrypt(){
      const fEnc = fileEnc.files && fileEnc.files[0];
      const fKey = fileKey.files && fileKey.files[0];
      if (!fEnc || !fKey) { logLine('Please provide both .encrypted file and .key', 'err'); beep(220, 120); return; }

      btn.classList.add('working');
      logLine(`Decrypting: ${fEnc.name}`);
      beep(520, 60);

      const fd = new FormData();
      fd.append('encrypted', fEnc, fEnc.name);
      fd.append('key', fKey, fKey.name);

      try {
        const t0 = performance.now();
        const res = await fetch('/decrypt', { method: 'POST', body: fd });
        const data = await res.json();
        const dt = (performance.now() - t0) / 1000;

        if (!data.ok) throw new Error(data.error || 'Decryption failed');
        logLine('Key accepted [OK]');
        logLine('File decrypted successfully [OK]');

        dlDec.href = data.decrypted.url;
        dlDec.download = data.decrypted.display_name;
        stats.innerHTML = `
          <div>Decryption time (server): <strong>${data.stats.elapsed_seconds}s</strong> • Total RTT: <strong>${dt.toFixed(3)}s</strong></div>
          <div>Output size: <strong>${(data.decrypted.size_bytes/1024).toFixed(1)} KB</strong></div>
        `;
        if (ioDec) ioDec.hidden = true;
        results.hidden = false;
        beep(760, 120);
      } catch (e) {
        logLine('Decryption error: ' + e.message, 'err');
        beep(200, 160);
      } finally {
        btn.classList.remove('working');
      }
    }

    btn.addEventListener('click', doDecrypt);
  }

  // Matrix rain overlay
  function initMatrix(){
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    function resize(){ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
    resize();
    window.addEventListener('resize', resize);

    const letters = 'アカサタナハマヤラワ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const fontSize = 16;
    let columns = Math.floor(canvas.width / fontSize);
    let drops = new Array(columns).fill(1);

    function draw(){
      if (columns !== Math.floor(canvas.width / fontSize)) {
        columns = Math.floor(canvas.width / fontSize);
        drops = new Array(columns).fill(1);
      }
      ctx.fillStyle = 'rgba(0, 0, 0, 0.08)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = '#00ffbf';
      ctx.font = fontSize + 'px monospace';
      for (let i = 0; i < drops.length; i++) {
        const text = letters[Math.floor(Math.random() * letters.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);
        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      }
      requestAnimationFrame(draw);
    }
    requestAnimationFrame(draw);
  }

  // Three.js neon grid + cube
  function initThree(){
    const canvas = document.getElementById('three-bg');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));

    // Grid plane
    const gridHelper = new THREE.GridHelper(80, 60, 0x00ffc6, 0x00ffc6);
    gridHelper.material.opacity = 0.12;
    gridHelper.material.transparent = true;
    scene.add(gridHelper);

    // Wireframe cube
    const boxGeo = new THREE.BoxGeometry(6, 6, 6);
    const boxMat = new THREE.MeshBasicMaterial({ color: 0x04f06a, wireframe: true, transparent: true, opacity: 0.6 });
    const cube = new THREE.Mesh(boxGeo, boxMat);
    cube.position.set(0, 6, 0);
    scene.add(cube);

    camera.position.set(12, 16, 22);
    camera.lookAt(0, 0, 0);

    function animate(){
      cube.rotation.x += 0.0035;
      cube.rotation.y += 0.0045;
      gridHelper.rotation.y += 0.0007;
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    }
    animate();

    function onResize(){
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }
    window.addEventListener('resize', onResize);
  }

  function init(){
    initTyped();
    bootSequence();
    initTabs();
    initEncrypt();
    initDecrypt();
    initThree();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
