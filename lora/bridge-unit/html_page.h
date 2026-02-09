// --- HTML / JAVASCRIPT (2x6 tuki) ---
const char* htmlPage = R"rawliteral(
<!DOCTYPE html><html><head>
<meta charset="utf-8">
<title>OH8KVA 2x6 Matrix</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font-family: sans-serif; text-align: center; background: #1a1a1a; color: #eee; margin: 0; padding: 20px; }
  .matrix-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; }
  .rig-box { border: 1px solid #444; padding: 15px; border-radius: 10px; background: #2a2a2a; width: 300px; }
  .rig-a { border-top: 5px solid #28a745; }
  .rig-b { border-top: 5px solid #007bff; }
  button { padding: 15px; margin: 5px; font-size: 16px; width: 80px; cursor: pointer; border-radius: 5px; border: 1px solid #555; background: #444; color: white; transition: 0.2s; }
  button.active-a { background: #28a745; border-color: #2ecc71; box-shadow: 0 0 10px #28a745; }
  button.active-b { background: #007bff; border-color: #33b5ff; box-shadow: 0 0 10px #007bff; }
  button:disabled { opacity: 0.3; cursor: not-allowed; }
  #status { margin-top: 20px; font-size: 0.8em; color: #777; }
</style></head>
<body>
  <h2>OH8KVA 2x6 Antennimatriisi</h2>
  <div class="matrix-container">
    <div class="rig-box rig-a">
      <h3>RIG A</h3>
      <button id="A1" onclick="send('A1')">1</button>
      <button id="A2" onclick="send('A2')">2</button>
      <button id="A3" onclick="send('A3')">3</button><br>
      <button id="A4" onclick="send('A4')">4</button>
      <button id="A5" onclick="send('A5')">5</button>
      <button id="A6" onclick="send('A6')">6</button><br>
      <button id="A0" onclick="send('A-')" style="width:174px; margin-top:10px;">OFF</button>
    </div>
    <div class="rig-box rig-b">
      <h3>RIG B</h3>
      <button id="B1" onclick="send('B1')">1</button>
      <button id="B2" onclick="send('B2')">2</button>
      <button id="B3" onclick="send('B3')">3</button><br>
      <button id="B4" onclick="send('B4')">4</button>
      <button id="B5" onclick="send('B5')">5</button>
      <button id="B6" onclick="send('B6')">6</button><br>
      <button id="B0" onclick="send('B-')" style="width:174px; margin-top:10px;">OFF</button>
    </div>
    <div class="rig-box" style="width: 630px; margin-top: 20px; border-top: 5px solid #f1c40f;">
      <h3>LÄHETYSTEHO (TX POWER)</h3>
      <input type="range" id="pwrRange" min="2" max="17" value="2" onchange="updatePower(this.value)" style="width: 80%;">
      <p><span id="pwrVal">2</span> dBm</p>
    </div>
  </div>

  <div id="status">Yhdistetään...</div>
<script>
  var socket;
  var isWaiting = false; // Lukko selaimen päässä

  function connect() {
    socket = new WebSocket('ws://' + window.location.hostname + ':81/');
    socket.onopen = function() { 
      updateStatus('Yhteys kunnossa', '#2ecc71'); 
    };
    
    socket.onmessage = function(e) {
      // Vapautetaan lukko HETI kun jotain tulee, jotta selain ei jää jumiin
      isWaiting = false; 
      toggleButtons(true);
      
      console.log('Received raw: ' + e.data);
      
      try {
        // Joskus WebSocket saattaa yhdistää kaksi pakettia, 
        // etsitään ensimmäinen kokonainen JSON-objekti { }
        var rawData = e.data.trim();
        var firstCleanJson = rawData.substring(rawData.indexOf('{'), rawData.lastIndexOf('}') + 1);
        
        var data = JSON.parse(firstCleanJson);
        
        if(data.error) {
          updateStatus('Masto: ' + data.error, '#e74c3c');
        } else {
          updateStatus('Masto päivitetty', '#3498db');
          updateUI(data);
        }
      } catch(err) { 
        console.log('JSON error', err);
        updateStatus('Yhteysvirhe (viallinen data)', '#e67e22');
      }
    };
    
    socket.onclose = function() {
      updateStatus('Yhteys katkesi - yritetään uudelleen...', '#e67e22');
      setTimeout(connect, 2000);
    };
  }

  function send(cmd) {
    if(isWaiting) return;

    if(socket && socket.readyState == WebSocket.OPEN) {
      isWaiting = true;
      toggleButtons(false);
      updateStatus('Lähetetään...', '#f1c40f');
      socket.send(cmd);

      // VARMUUSLUKKO: Jos vastausta ei kuulu 3 sekuntiin, vapautetaan napit
      setTimeout(function() {
        if(isWaiting) {
          isWaiting = false;
          toggleButtons(true);
          updateStatus('Ei vastausta mastolta', '#e74c3c');
        }
      }, 3000); 

    } else {
      alert('Ei yhteyttä siltaan!');
    }
  }

  function toggleButtons(enabled) {
    const btns = document.querySelectorAll('button');
    btns.forEach(btn => {
      // Pidetään OFF-napit aina käytettävissä tai lukitaan kaikki
      btn.disabled = !enabled;
    });
  }

  function updateStatus(msg, color) {
    const s = document.getElementById('status');
    s.innerHTML = msg;
    s.style.color = color;
  }

  function updatePower(val) {
    document.getElementById('pwrVal').innerText = val;
    // Muutetaan numero merkkijonoksi ja täytetään nollalla (2 -> "02")
    let cmd = val.toString().padStart(2, '0');
    send(cmd);
  }

  function updateUI(data) {
    const ants = ["1", "2", "3", "4", "5", "6"];

    // lähetystehon asetus
    if (data.pwr !== undefined) {
      const slider = document.getElementById('pwrRange');
      const display = document.getElementById('pwrVal');
      
      // Päivitetään sliderin asento ja numeroarvo
      slider.value = data.pwr;
      display.innerText = data.pwr;
    }
    
    // Rig A päivitys
    ants.forEach(val => {
      let btnA = document.getElementById('A' + val);
      if(data.a == val) {
          btnA.classList.add('active-a');
      } else {
          btnA.classList.remove('active-a');
      }
      // Estetään valitsemasta samaa antennia Rig B:lle
      btnA.disabled = (data.b == val);
    });

    // Rig B päivitys
    ants.forEach(val => {
      let btnB = document.getElementById('B' + val);
      if(data.b == val) {
          btnB.classList.add('active-b');
      } else {
          btnB.classList.remove('active-b');
      }
      // Estetään valitsemasta samaa antennia Rig A:lle
      btnB.disabled = (data.a == val);
    });

    // OFF-napit
    if(data.a == "-") document.getElementById('A0').classList.add('active-a');
    else document.getElementById('A0').classList.remove('active-a');
    
    if(data.b == "-") document.getElementById('B0').classList.add('active-b');
    else document.getElementById('B0').classList.remove('active-b');
  }

  connect();
</script></body></html>
)rawliteral";