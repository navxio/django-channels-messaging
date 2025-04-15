const WebSocket = require('ws');
const readline = require('readline');

const URL = 'ws://localhost:8000/ws/chat/'; // adjust if hosted elsewhere

function startClient(role) {
  const ws = new WebSocket(URL);

  ws.on('open', () => {
    console.log(`[${role.toUpperCase()}] Connected to server.`);
    askInput();
  });

  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    console.log(`[SERVER → ${role.toUpperCase()}]`, msg);
  });

  ws.on('close', () => {
    console.log(`[${role.toUpperCase()}] Disconnected.`);
    process.exit();
  });

  ws.on('error', (err) => {
    console.error('Connection error:', err);
  });

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  function askInput() {
    rl.question(`[${role.toUpperCase()}] Type a message: `, (input) => {
      if (input === '/exit') {
        ws.close();
        return;
      }

      // Send appropriate structure
      if (role === 'agent') {
        ws.send(JSON.stringify({
          type: 'agent',
          prompt: input
        }));
      } else {
        ws.send(JSON.stringify({
          type: 'chat',
          message: input
        }));
      }

      askInput(); // wait for next input
    });
  }
}

// Get role from CLI args
const role = process.argv[2];

if (!['agent', 'visitor'].includes(role)) {
  console.log('Usage: node client.js <agent|visitor>');
  process.exit(1);
}

startClient(role);
